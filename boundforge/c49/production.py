"""Exploratory new-family search after a stalled greedy pilot, kept outside held-out study."""
import hashlib,json,os,pathlib,shutil,subprocess,time
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"production";OUT.mkdir(exist_ok=True)
from budget import Ledger
from exact import bounds,rate_interval,improves
from tasks import isvalid_c49
def main():
 latest=HERE/"model_study/budget.sqlite"
 shutil.copyfile(latest if latest.exists() else HERE/"evaluation/budget.sqlite",OUT/"budget.sqlite");ledger=Ledger(OUT)
 import modal
 image=modal.Image.debian_slim(python_version="3.11").pip_install("ortools==9.15.6755")
 for name in ["cp_search.py","tasks.py"]:image=image.add_local_file(str(HERE/name),"/root/c49/"+name)
 app=modal.App("boundforge-c49-constraint-separation")
 @app.function(image=image,cpu=2,memory=3072,timeout=420,max_containers=4,serialized=True)
 def work(spec):
  import sys;sys.path.insert(0,"/root/c49")
  from cp_search import run
  return run(spec)
 ledger.reserve("modal",2,"constraint image/build")
 _,barhi=bounds([33980,64728,64728,88867],26)
 specs=[]
 for n,num in [(10,145),(10,148),(10,150),(10,155),(11,160),(11,170)]:
  upper=barhi**(n-2);den=10**6;lam=upper.numerator*den//upper.denominator+1
  specs.append({"n":n,"ratio_num":num,"ratio_den":100,"lambda_num":lam,"lambda_den":den,"seconds":300,"seed":701+len(specs)})
 (OUT/"specs.json").write_text(json.dumps(specs,indent=2));rows=[]
 with modal.enable_output(),app.run():
  pending=[]
  for spec in specs:
   ledger.reserve("modal",1.2,"bounded CP-SAT worker");pending.append(work.spawn(spec))
  for call in pending:
   r=call.get();rows.append(r);(OUT/"runs.json").write_text(json.dumps(rows))
   print("C49_PRODUCTION_PROGRESS "+json.dumps({k:v for k,v in r.items() if k not in ["trace","candidate"]}|{"iterations":len(r["trace"]),"candidate_found":r["candidate"] is not None}),flush=True)
 subprocess.run(["g++","-O3","-std=c++17",str(HERE/"verify_bdd.cpp"),"-o",str(OUT/"bdd")],check=True)
 certificates=[]
 for r in rows:
  c=r["candidate"]
  if c is None:continue
  assert isvalid_c49(c["masks"],c["n"])
  path=OUT/"candidate.masks";path.write_text("\n".join(map(str,c["masks"])))
  checked=json.loads(subprocess.check_output([str(OUT/"bdd"),str(path),str(c["n"]),*map(str,c["ports"])]))
  rate=rate_interval(checked["counts"],c["n"]-2);c.update(rate=rate,strict_improvement=improves(checked["counts"],c["n"]-2))
  certificates.append(c)
 (OUT/"certificates.json").write_text(json.dumps(certificates,indent=2))
 report={"source_sha":os.environ["GITHUB_SHA"],"run_id":os.environ["GITHUB_RUN_ID"],"runs":len(rows),"new_record":any(c["strict_improvement"] for c in certificates),"cpu_seconds":sum(r["cpu_seconds"] for r in rows),"ledger":ledger.summary(),"outcomes":[{"spec":r["spec"],"iterations":len(r["trace"]),"final":r["trace"][-1] if r["trace"] else None,"candidate_found":r["candidate"] is not None} for r in rows]}
 (OUT/"report.json").write_text(json.dumps(report,indent=2));print("C49_PRODUCTION_FINAL "+json.dumps(report),flush=True)
if __name__=="__main__":main()
