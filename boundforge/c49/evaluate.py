"""Frozen held-out comparison. No model/web adaptation while outcomes are opened."""
import collections,hashlib,itertools,json,math,os,pathlib,shutil,statistics,subprocess,time
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"evaluation";OUT.mkdir(exist_ok=True)
from tasks import heldout_tasks,isvalid_c49
from budget import Ledger
from exact import rate_interval,improves
def main():
 frozen=HERE/"freeze";freeze=json.loads((frozen/"freeze.json").read_text())
 for p,h in freeze["code_hashes"].items():assert hashlib.sha256((HERE/p).read_bytes()).hexdigest()==h,("frozen source changed",p)
 shutil.copyfile(frozen/"budget.sqlite",OUT/"budget.sqlite");ledger=Ledger(OUT)
 import modal
 image=modal.Image.debian_slim(python_version="3.11").apt_install("g++")
 for name in ["search.cpp","worker.py","controller.py","episode.py"]:image=image.add_local_file(str(HERE/name),"/root/c49/"+name,copy=True)
 image=image.run_commands("g++ -O3 -std=c++17 /root/c49/search.cpp -o /root/c49/search")
 app=modal.App("boundforge-c49-frozen-evaluation")
 @app.function(image=image,cpu=1,memory=1024,timeout=90,max_containers=8,serialized=True)
 def work(task,freeze,arm,seed):
  import sys;sys.path.insert(0,"/root/c49")
  from episode import episode
  return episode(task,freeze,arm,seed,freeze["steps"],freeze["quantum_cpu_ms"])
 ledger.reserve("modal",2,"evaluation image/build")
 specs=[(t,a,s) for t in heldout_tasks() for s in freeze["seeds"] for a in freeze["arms"]]
 rows=[];start=time.monotonic()
 with modal.enable_output(),app.run():
  for index in range(0,len(specs),16):
   pending=[]
   for task,arm,seed in specs[index:index+16]:
    ledger.reserve("modal",.04,"bounded evaluation episode");pending.append(work.spawn(task,freeze,arm,seed))
   for call in pending:
    r=call.get();rows.append(r)
    (OUT/"episodes.json").write_text(json.dumps(rows))
   print("C49_EVAL_PROGRESS "+json.dumps({"episodes":len(rows),"total":len(specs),"cpu_seconds":sum(x["cpu_seconds"] for x in rows)}),flush=True)
 # Independent exact checks of every reported best family.
 subprocess.run(["g++","-O3","-std=c++17",str(HERE/"verify_bdd.cpp"),"-o",str(OUT/"bdd")],check=True)
 subprocess.run(["g++","-O3","-std=c++17",str(HERE/"graph_dump.cpp"),"-o",str(OUT/"graph")],check=True)
 checks=[];best=None;checked={}
 for r in rows:
  family=r["best_family"];key=(r["kind"],r["n"],r["param"],tuple(family))
  if key in checked:checks.append(checked[key]);continue
  assert len(family)==len(set(family))
  if r["kind"]==0:
   assert isvalid_c49(family,r["n"])
   p=OUT/"candidate.masks";p.write_text("\n".join(map(str,family)))
   b=json.loads(subprocess.check_output([str(OUT/"bdd"),str(p),str(r["n"]),*map(str,r["ports"])]))
   exact=rate_interval(b["counts"],r["n"]-2)
   record=improves(b["counts"],r["n"]-2)
   if record and (best is None or improves(b["counts"],r["n"]-2,best["rate"]["counts"],best["n"]-2)):best={"n":r["n"],"ports":r["ports"],"masks":family,"rate":exact,"source":{"arm":r["arm"],"seed":r["seed"]}}
   c={"task":r["task"],"valid":True,"checkers":["literal Python","BDD C++"],"exact":exact,"beats_frontier":record}
  elif r["kind"]==1:
   edges=json.loads(subprocess.check_output([str(OUT/"graph"),str(r["n"]),str(r["param"])]));s=set(family)
   assert all(0<=x<r["n"] for x in s) and not any(a in s and b in s for a,b in edges)
   c={"task":r["task"],"valid":True,"members":len(s),"graph_sha256":hashlib.sha256(json.dumps(edges).encode()).hexdigest()}
  else:
   assert all(0<=x<3**r["n"] for x in family)
   def line(a,b,c):
    for _ in range(r["n"]):
     if (a%3+b%3+c%3)%3:return False
     a//=3;b//=3;c//=3
    return True
   assert not any(line(*t) for t in itertools.combinations(family,3))
   c={"task":r["task"],"valid":True,"members":len(family),"definition":"no three distinct points with sum0 in F3^d"}
  checked[key]=c;checks.append(c)
 (OUT/"checks.json").write_text(json.dumps(checks,indent=2))
 if best:(OUT/"new-record.json").write_text(json.dumps(best,indent=2))
 summaries={}
 for task in freeze["heldout_tasks"]:
  summaries[task]={}
  for arm in freeze["arms"]:
   rr=[r for r in rows if r["task"]==task and r["arm"]==arm]
   summaries[task][arm]={"n":len(rr),"mean":statistics.mean(r["best_score"] for r in rr),"std":statistics.pstdev(r["best_score"] for r in rr),"min":min(r["best_score"] for r in rr),"max":max(r["best_score"] for r in rr),"cpu_seconds":sum(r["cpu_seconds"] for r in rr),"tested":sum(r["tested"] for r in rr)}
 report={"source_sha":os.environ["GITHUB_SHA"],"run_id":os.environ["GITHUB_RUN_ID"],"freeze_source_run":freeze["run_id"],"freeze_sha256":hashlib.sha256((frozen/"freeze.json").read_bytes()).hexdigest(),"episodes":len(rows),"summaries":summaries,"new_record":best is not None,"elapsed_seconds":time.monotonic()-start,"ledger":ledger.summary(),"scope":"Descriptive7-start comparison on2 C49 families and3 auxiliary instances; no universal superiority claim."}
 (OUT/"report.json").write_text(json.dumps(report,indent=2));print("C49_EVAL_FINAL "+json.dumps(report),flush=True)
if __name__=="__main__":main()
