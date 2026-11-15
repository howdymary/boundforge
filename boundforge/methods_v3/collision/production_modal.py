"""Bounded conventional production campaign; acceptance remains on the parent."""
import argparse,copy,hashlib,json,os,pathlib,time
from fractions import Fraction as Q
from ..ledger import reserve
from boundforge.verify import report,measure
from boundforge.verify_independent import check,decimal
def main():
 import modal
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True);root=pathlib.Path(__file__).resolve().parent;source=pathlib.Path("boundforge/results/best.json").read_bytes();baseline=json.loads(source);best=copy.deepcopy(baseline);baseq=check(baseline);blo,bhi,_=measure(baseline)
 image=modal.Image.debian_slim(python_version="3.11").add_local_dir(str(root),"/root/collision",copy=True);app=modal.App("boundforge-bounded-weighted-events")
 @app.function(image=image,cpu=1,memory=1024,timeout=180,max_containers=4,retries=0,serialized=True)
 def work(certificate,seed):
  import sys;sys.path.insert(0,"/root")
  from collision.weighted_events import search
  return search(certificate,seed,60)
 holds=[reserve("modal",1,"weighted production CPU setup; charge unresolved")];results=[];start=time.monotonic()
 with modal.enable_output(),app.run():
  for at in [0,4]:
   holds.append(reserve("modal",.8,"four weighted search workers,180s/1CPU/1GiB maximum each,no retries"))
   calls=[work.spawn(best,10001+i)for i in range(at,at+4)]
   for call in calls:
    r=call.get(timeout=210);candidate=r["candidate"];validation=report(candidate);ql,qh=check(candidate);al,ah,_=measure(candidate);strict_arb=bool(al>bhi);strict_rational=ql>baseq[1];assert strict_arb==strict_rational
    r["final_validation"]={"arb":validation,"independent_ratio":[decimal(ql),decimal(qh,True)],"strict_vs_archived_arb":strict_arb,"strict_vs_archived_rational":strict_rational,"archived_sha256":hashlib.sha256(source).hexdigest()}
    if strict_rational and ql>check(best)[1]:best=copy.deepcopy(candidate)
    (out/("seed-"+str(r["seed"])+".json")).write_text(json.dumps(r));results.append({k:v for k,v in r.items()if k not in ["trace","candidate"]})
    (out/"partial-summary.json").write_text(json.dumps(results,indent=2))
 reportdata={"run_id":os.environ.get("GITHUB_RUN_ID"),"source_sha":os.environ.get("GITHUB_SHA"),"archived_incumbent_sha256":hashlib.sha256(source).hexdigest(),"stage":"production_not_method_evaluation","workers":len(results),"worker_search_cpu":sum(r["search_cpu"]for r in results),"wall":time.monotonic()-start,"modal_hold_usd":2.6,"reservation_ids":holds,"results":results,"strict_improvements_vs_archived":sum(r["final_validation"]["strict_vs_archived_rational"]for r in results),"frontier_refresh_required_before_any_record_claim":True,"world_record_claim":False,"method_claim":False}
 (out/"report.json").write_text(json.dumps(reportdata,indent=2));(out/"best-certificate.json").write_text(json.dumps(best,indent=2));print(json.dumps(reportdata),flush=True)
if __name__=="__main__":main()
