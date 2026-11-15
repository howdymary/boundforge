"""Bounded parallel development pilot. Workers have no repository/provider keys."""
import argparse,hashlib,json,os,pathlib,random,statistics,time
from ..ledger import reserve
from .certify import verify,verify_intervals
def main():
 import modal
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True);root=pathlib.Path(__file__).resolve().parent
 image=modal.Image.debian_slim(python_version="3.11").add_local_dir(str(root),"/root/collision",copy=True)
 app=modal.App("boundforge-collision-development")
 @app.function(image=image,cpu=1,memory=1024,timeout=60,max_containers=8,retries=0,serialized=True)
 def work(spec,policy,seed,cpu):
  import sys;sys.path.insert(0,"/root")
  from collision.search import episode
  return episode(spec,policy,seed,cpu,certify=False)
 policies=["coordinate","random_flat","circuit","random_pivot","guided_pivot","shuffled_core"]
 controlsets=[[(1,0),(0,1),(1,1)],[(1,0),(0,1),(1,1),(1,2)],[(1,0),(0,1),(1,1),(1,2),(1,3)]]
 specs=[([m,controls],policy,seed,1.2)for m in [6,8,10]for controls in controlsets for policy in policies for seed in [9101,9102,9103]]
 random.Random(411).shuffle(specs);rows=[];holds=[];start=time.monotonic();hold=reserve("modal",2,"bounded CPU image/setup; actual receipt unresolved");holds.append(hold)
 with modal.enable_output(),app.run():
  for at in range(0,len(specs),8):
   batch=specs[at:at+8];holds.append(reserve("modal",.05*len(batch),"collision pilot batch "+str(at)+"; 1CPU/1GiB/60s max per call, no retries"))
   calls=[work.spawn(*spec)for spec in batch]
   for call in calls:
    try:r=call.get(timeout=90)
    except Exception as e:
     rows.append({"status":"worker_failed","error_type":type(e).__name__});(out/"episodes.json").write_text(json.dumps(rows));raise
    v=time.process_time();r["check"]=verify(r["witness"]);r["second_check"]=verify_intervals(r["witness"]);r["parent_verification_cpu"]=time.process_time()-v;r["status"]="verified";rows.append(r)
    (out/"episodes.json").write_text(json.dumps(rows))
   print(json.dumps({"completed":len(rows),"total":len(specs),"worker_cpu":sum(r.get("total_cpu",0)for r in rows)}),flush=True)
 report={"run_id":os.environ.get("GITHUB_RUN_ID"),"source_sha":os.environ.get("GITHUB_SHA"),"stage":"development_only","episodes":len(rows),"source_hashes":{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in root.glob("*.py")},"worker_cpu":sum(r["total_cpu"]for r in rows),"parent_verification_cpu":sum(r["parent_verification_cpu"]for r in rows),"wall":time.monotonic()-start,"modal_allocations":{"cpu":1,"memory_mib":1024,"timeout_seconds":60,"max_containers":8,"gpu":0,"retries":0},"unresolved_modal_hold_usd":2+.05*len(specs),"reservation_ids":holds,"new_method_claim":False,"record_claim":False}
 summaries={}
 for m in [6,8,10]:
  for k in [3,4,5]:
   name="m"+str(m)+"-controls"+str(k);summaries[name]={}
   for pol in policies:
    rr=[r for r in rows if r["task"]["m"]==m and len(r["task"]["controls"])==k and r["policy"]==pol]
    summaries[name][pol]={"values":[r["best_ratio"]for r in rr],"mean":statistics.mean(r["best_ratio"]for r in rr),"parent_verified":all(r["check"]["valid"]and r["second_check"]["valid"]for r in rr),"pivots":sum(r["representation_changes"]for r in rr),"pivots_enabling_one_row":sum(r["directed_pivots_enabled"]for r in rr),"worker_cpu":sum(r["total_cpu"]for r in rr)}
 report["summaries"]=summaries;(out/"report.json").write_text(json.dumps(report,indent=2));print("COLLISION_REPORT "+json.dumps(report),flush=True)
if __name__=="__main__":main()
