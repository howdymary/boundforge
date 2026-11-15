"""Next eligible constant adapters, serialized after C1b credit accounting."""
import base64,hashlib,json,os,pathlib,shutil,subprocess,sys,time,urllib.request
from fractions import Fraction
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"c1ad";OUT.mkdir(exist_ok=True)
from budget import Ledger
def fetch(repo,path,ref):
 d=json.loads(subprocess.check_output(["gh","api",f"repos/{repo}/contents/{path}?ref={ref}"]))
 return base64.b64decode(d["content"]) if d.get("content") else urllib.request.urlopen(d["download_url"],timeout=60).read()
def check(p,name):return json.loads(subprocess.check_output([sys.executable,"-I",str(HERE/name),str(p)]))
def main():
 previous=HERE/"c1b";pr=json.loads((previous/"report.json").read_text());shutil.copyfile(previous/"budget.sqlite",OUT/"budget.sqlite");ledger=Ledger(OUT)
 # A tiny candidate remains subject to final literature/threshold audit. If an
 # Arena-sized improvement has already appeared, do not launch more paid work.
 gain=Fraction(pr["baseline"])-Fraction(pr["best"])
 if gain>=Fraction(1,10**7):
  (OUT/"report.json").write_text(json.dumps({"skipped":True,"reason":"C1b already passed Arena-sized improvement gate; finish certification first","ledger":ledger.summary()}));return
 specs=[];baselines={};sources={}
 for kind in ["C_1d","C_1a"]:
  if kind=="C_1d":
   repo="arhancanli/quantavane-replays";ref="cc2c67deb49fb09bcdc1947d0ad0b6ee2b9106b5";path="improvements/c1d/c1d_upper_n163840_v2.json";raw=fetch(repo,path,ref)
   assert hashlib.sha256(raw).hexdigest()=="253d0ca68f060eedc6fd24e3afc6b1ce477cb6a97e25d80453e4616362153a82"
   cert=json.loads(raw);expected=Fraction(838861227937471890002426104328885370880,576666392427609677715360509915372739121)
  else:
   repo="intervalplace/frontier";ref="8c9fa72";path="c1-first-autocorrelation/C1_262144_1.5026648336.txt";raw=fetch(repo,path,ref)
   assert hashlib.sha256(raw).hexdigest()=="b33995fe340396b6830ee8b1c6ec270acf9fdde59a35db6cb4e9f558d4f35495"
   vals=list(map(int,raw.decode().split()));assert len(vals)==262144
   cert={"constant":"C_1a","v_int":vals};expected=Fraction(11484584234108926456768515550896128,7642811608550585358028269349510225)
  p=OUT/(kind+"-baseline.json");p.write_text(json.dumps(cert));a=check(p,"c1d_exact.py");b=check(p,"c1d_ntt.py");assert Fraction(a["score"])==Fraction(b["score"])==expected
  baselines[kind]={"certificate":cert,"packed":a,"NTT":b};sources[kind]={"url":f"https://github.com/{repo}/blob/{ref}/{path}","sha256":hashlib.sha256(raw).hexdigest()}
  print("C1AD_BASELINE "+json.dumps({"kind":kind,"score":str(expected),"n":len(cert["v_int"])}),flush=True)
 (OUT/"baseline-checks.json").write_text(json.dumps({k:{q:v for q,v in val.items() if q!="certificate"} for k,val in baselines.items()},indent=2));(OUT/"sources.json").write_text(json.dumps(sources,indent=2))
 for i,(kind,p0,refine,kick) in enumerate([("C_1d",3e7,1,0),("C_1d",1e8,1,1e-6),("C_1d",3e7,2,0),("C_1d",3e6,1,2e-5),("C_1a",3e7,1,0),("C_1a",1e8,1,1e-6)]):
  specs.append({"kind":kind,"p0":p0,"refine":refine,"kick":kick,"seed":900+i,"seconds":420})
 (OUT/"specs.json").write_text(json.dumps(specs,indent=2))
 import modal
 image=modal.Image.debian_slim(python_version="3.11").pip_install("numpy==2.3.5","scipy==1.16.3").add_local_file(str(HERE/"c1d_search.py"),"/root/c1d_search.py",copy=True)
 app=modal.App("boundforge-record-autoconvolution")
 @app.function(image=image,cpu=1,memory=2048,timeout=480,max_containers=4,serialized=True)
 def work(cert,spec):
  import sys;sys.path.insert(0,"/root")
  from c1d_search import run
  return run(cert,spec)
 ledger.reserve("modal",2,"autoconvolution image/build");rows=[];checks=[];start=time.monotonic()
 with modal.enable_output(),app.run():
  pending=[]
  for spec in specs:ledger.reserve("modal",1.5,"bounded420s autoconvolution worker");pending.append(work.spawn(baselines[spec["kind"]]["certificate"],spec))
  for i,call in enumerate(pending):
   r=call.get();rows.append(r);(OUT/"runs.json").write_text(json.dumps(rows))
   p=OUT/("candidate-"+str(i)+".json");p.write_text(json.dumps(r["candidate"]));a=check(p,"c1d_exact.py");b=check(p,"c1d_ntt.py");assert a["score"]==b["score"]
   kind=r["spec"]["kind"];gain=Fraction(baselines[kind]["packed"]["score"])-Fraction(a["score"])
   checks.append({"index":i,"kind":kind,"score":a["score"],"gain":str(gain),"project_record_candidate":gain>Fraction(1,10**12),"packed":a,"NTT":b})
   (OUT/"checks.json").write_text(json.dumps(checks,indent=2));print("C1AD_RESULT "+json.dumps(checks[-1]),flush=True)
 report={"run_id":os.environ["GITHUB_RUN_ID"],"source_sha":os.environ["GITHUB_SHA"],"outcomes":checks,"new_record_candidate":any(c["project_record_candidate"] for c in checks),"ledger":ledger.summary(),"elapsed_seconds":time.monotonic()-start,"scope":"Exact improvements over audited primary witnesses, pending final frontier refresh. Standard continuation, no method-novelty claim."}
 (OUT/"report.json").write_text(json.dumps(report,indent=2));print("C1AD_FINAL "+json.dumps(report),flush=True)
if __name__=="__main__":main()
