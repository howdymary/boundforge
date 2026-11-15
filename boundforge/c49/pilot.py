"""Paired, bounded development study; no held-out results are opened."""
import datetime as dt,json,os,pathlib,sys,subprocess,hashlib,time
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"pilot";OUT.mkdir(exist_ok=True)
from tasks import dev_tasks,digest,isvalid_c49
def main():
 if not os.environ.get("GITHUB_ACTIONS"):raise SystemExit("remote only")
 import modal
 image=(modal.Image.debian_slim(python_version="3.11").apt_install("g++")
  .add_local_file(str(HERE/"search.cpp"),"/root/c49/search.cpp",copy=True)
  .add_local_file(str(HERE/"worker.py"),"/root/c49/worker.py",copy=True)
  .run_commands("g++ -O3 -std=c++17 /root/c49/search.cpp -o /root/c49/search"))
 app=modal.App("boundforge-c49-pilot")
 @app.function(image=image,cpu=1,memory=1024,timeout=90,max_containers=4,serialized=True)
 def work(task,state,seed):
  import sys;sys.path.insert(0,"/root/c49")
  from worker import paired
  return paired(task,state,seed)
 # Fixed worst-case allowance: imageUSD2 + 24workersUSD0.20. Actual charges remain held.
 from budget import Ledger
 ledger=Ledger(OUT);ledger.reserve("modal",2,"image/build")
 specs=[]
 for task in dev_tasks():
  assert isvalid_c49(task["state"],task["n"])
  # Four saved states per family: original plus deterministic deletions.
  for k in range(4):
   state=task["state"] if k==0 else task["state"][k*2:]
   for seed in [101,202,303]:specs.append((task,state,k,seed))
 rows=[]
 with modal.enable_output(),app.run():
  for start in range(0,len(specs),8):
   batch=[]
   for task,state,k,seed in specs[start:start+8]:
    ledger.reserve("modal",.2,"paired worker")
    batch.append((task,state,k,seed,work.spawn(task,state,seed)))
   for task,state,k,seed,call in batch:
    result=call.get()
    row={"task":task,"state":state,"state_hash":digest(state),"state_index":k,"seed":seed,"interventions":result}
    rows.append(row)
    (OUT/"paired.json").write_text(json.dumps(rows))
    print("C49_PILOT_ROW "+json.dumps({k:v for k,v in row.items() if k not in ["task","state","interventions"]}|{"task_id":task["id"],"actions":[{"action":x["action"],"best_score":x["best_score"],"cpu_seconds":x["cpu_seconds"],"tested":x["tested"],"rejected":x["rejected"]} for x in result]}),flush=True)
 report={"source_sha":os.environ["GITHUB_SHA"],"run_id":os.environ["GITHUB_RUN_ID"],"paired_states":8,"seeds":3,"worker_calls":len(rows),"interventions":len(rows)*6,"initialization_differences":"Saved states differ by deletion; not independent construction families.","cpu_seconds":sum(x["cpu_seconds"] for r in rows for x in r["interventions"]),"ledger":ledger.summary()}
 (OUT/"report.json").write_text(json.dumps(report,indent=2));print("C49_PILOT_FINAL "+json.dumps(report),flush=True)
if __name__=="__main__":main()
