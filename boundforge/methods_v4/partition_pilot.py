"""Finite-objective development comparison; no confirmatory or novelty claim."""
import argparse,itertools,json,pathlib,time
from fractions import Fraction as Q
from .partitions import compile_partitions,equality_maps
from .finite import certify,arb_values
from .masks import signatures,cone
def encode(x):
 if isinstance(x,Q):return str(x)
 if isinstance(x,dict):return {str(k):encode(v)for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [encode(v)for v in x]
 return x
def main():
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True);rows=[]
 tasks=[
 ("coordinated-private",[(0,0)],[(1,0),(0,1),(1,1)],[[Q(-3,2),0,1],[0,Q(-3,2),1]]),
 ("negative-Shannon",[(0,0)],[(1,0),(0,1),(1,-1)],[[-2,-2,1]]),
 ("old-mass-redistribution",[(0,),(1,)],[(1,)],[[-1]]),
 ("three-dimensional",[(0,0,0)],[(1,0,0),(0,1,0),(0,0,1),(1,1,1)],[[-1,-1,0,2],[0,-1,-1,2]])]
 for name,old,forms,margins in tasks:
  start=time.process_time();c=compile_partitions(old,forms,2,max_flats=12000);base=[Q(1,len(old))]*len(old)+[Q(0)]*2;polys=[[p,-p]for p in base[:-2]]+[[0,Q(1,2)],[0,Q(1,2)]]
  evaluated=0;best=None
  for maps,item in c["partitions"].items():
   for e in [Q(1,16),Q(1,64),Q(1,256)]:
    probs=[Q(p[0])+Q(p[1])*e for p in polys];before=arb_values(base,maps,margins,256);after=arb_values(probs,maps,margins,256);score=min(float(x-y)for x,y in zip(after,before));evaluated+=1
    if best is None or score>best["score"]:best={"score":score,"maps":maps,"new_points":item["new_points"],"epsilon":e}
  verification=certify(polys,best["maps"],margins,best["epsilon"],512)
  rows.append({"task":name,"partition_count":len(c["partitions"]),"complete_geometry":c["complete"],"flat_count":c["flats"],"equations":c["equations"],"geometry_cpu":c["cpu"],"finite_evaluations":evaluated,"best":best,"independent_finite_check":verification,"total_cpu":time.process_time()-start})
  (out/"tasks.json").write_text(json.dumps(encode(rows),indent=2))
 # Directly expose information discarded by a per-atom novelty mask.
 old=[(0,0)];forms=[(1,0),(0,1),(1,1)];program=[[1,-1],[0,Q(1,2)],[0,Q(1,2)]];margins=[[0,0,1]]
 pairs=[[(1,0),(0,1)],[(1,0),(0,2)]]
 controls=[certify(program,equality_maps(old,pair,forms),margins,Q(1,64),512)for pair in pairs]
 (out/"same-mask-counterexample.json").write_text(json.dumps({"pairs":pairs,"checks":controls,"claim":"The new atoms have the same novelty masks in both pairs, but target-image collisions and finite entropy differ. This is a representation limitation, not a new entropy identity."},indent=2))
 report={"tasks":len(rows),"complete_geometries":sum(r["complete_geometry"]for r in rows),"verified_positive":sum(r["independent_finite_check"]["strict_all_margins"]for r in rows),"cpu":sum(r["total_cpu"]for r in rows),"source_of_geometry":"standard exact affine arrangement traversal","new_method_claim":False,"claim_limit":"Fixed k=2, equal added weights, three epsilon values. Complete geometry does not establish global weight/epsilon optimization. Development only."}
 (out/"report.json").write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
if __name__=="__main__":main()
