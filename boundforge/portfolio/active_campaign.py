import json,os,pathlib,shutil,subprocess,sys,time
from fractions import Fraction
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"active";OUT.mkdir(exist_ok=True)
from budget import Ledger
def main():
 old=HERE/"c1ad";shutil.copyfile(old/"budget.sqlite",OUT/"budget.sqlite");ledger=Ledger(OUT)
 specs=[{"kind":"C_1d","blocks":256,"radius":.001,"seconds":300},{"kind":"C_1d","blocks":512,"radius":.0001,"seconds":300},{"kind":"C_1a","blocks":512,"radius":.0001,"seconds":300}]
 base={k:json.loads((old/(k+"-baseline.json")).read_text())for k in ["C_1d","C_1a"]}
 checks0=json.loads((old/"baseline-checks.json").read_text())
 import modal
 image=modal.Image.debian_slim(python_version="3.11").pip_install("numpy==2.3.5","scipy==1.16.3").add_local_file(str(HERE/"active_search.py"),"/root/active_search.py",copy=True)
 app=modal.App("boundforge-record-active-knot")
 @app.function(image=image,cpu=1,memory=3072,timeout=360,max_containers=3,serialized=True)
 def work(cert,spec):
  import sys;sys.path.insert(0,"/root")
  from active_search import run
  return run(cert,spec)
 ledger.reserve("modal",2,"active-knot image/build");rows=[];checks=[];start=time.monotonic()
 with modal.enable_output(),app.run():
  calls=[]
  for sp in specs:
   ledger.reserve("modal",1.2,"active-knot bounded 300s CPU worker");calls.append(work.spawn(base[sp["kind"]],sp))
  for i,call in enumerate(calls):
   r=call.get();rows.append(r);(OUT/"runs.json").write_text(json.dumps(rows))
   p=OUT/("candidate-"+str(i)+".json");p.write_text(json.dumps(r["candidate"]))
   res=[json.loads(subprocess.check_output([sys.executable,"-I",str(HERE/checker),str(p)]))for checker in ["c1d_exact.py","c1d_ntt.py"]]
   assert res[0]["score"]==res[1]["score"];kind=r["spec"]["kind"]
   gain=Fraction(checks0[kind]["packed"]["score"])-Fraction(res[0]["score"])
   checks.append({"i":i,"kind":kind,"score":res[0]["score"],"gain":str(gain),"record_candidate":gain>Fraction(1,10**12),"checkers":res})
 report={"run_id":os.environ["GITHUB_RUN_ID"],"source_sha":os.environ["GITHUB_SHA"],"checks":checks,"ledger":ledger.summary(),"seconds":time.monotonic()-start,"scope":"Exact comparison with audited incumbents; final new-frontier audit still required."}
 (OUT/"report.json").write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=="__main__":main()
