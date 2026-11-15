"""Paid C1b pilot after exact baseline reproduction; all worker deadlines bounded."""
import base64,hashlib,json,os,pathlib,subprocess,sys,time
from fractions import Fraction
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"c1b";OUT.mkdir(exist_ok=True)
from budget import Ledger
def fetch(p):
 repo="intervalplace/frontier";pin="6d6c4bac7b04cc224c1bb6016f594e5b785e3f48"
 d=json.loads(subprocess.check_output(["gh","api",f"repos/{repo}/contents/c1b-erdos-minimum-overlap/{p}?ref={pin}"]));return base64.b64decode(d["content"])
def check(p,name):return json.loads(subprocess.check_output([sys.executable,"-I",str(HERE/name),str(p)]))
def main():
 start=time.monotonic();raw=fetch("C1b_15360_0.3808564712.json")
 assert hashlib.sha256(raw).hexdigest()=="7bfe24a36566ee3544d22f4064e9cb64495b21431a31f521de390dc5f0865b7b"
 base=OUT/"baseline.json";base.write_bytes(raw);cert=json.loads(raw);baseline=check(base,"c1b_exact.py");second=check(base,"c1b_ntt.py")
 assert baseline["score"]==second["score"]==str(Fraction(3707849734734953936493216938911489,9735556609752801803494680617287680))
 (OUT/"baseline-verification.json").write_text(json.dumps({"packed":baseline,"NTT":second,"source":"intervalplace/frontier@6d6c4ba","primary_sha256":hashlib.sha256(raw).hexdigest()},indent=2))
 # Free runner reproduces all-shift acceptance before the first paid reservation.
 import numpy as np
 from c1b_search import values
 a=np.array(cert["heights_int"],dtype=float)/cert["Q"];v=values(a);top=float(v.max())
 diagnostic={"n":len(a),"score":top,"within_1e_8":int(np.sum(top-v<1e-8)),"within_1e_10":int(np.sum(top-v<1e-10)),"within_1e_12":int(np.sum(top-v<1e-12)),"interior_heights":int(np.sum((a>0)&(a<1)))}
 (OUT/"diagnostic.json").write_text(json.dumps(diagnostic,indent=2));print("C1B_BASELINE "+json.dumps(diagnostic),flush=True)
 ledger=Ledger(OUT)
 import modal
 image=modal.Image.debian_slim(python_version="3.11").pip_install("numpy==2.3.5","scipy==1.16.3").add_local_file(str(HERE/"c1b_search.py"),"/root/c1b_search.py",copy=True)
 app=modal.App("boundforge-record-c1b")
 @app.function(image=image,cpu=1,memory=2048,timeout=420,max_containers=4,serialized=True)
 def work(cert,spec):
  import sys;sys.path.insert(0,"/root")
  from c1b_search import run
  return run(cert,spec)
 specs=[{"refine":r,"beta":b,"factor":1.6,"seed":700+i,"seconds":360,"kick":k} for i,(r,b,k) in enumerate([(1,3e8,0),(1,1e9,0),(1,3e9,1e-6),(2,3e8,0),(2,1e9,0),(2,3e9,1e-6)])]
 (OUT/"specs.json").write_text(json.dumps(specs,indent=2));ledger.reserve("modal",2,"C1b image/build");rows=[];checks=[];best=Fraction(baseline["score"])
 with modal.enable_output(),app.run():
  calls=[]
  for spec in specs:ledger.reserve("modal",1.2,"C1b bounded360s worker");calls.append(work.spawn(cert,spec))
  for i,call in enumerate(calls):
   row=call.get();rows.append(row);(OUT/"runs.json").write_text(json.dumps(rows))
   p=OUT/("candidate-"+str(i)+".json");p.write_text(json.dumps(row["candidate"]))
   one=check(p,"c1b_exact.py");two=check(p,"c1b_ntt.py");assert one["score"]==two["score"]
   rate=Fraction(one["score"]);improved=rate<Fraction(baseline["score"]);checks.append({"index":i,"packed":one,"NTT":two,"strict_improvement":improved,"gain_exact":str(Fraction(baseline["score"])-rate)})
   if rate<best:best=rate;(OUT/"best.json").write_bytes(p.read_bytes())
   (OUT/"checks.json").write_text(json.dumps(checks,indent=2))
   print("C1B_RESULT "+json.dumps({"index":i,"spec":row["spec"],"score":str(rate),"float_gain":row["float_gain"],"strict_improvement":improved,"calls":row["calls"]}),flush=True)
 report={"run_id":os.environ["GITHUB_RUN_ID"],"source_sha":os.environ["GITHUB_SHA"],"baseline":baseline["score"],"best":str(best),"new_record_candidate":best<Fraction(baseline["score"]),"ledger":ledger.summary(),"elapsed_seconds":time.monotonic()-start,"outcomes":checks,"scope":"An exact improvement over the audited strongest public witness is a candidate record, pending final independent recertification and live frontier refresh. No method novelty or significance magnitude is assumed."}
 (OUT/"report.json").write_text(json.dumps(report,indent=2));print("C1B_FINAL "+json.dumps(report),flush=True)
if __name__=="__main__":main()
