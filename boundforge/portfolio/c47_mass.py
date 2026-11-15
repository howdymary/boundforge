"""Frozen-witness mass LP. Standard optimization; no geometric completeness claim."""
import hashlib,json,math,os,pathlib,subprocess,sys,time,urllib.request
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"c47";OUT.mkdir(exist_ok=True)
URL="https://raw.githubusercontent.com/rpinho/math-certificates/85c4680cc57130d4e9f3f0f48643e51775cdb286/c47/round8/"
EXPECTED="1afaf5d5c8968fffd3f98cf77de4d462dd1070b9dea4ec1456dd5a91087bfb44"
Q=F("114388018195906255044427129545533845966664904690010061034899/67069990589546886330812144279013633721316147200000000000000")
def main():
 start=time.monotonic();raw=urllib.request.urlopen(URL+"certificates/final.json").read();assert hashlib.sha256(raw).hexdigest()==EXPECTED
 p=OUT/"baseline.json";p.write_bytes(raw);code=urllib.request.urlopen(URL+"verify_exact.py").read();(OUT/"primary.py").write_bytes(code)
 sub=subprocess.run([sys.executable,"-I",str(OUT/"primary.py"),str(p),"--claim",str(Q),"--out",str(OUT/"baseline-check.json")],capture_output=True,text=True,env={"PATH":os.environ["PATH"]},timeout=240);assert sub.returncode==0,sub.stdout
 doc=json.loads(raw);d=doc["measure"];pts=[tuple(map(F,p))for p in d["pts"]];boxes=[tuple(map(F,w["box"]))for w in doc["witnesses"]];px,py=F(d["Px"]),F(d["Py"])
 den=math.lcm(*(v.denominator for p in pts for v in p[:2]),px.denominator,py.denominator,*(v.denominator for b in boxes for v in b))
 x=np.array([int(p[0]*den)for p in pts],dtype=np.int64);y=np.array([int(p[1]*den)for p in pts],dtype=np.int64);P=int(px*den);R=int(py*den)
 assert max(abs(int(v*den)) for b in boxes for v in b)<2**60
 A=np.zeros((len(boxes),len(pts)),dtype=np.int16)
 for i,(a,b,c,e) in enumerate(boxes):
  a,b,c,e=[int(v*den)for v in [a,b,c,e]]
  nx=np.maximum(0,(b-x)//P+(x-a)//P+1);ny=np.maximum(0,(e-y)//R+(y-c)//R+1)
  assert (nx*ny).max()<32768;A[i]=nx*ny
 mass0=sum(v[2]for v in pts);rhs=np.array([float(4*F(w["radius"])**2*F(d["lam"]))for w in doc["witnesses"]])
 opt=linprog(np.ones(len(pts)),A_ub=-A.astype(float),b_ub=-rhs,bounds=(0,None),method="highs",options={"time_limit":60,"dual_feasibility_tolerance":1e-9,"primal_feasibility_tolerance":1e-9})
 report={"run_id":os.environ["GITHUB_RUN_ID"],"source_sha":os.environ["GITHUB_SHA"],"baseline_sha256":EXPECTED,"primary_checker_sha256":hashlib.sha256(code).hexdigest(),"baseline_periodic_ratio":str(Q),"source":URL,"lp_success":bool(opt.success),"status":str(opt.message),"n":len(pts),"constraints":len(boxes),"scope":"Exact periodic-incumbent replay followed by standard LP on fixed rectangle family. Numerical screen is not new-record acceptance."}
 if opt.success:
  # Freeze candidate heights, then repair all mass inequalities with exact scalars.
  masses=[F(max(0,int(round(v*10**17))),10**17)for v in opt.x]
  factor=F(1);totals=[]
  for i,w in enumerate(doc["witnesses"]):
   s=sum(int(A[i,j])*masses[j]for j in np.flatnonzero(A[i]));assert s>0
   need=4*F(w["radius"])**2*F(d["lam"]);factor=max(factor,need/s)
  factor*=1+F(1,10**14);masses=[m*factor for m in masses]
  newmass=sum(masses);ratio=Q*mass0/newmass
  report.update({"numerical_mass":float(opt.fun),"old_mass":str(mass0),"exact_repair_factor":str(factor),"repaired_mass":str(newmass),"repaired_periodic_ratio":str(ratio),"ratio_float":float(ratio),"gain_float":float(ratio-Q),"passes_promising_gate":ratio>Q+F(1,10**9)})
  if report["passes_promising_gate"]:
   doc["measure"]["pts"]=[[str(a),str(b),str(m)]for (a,b,_),m in zip(pts,masses)if m>0];candidate=OUT/"candidate.json";candidate.write_text(json.dumps(doc))
   sub=subprocess.run([sys.executable,"-I",str(OUT/"primary.py"),str(candidate),"--claim",str(ratio),"--out",str(OUT/"candidate-primary-check.json")],capture_output=True,text=True,env={"PATH":os.environ["PATH"]},timeout=240)
   report["candidate_primary_pass"]=sub.returncode==0;report["requires_independent_checker"]=True
 report["seconds"]=time.monotonic()-start;(OUT/"report.json").write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=="__main__":main()
