"""Counterfactual: strongest existing conventional solver, with and without top addition."""
import argparse,copy,hashlib,json,os,pathlib,time
from fractions import Fraction as Q
from boundforge.methods_v3.ledger import reserve
from .adaptive_log import certificate_bounds
def main():
 import modal
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True);root=pathlib.Path("boundforge")
 base=json.loads((root/"results/best.json").read_bytes())
 from boundforge.precision import proposals
 options,nu=proposals(base);top=options[0]
 image=modal.Image.debian_slim(python_version="3.11").pip_install("mpmath==1.3.0")
 for name in ["__init__.py","precision.py"]:image=image.add_local_file(str(root/name),"/root/boundforge/"+name,copy=True)
 app=modal.App("boundforge-v4-conventional-counterfactual")
 @app.function(image=image,cpu=1,memory=2048,timeout=140,max_containers=2,retries=0,serialized=True)
 def solve(c,addition):
  import sys,time;sys.path.insert(0,"/root")
  from boundforge.precision import newton
  start=time.process_time()
  try:
   candidate,info=newton(c,addition,seconds=90)
   return {"candidate":candidate,"info":info,"cpu":time.process_time()-start,"status":"candidate"}
  except Exception as e:return {"status":"failed","exception_type":type(e).__name__,"message":str(e)[:300],"cpu":time.process_time()-start}
 hold=reserve("modal",1,"v4 conventional counterfactual: 2x1CPU/2GiB max140s, no retries; image setup; unknown receipt held")
 rows=[];start=time.monotonic()
 with modal.enable_output(),app.run():
  calls=[(name,solve.spawn(base,addition))for name,addition in [("fixed_support_newton",None),("legacy_top_ranked_addition",top)]]
  for name,call in calls:
   try:r=call.get(timeout=180)
   except Exception as e:r={"status":"worker-failed","error_type":type(e).__name__}
   r["name"]=name
   if r.get("candidate"):
    lo,hi=certificate_bounds(r["candidate"],1600);blo,bhi=certificate_bounds(base,1600);r["strict_archived_improvement"]=lo>bhi;r["interval"]=list(map(str,[lo,hi]));r["improvement_interval"]=list(map(str,[lo-bhi,hi-blo]))
   rows.append(r);(out/"experiments.json").write_text(json.dumps(rows,indent=2))
 valid=[r for r in rows if r.get("strict_archived_improvement")]
 if valid:
  best=max(valid,key=lambda r:Q(r["interval"][0]));c=copy.deepcopy(best["candidate"]);lo,hi=certificate_bounds(c,1600);s=10**80;claim=Q(lo.numerator*s//lo.denominator,s);c["claimed_lower_bound"]=[claim.numerator,claim.denominator]
  from boundforge.verify import report,improves
  from boundforge.verify_independent import check
  proof=report(c);assert proof["claim_certified"] and improves(c,base);ql,qh=check(c);bl,bh=check(base);assert ql>bh
  (out/"candidate.json").write_text(json.dumps(c,indent=2));(out/"certification.json").write_text(json.dumps({"protected_arb":proof,"protected_rational_strict":True,"improvement_interval":list(map(str,[ql-bh,qh-bl])),"selected":best["name"],"new_method_claim":False,"world_record_claim":False},indent=2))
 (out/"report.json").write_text(json.dumps({"source_sha":os.environ.get("GITHUB_SHA"),"experiments":len(rows),"top_proposal":top,"valid_improvements":len(valid),"cpu":sum(r.get("cpu",0)for r in rows),"wall":time.monotonic()-start,"modal_hold":1,"reservation":hold,"unknown_receipt_held":True,"new_method_claim":False},indent=2))
if __name__=="__main__":main()
