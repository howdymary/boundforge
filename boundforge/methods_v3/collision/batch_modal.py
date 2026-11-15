"""Development timing and CPU-matched search for shared exact repair."""
import argparse,json,os,pathlib,random,statistics,time
from ..ledger import reserve
from .certify import verify,verify_intervals
def main():
 import modal
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
 root=pathlib.Path(__file__).resolve().parent;image=modal.Image.debian_slim(python_version="3.11").add_local_dir(str(root),"/root/collision",copy=True);app=modal.App("boundforge-shared-repair-development")
 @app.function(image=image,cpu=1,memory=1024,timeout=180,max_containers=8,retries=0,serialized=True)
 def benchmark(spec,seed):
  import sys,time,random;sys.path.insert(0,"/root")
  from collision.linear import Problem
  from collision.search import propose,sample_row
  from collision.batch import best_repair
  p=Problem(*spec);state=p.initial;rng=random.Random(seed)
  for _ in range(5):state,_=propose(p,state,"circuit",rng)
  row,trial=sample_row(p,state,rng);assert trial is not None
  order=[True,False];random.Random(seed).shuffle(order);results={}
  for shared in order:
   begin=time.process_time();candidate,event=best_repair(p,state,row,trial,shared);results[str(shared)]={"cpu":time.process_time()-begin,"flat":candidate.key(),"event":event}
  assert results["True"]["flat"]==results["False"]["flat"]
  assert results["True"]["event"]["counterfactual_records"]==results["False"]["event"]["counterfactual_records"]
  return {"spec":spec,"seed":seed,"basis":state.ids,"new_row":row,"results":results,"exact_equality":True}
 @app.function(image=image,cpu=1,memory=1024,timeout=120,max_containers=8,retries=0,serialized=True)
 def search(spec,seed):
  import sys,random;sys.path.insert(0,"/root")
  from collision.search import episode
  policies=["batch_repair","naive_best_repair","circuit","coordinate"];random.Random(seed+spec[0]).shuffle(policies)
  return [episode(spec,p,seed,2,certify=False)for p in policies]
 controls=[[(1,0),(0,1),(1,1),(1,2)],[(1,0),(0,1),(1,1),(1,2),(1,3)]]
 timingcases=[([m,c],9411)for m in [6,10,14,18]for c in controls]
 cases=[([m,c],seed)for m in [8,12,16]for c in controls for seed in range(9401,9406)];random.Random(672).shuffle(cases);rows=[];timings=[];holds=[reserve("modal",1,"shared-repair CPU setup")];start=time.monotonic()
 with modal.enable_output(),app.run():
  holds.append(reserve("modal",.3*len(timingcases),"complete paired evaluation timing;180s/1CPU/1GiB max per case, no retries"))
  calls=[benchmark.spawn(*x)for x in timingcases]
  for i,call in enumerate(calls):
   r=call.get(timeout=210);timings.append(r);(out/("timing-"+str(i)+".json")).write_text(json.dumps(r))
  for at in range(0,len(cases),8):
   batch=cases[at:at+8];holds.append(reserve("modal",.1*len(batch),"shared versus naive best repair and fixed controls;120s/1CPU/1GiB maximum per group"))
   calls=[search.spawn(*spec)for spec in batch]
   for i,call in enumerate(calls):
    group=call.get(timeout=150)
    for r in group:
     begin=time.process_time();r["check"]=verify(r["witness"]);r["second_check"]=verify_intervals(r["witness"]);r["parent_verification_cpu"]=time.process_time()-begin
    (out/("group-"+str(at+i)+".json")).write_text(json.dumps(group));rows.extend(group)
   print(json.dumps({"completed":len(rows),"total":120}),flush=True)
 summary={}
 for m in [8,12,16]:
  for k in [4,5]:
   summary[str(m)+"-"+str(k)]={}
   for policy in ["batch_repair","naive_best_repair","circuit","coordinate"]:
    rr=sorted([r for r in rows if r["task"]["m"]==m and len(r["task"]["controls"])==k and r["policy"]==policy],key=lambda r:r["seed"])
    summary[str(m)+"-"+str(k)][policy]={"values":[r["best_ratio"]for r in rr],"mean":statistics.mean(r["best_ratio"]for r in rr),"cpu":sum(r["total_cpu"]for r in rr),"proposals":sum(r["proposals"]for r in rr),"repair_subsets_checked":sum(r["repair_subsets_checked"]for r in rr)}
 report={"run_id":os.environ.get("GITHUB_RUN_ID"),"source_sha":os.environ.get("GITHUB_SHA"),"stage":"development","episodes":len(rows),"all_verified":all(r["check"]["valid"]and r["second_check"]["valid"]for r in rows),"worker_search_total_cpu":sum(r["total_cpu"]for r in rows),"timing_cpu":sum(z["cpu"]for r in timings for z in r["results"].values()),"wall":time.monotonic()-start,"timing_pairs":[{"spec":r["spec"],"naive_cpu":r["results"]["False"]["cpu"],"shared_cpu":r["results"]["True"]["cpu"],"ratio":(r["results"]["False"]["cpu"]/r["results"]["True"]["cpu"]if r["results"]["True"]["cpu"]>0 else None),"subsets":r["results"]["True"]["event"]["repair_subsets_checked"],"exact_equality":r["exact_equality"]}for r in timings],"summaries":summary,"unresolved_modal_hold_usd":6.4,"reservation_ids":holds,"method_claim":False,"record_claim":False}
 (out/"report.json").write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
if __name__=="__main__":main()
