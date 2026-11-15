"""Group matched procedures on one worker to reduce RPC and hardware imbalance."""
import argparse,json,os,pathlib,random,statistics,time
from ..ledger import reserve
from .certify import verify,verify_intervals
POLICIES=["coordinate","random_flat","circuit","random_pivot","guided_pivot","shuffled_core","conditional_rebuild","library_ucb","library_random"]
def main():
 import modal
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
 root=pathlib.Path(__file__).resolve().parent
 image=modal.Image.debian_slim(python_version="3.11").add_local_dir(str(root),"/root/collision",copy=True)
 app=modal.App("boundforge-collision-controls")
 @app.function(image=image,cpu=1,memory=1024,timeout=120,max_containers=8,retries=0,serialized=True)
 def work(spec,seed,policies):
  import sys,random,time;sys.path.insert(0,"/root")
  from collision.search import episode
  order=list(policies);random.Random(seed+100*spec[0]+len(spec[1])).shuffle(order)
  return [episode(spec,policy,seed,1.5,certify=False)for policy in order]
 controls=[[(1,0),(0,1),(1,1),(1,2)],[(1,0),(0,1),(1,1),(1,2),(1,3)]]
 cases=[([m,c],seed)for m in [8,10,12]for c in controls for seed in range(9201,9206)]
 random.Random(51).shuffle(cases);rows=[];holds=[reserve("modal",1,"grouped CPU controls setup; actual charge unresolved")];start=time.monotonic()
 with modal.enable_output(),app.run():
  for at in range(0,len(cases),8):
   batch=cases[at:at+8];holds.append(reserve("modal",.1*len(batch),"matched controls "+str(at)+"; 120s/1CPU/1GiB maximum, no retries"))
   calls=[work.spawn(spec,seed,POLICIES)for spec,seed in batch]
   for offset,call in enumerate(calls):
    group=call.get(timeout=150)
    for r in group:
     v=time.process_time();r["check"]=verify(r["witness"]);r["second_check"]=verify_intervals(r["witness"]);r["parent_verification_cpu"]=time.process_time()-v;r["status"]="verified"
    (out/("group-"+str(at+offset)+".json")).write_text(json.dumps(group));rows.extend(group)
   print(json.dumps({"completed":len(rows),"total":270}),flush=True)
 summaries={}
 for m in [8,10,12]:
  for k in [4,5]:
   summaries[str(m)+"-"+str(k)]={}
   for policy in POLICIES:
    rr=sorted([r for r in rows if r["task"]["m"]==m and len(r["task"]["controls"])==k and r["policy"]==policy],key=lambda r:r["seed"])
    summaries[str(m)+"-"+str(k)][policy]={"values":[r["best_ratio"]for r in rr],"mean":statistics.mean(r["best_ratio"]for r in rr),"cpu":sum(r["total_cpu"]for r in rr),"proposals":sum(r["proposals"]for r in rr),"pivots":sum(r["representation_changes"]for r in rr)}
 report={"run_id":os.environ.get("GITHUB_RUN_ID"),"source_sha":os.environ.get("GITHUB_SHA"),"stage":"development_control_comparison","episodes":len(rows),"all_verified":all(r["check"]["valid"]and r["second_check"]["valid"]for r in rows),"worker_cpu":sum(r["total_cpu"]for r in rows),"parent_verification_cpu":sum(r["parent_verification_cpu"]for r in rows),"wall":time.monotonic()-start,"modal_hold_usd":4,"reservation_ids":holds,"summaries":summaries,"new_method_claim":False,"record_claim":False}
 (out/"report.json").write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
if __name__=="__main__":main()
