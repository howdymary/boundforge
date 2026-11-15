"""Development pilot, counterfactual legacy audit, and durable certificate extraction."""
import argparse,copy,hashlib,io,itertools,json,pathlib,subprocess,time,zipfile
from fractions import Fraction as Q
from .masks import signatures,cone,dot
from .adaptive_log import certificate_bounds
def enc(x):
 if isinstance(x,Q):return str(x)
 if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [enc(v) for v in x]
 if isinstance(x,set):return sorted(map(str,x))
 return x
def main():
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);args=p.parse_args();out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
 def save(name,data):(out/name).write_text(json.dumps(enc(data),indent=2))
 fixtures=[
 ("coordinated",[(0,0)],[(1,1),(1,0),(0,1)],[[1,Q(-3,2),0],[1,0,Q(-3,2)]],(0,)),
 ("negative",[(0,0)],[(1,-1),(1,0),(0,1)],[[1,-2,-2]],(0,)),
 ("three-dimensional",[(0,0,0),(1,2,3)],[(1,0,0),(0,1,0),(0,0,1),(1,1,1),(1,-1,1)],[[0,-1,-1,2,0],[0,-1,-1,0,2]],()),
 ("dependent-rational",[(Q(1,3),Q(2,5)),(1,2)],[(1,0),(0,1),(1,1),(2,2),(0,0)],[[1,1,-1,0,0]],())]
 rows=[]
 for name,pts,forms,margins,req in fixtures:
  a=signatures(pts,forms,req);c=cone(a["masks"],margins);rows.append({"name":name,"geometry":a,"cone":c})
 save("oracle-development.json",rows)
 # Legacy counterfactual: determine whether the conventional proposer already covered the atom.
 base=json.loads(pathlib.Path("boundforge/results/best.json").read_bytes())
 from boundforge.precision import proposals
 t=time.process_time();opts,nu=proposals(base,limit=10000)
 target=[o for o in opts if o["law"]==1 and o["point"]==[11,-9]]
 save("legacy-counterfactual.json",{"candidate":[1,[11,-9]],"rank_1based":next((i+1 for i,o in enumerate(opts)if o in target),None),"eligible_options":len(opts),"default_top8":opts[:8],"target_option":target,"dual":nu,"cpu":time.process_time()-t,"note":"Eligibility/shortlist only; this does not establish that the earlier Newton solver could find this candidate or that it had been executed."})
 # Read immutable previous run artifacts into remote output; no local host project files.
 artifact=14179131546
 raw=subprocess.check_output(["gh","api","repos/howdymary/boundforge/actions/artifacts/"+str(artifact)+"/zip"])
 z=zipfile.ZipFile(io.BytesIO(raw))
 for name in ["candidate.json","decisions.json","report.json"]:
  item=next(x for x in z.namelist()if x.rsplit("/",1)[-1]==name);(out/("support-original-"+name)).write_bytes(z.read(item))
 c=json.loads((out/"support-original-candidate.json").read_bytes());lo,hi=certificate_bounds(c,1300);S=10**80;claim=Q(lo.numerator*S//lo.denominator,S);c["claimed_lower_bound"]=[claim.numerator,claim.denominator];save("candidate.json",c)
 # Both existing acceptance implementations, unchanged, independently resolve strict improvement.
 from boundforge.verify import report,improves
 from boundforge.verify_independent import check
 start=time.process_time();arb=report(c);assert arb["claim_certified"] and improves(c,base)
 qlo,qhi=check(c);blo,bhi=check(base);assert qlo>bhi
 save("final-certification.json",{"protected_arb":arb,"strict_arb":True,"strict_original_rational":qlo>bhi,"ratio_interval":[qlo,qhi],"baseline_interval":[blo,bhi],"improvement_interval":[qlo-bhi,qhi-blo],"cpu":time.process_time()-start,"protected_hashes":{name:hashlib.sha256(pathlib.Path("boundforge/"+name).read_bytes()).hexdigest()for name in ["verify.py","verify_independent.py"]},"world_record_claim":False,"method_novelty_claim":False})
 print(json.dumps({"fixtures":len(rows),"legacy_target_rank":next((i+1 for i,o in enumerate(opts)if o in target),None),"two_original_checkers_passed":True}),flush=True)
if __name__=="__main__":main()
