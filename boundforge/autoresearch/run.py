"""One command runs the bounded research loop; no winner is supplied to workers."""
import argparse,hashlib,json,os,pathlib,subprocess,sys,time
from fractions import Fraction as F
from .trace import Trace,digest,canonical
from .policy import choose,diagnose
HERE=pathlib.Path(__file__).resolve().parent;PORT=HERE.parent/"portfolio"
def filehash(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic_json(p,v):
 temp=p.with_suffix(".tmp");temp.write_text(json.dumps(v,indent=2)+"\n");os.replace(temp,p)
def sandbox(req,args,deadline=None):
 import uuid
 container="boundforge-"+uuid.uuid4().hex[:18]
 if args.sandbox=="docker":
  cmd=["docker","run","--name",container,"--rm","-i","--ulimit","cpu=25:25","--network","none","--read-only","--cpus","1","--memory","1g","--pids-limit","64","--cap-drop","ALL","--security-opt","no-new-privileges","--tmpfs","/tmp:rw,noexec,nosuid,size=64m",args.image]
 else:cmd=[sys.executable,"-I",str(HERE/"worker.py")]
 try:p=subprocess.run(cmd,input=canonical(req),capture_output=True,text=True,timeout=min(req["seconds"]+15,max(.1,deadline-time.monotonic()))if deadline else req["seconds"]+15,env={"PATH":os.environ["PATH"]})
 except subprocess.TimeoutExpired:
  if args.sandbox=="docker":subprocess.run(["docker","rm","-f",container],capture_output=True,timeout=10)
  raise
 if p.returncode:return {"status":"optimizer_failure","error_type":"worker_exit","detail":p.stderr[-300:]}
 try:r=json.loads(p.stdout)
 except Exception:return {"status":"optimizer_failure","error_type":"invalid_worker_json","detail":p.stdout[-200:]}
 if r.get("request_sha256")!=digest(req):raise ValueError("worker request hash mismatch")
 return r
def certificate(path,out,incumbent,theta,upstream=False,deadline=None):
 reports={}
 for name in ["c51_bernstein.py","c51_taylor.py"]:
  p=subprocess.run([sys.executable,"-I",str(PORT/name),str(path)],capture_output=True,text=True,timeout=min(60,max(.1,deadline-time.monotonic()))if deadline else 60,env={"PATH":os.environ["PATH"]})
  if p.returncode:raise ValueError(name+" refused: "+p.stderr[-400:])
  r=json.loads(p.stdout)
  if not r.get("valid"):raise ValueError("invalid check result")
  reports[name]=r;atomic_json(out/(name+".json"),r)
 data=json.loads(path.read_text());claim=F(data["lower_bound"])
 if any(F(r["lower_bound"])!=claim for r in reports.values()):raise ValueError("checker objective mismatch")
 from boundforge.portfolio.c51_bernstein import witness_upper
 old_upper=min(witness_upper(incumbent,"0"),witness_upper(incumbent,theta))
 if claim<=old_upper:raise ValueError("does not beat actual registered incumbent")
 external=None
 if upstream:
  from .upstream_verify import verify
  external=verify(path,out/"published-checker",deadline=deadline)
  if not external["valid"]:raise ValueError("separately authored checker refuses")
 return {"candidate_sha256":filehash(path),"lower_bound":str(claim),"previous_actual_beta_upper":str(old_upper),"strict_gain_lower":str(claim-old_upper),"checkers":reports,"published_checker":external}
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument("--out",type=pathlib.Path,required=True);p.add_argument("--registry",type=pathlib.Path,default=HERE/"frontier.json");p.add_argument("--sandbox",choices=["docker","process"],default="docker");p.add_argument("--image",default="boundforge-research-worker");p.add_argument("--policy",choices=["diagnostic","fixed_float","fixed_precision"],default="diagnostic");p.add_argument("--max-steps",type=int,default=6);p.add_argument("--wall-seconds",type=int,default=180);p.add_argument("--seed",type=int,default=51301);p.add_argument("--resume",action="store_true");p.add_argument("--upstream",action="store_true");p.add_argument("--providers",action="store_true");args=p.parse_args(argv)
 if args.max_steps<1 or not 1<=args.wall_seconds<=600:raise ValueError("bounded limits required")
 args.out.mkdir(parents=True,exist_ok=True);trace=Trace(args.out);registry=json.loads(args.registry.read_text())
 if registry.get("unresolved_claims"):raise ValueError("unresolved frontier claim requires review")
 sources={q.name:filehash(q)for q in sorted(HERE.glob("*.py"))};sources.update({q:filehash(HERE/q)for q in ["Dockerfile","requirements-worker.txt"]});sources.update({q:filehash(PORT/q)for q in ["c51_bernstein.py","c51_taylor.py"]})
 config={"registry":registry,"source_hashes":sources,"policy":args.policy,"seed":args.seed,"max_steps":args.max_steps,"wall_seconds":args.wall_seconds,"sandbox":args.sandbox,"image":args.image,"providers":args.providers,"upstream":args.upstream};confhash=digest(config);statepath=args.out/"checkpoint.json"
 if statepath.exists():
  if not args.resume:raise ValueError("output already has checkpoint; use --resume")
  state=json.loads(statepath.read_text())
  if state["config_sha256"]!=confhash:raise ValueError("resume input/source/config changed")
  if state["status"]!="running":
   report=json.loads((args.out/"report.json").read_text())
   for path,sha in report["artifact_hashes"].items():
    if filehash(args.out/path)!=sha:raise ValueError("retained artifact changed")
   print(json.dumps(report));return report
 else:
  state={"status":"running","config_sha256":confhash,"history":[],"elapsed_seconds":0.,"step":0}
  trace.add("campaign_start",config=config,config_sha256=confhash,source_sha=os.environ.get("GITHUB_SHA"),chronology=registry["chronology"],fresh_discovery=False)
  # Baseline reproduction occurs in the trusted acceptance process.
  bp=args.out/"baseline.json";atomic_json(bp,registry["incumbent"])
  for check in ["c51_bernstein.py","c51_taylor.py"]:
   r=subprocess.run([sys.executable,"-I",str(PORT/check),str(bp)],capture_output=True,text=True,timeout=60,env={"PATH":os.environ["PATH"]})
   if r.returncode:raise ValueError("baseline replay refused "+r.stderr[-300:])
   trace.add("baseline_certified",checker=check,result=json.loads(r.stdout),baseline_sha256=filehash(bp))
  if args.sandbox=="docker":
   meta=json.loads(subprocess.check_output(["docker","image","inspect",args.image]))[0]
   trace.add("worker_isolation",image_id=meta["Id"],network="none",filesystem="read-only",mounted_repository=False,credentials_passed=False,source_inventory=["worker.py","pinned numerical dependencies"],limits={"CPU":1,"memory":"1g","pids":64})
  else:trace.add("worker_isolation",scope="trusted-process testing only; not a filesystem sandbox")
  trace.save(state)
 start=time.monotonic();elapsed_start=state["elapsed_seconds"];deadline=start+args.wall_seconds-elapsed_start;providers=None
 if args.providers:
  from .services import Services
  providers=Services(args.out,trace)
 accepted=None
 for step in range(state["step"],args.max_steps):
  elapsed=elapsed_start+time.monotonic()-start
  if elapsed>=args.wall_seconds-10:trace.add("stop",reason="wall allowance reached",elapsed=elapsed);break
  action,why=choose(state["history"],args.policy)
  if providers and state["history"]:
   advisory=providers.research_and_choose(state["history"][-1],action,registry)
   if advisory.get("frontier_review_required"):trace.add("stop",reason="new unverified frontier lead");break
   if advisory.get("action")in["float_local","precision_equioscillation","precision_restart"]:action=advisory["action"];why["provider_advisory"]=advisory
  trace.add("decision",step=step,action=action,why=why,remaining_wall_seconds=args.wall_seconds-elapsed)
  request={"operator":"float_local"if action=="float_local"else"precision_equioscillation","restart":action=="precision_restart","incumbent":registry["incumbent"],"seed":args.seed+step,"seconds":min(15,max(1,int(args.wall_seconds-elapsed-10))),"precision":100+20*sum(h["diagnosis"]=="CERTIFICATION_FAILURE"for h in state["history"])}
  reqpath=args.out/("request-"+str(step)+".json");atomic_json(reqpath,request);trace.add("experiment_started",step=step,request_sha256=digest(request),request_path=reqpath.name,operator=action)
  try:r=sandbox(request,args,deadline)
  except subprocess.TimeoutExpired:r={"status":"optimizer_failure","error_type":"worker_timeout","detail":"bounded worker deadline"}
  rawpath=args.out/("result-"+str(step)+".json");atomic_json(rawpath,r);label,evidence=diagnose(r)
  event=trace.add("experiment_result",step=step,operator=action,diagnosis=label,evidence=evidence,result_path=rawpath.name,result_sha256=filehash(rawpath),measured_elapsed=r.get("elapsed_seconds"))
  if r.get("candidate"):
   cp=args.out/("candidate-"+str(step)+".json");atomic_json(cp,r["candidate"])
   trace.add("certification_requested",step=step,candidate_sha256=filehash(cp),candidate_path=cp.name,screen_only=True)
   try:
    accepted=certificate(cp,args.out,registry["incumbent"],r["baseline_test_theta"],args.upstream,deadline);atomic_json(args.out/"candidate.json",r["candidate"])
    trace.add("certified_improvement",step=step,result=accepted,comparison_scope=registry["reference_scope"],fresh_discovery=False)
    state["status"]="certified_historical_replay"
   except Exception as e:
    accepted=None;label="CERTIFICATION_FAILURE";evidence={"type":type(e).__name__,"detail":str(e)[:500],"scope":"specific proposal/cover, no mathematical impossibility conclusion"};event=trace.add("certification_refused",step=step,evidence=evidence)
  state["history"].append({"step":step,"operator":action,"diagnosis":label,"evidence":evidence,"event_id":event,"request_sha256":digest(request),"target":"C51a","context_sha256":digest(registry["incumbent"])})
  state["step"]=step+1;state["elapsed_seconds"]=elapsed_start+time.monotonic()-start;trace.save(state)
  if accepted:break
 state["elapsed_seconds"]=elapsed_start+time.monotonic()-start
 if state["status"]=="running":state["status"]="no_certified_improvement"
 trace.add("campaign_finished",status=state["status"],experiments=state["step"],elapsed_seconds=state["elapsed_seconds"],claimed_fresh_world_record=False)
 files={p.name:filehash(p)for p in args.out.iterdir()if p.is_file()and p.name not in ["checkpoint.json","report.json"]}
 report={"status":state["status"],"run_id":os.environ.get("GITHUB_RUN_ID"),"source_sha":os.environ.get("GITHUB_SHA"),"config_sha256":confhash,"policy":args.policy,"experiments":state["history"],"accepted":accepted,"elapsed_seconds":state["elapsed_seconds"],"artifact_hashes":files,"provider_usage":providers.summary()if providers else{"enabled":False},"comparison_scope":registry["reference_scope"],"existing_project_result":registry["existing_project_result"],"fresh_discovery":False,"scope":"Autonomous execution/reproduction from an earlier external frontier. Controller/optimizers engineered after agent-directed discovery. No hidden-result, new-method or fresh-world-record claim."}
 atomic_json(args.out/"report.json",report);trace.save(state);print(json.dumps(report));return report
if __name__=="__main__":main()
