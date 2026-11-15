"""Bounded two-coordinate construction pilot; no numeric record acceptance."""
import hashlib,itertools,json,math,os,pathlib,random,subprocess,time
import numpy as np
from scipy.optimize import minimize
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"block2";OUT.mkdir(exist_ok=True)
def semigroup2(gens,B):
 present={(0,0)}
 for a in range(B+1):
  for b in range(B+1):
   if (a,b) in present:
    for c,d in gens:
     if a+c<=B and b+d<=B:present.add((a+c,b+d))
 return sorted(present)
def optimize(h):
 costs=np.arange(len(h["minus"]));minus=np.array(h["minus"]);plus=np.array(h["plus"])
 def fn(z):
  u,v=z;wx=minus*np.exp(u*costs);Z=wx.sum();mu=wx@costs/Z;var=wx@(costs*costs)/Z-mu*mu;wy=plus*np.exp(v*costs);P=wy.sum();nu=wy@costs/P
  rho=np.log(Z)-mu*u;sigma=np.log(P)-mu*v;value=rho/sigma
  g=np.array([var*(rho*v-sigma*u)/sigma**2,-rho*(nu-mu)/sigma**2])
  return -value,-g
 best=None
 for start in [(.815,.8514),(.9,.925)]:
  r=minimize(fn,np.log(start),jac=True,method="L-BFGS-B",bounds=[(-2,-.0001)]*2,options={"maxiter":100,"ftol":1e-14,"gtol":1e-10})
  if best is None or -r.fun>best["score"]:best={"score":-float(r.fun),"x":float(np.exp(r.x[0])),"y":float(np.exp(r.x[1])),"status":str(r.message),"evaluations":r.nfev}
 return best
def main():
 start=time.monotonic();B=80;rng=random.Random(14531);subprocess.run(["g++","-O3","-std=c++17",str(HERE/"block2_hist.cpp"),"-o",str(OUT/"hist")],check=True)
 proc=subprocess.Popen([str(OUT/"hist")],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True,bufsize=1);seen=set();rows=[];best=None
 def attempt(points,label):
  nonlocal best
  if time.monotonic()-start>175:return False
  points=sorted(set(points));digest=hashlib.sha256(json.dumps(points).encode()).hexdigest()
  if digest in seen:return True
  seen.add(digest);proc.stdin.write(str(B)+" "+str(len(points))+"\n"+"\n".join(str(a)+" "+str(b) for a,b in points)+"\n");proc.stdin.flush();h=json.loads(proc.stdout.readline());r=optimize(h);r.update(label=label,points=len(points),hash=digest,elapsed=time.monotonic()-start);rows.append(r)
  if best is None or r["score"]>best["score"]:
   best=r|{"alphabet":points,"histogram":h};(OUT/"best.json").write_text(json.dumps(best,indent=2));print("BLOCK2_BEST "+json.dumps(r),flush=True)
  (OUT/"runs.json").write_text(json.dumps(rows));return True
 axis=[(4,0),(5,0),(0,4),(0,5)];base=semigroup2(axis,B);attempt(base,"product <4,5> x <4,5>")
 # Verify exact product histograms against independent 1D combinatorial counts.
 pbase=best.copy();one=sorted({a for a,b in base});s={a+b for a in one for b in one};cost={}
 for a in one:
  for b in one:cost[a-b]=min(cost.get(a-b,10**9),a+b)
 hm=np.bincount(list(cost.values()),minlength=2*B+1);hp=np.bincount(list(s),minlength=2*B+1)
 assert np.array_equal(np.convolve(hm,hm),np.array(best["histogram"]["minus"])) and np.array_equal(np.convolve(hp,hp),np.array(best["histogram"]["plus"]))
 cross=[(a,b) for a in range(1,12) for b in range(1,12) if a not in one or b not in one];rng.shuffle(cross)
 for g in cross[:90]:
  if not attempt(semigroup2(axis+[g],B),"cross generator "+str(g)):break
 for _ in range(100):
  g=rng.sample(cross,2)
  if not attempt(semigroup2(axis+g,B),"two cross generators "+str(g)):break
 for _ in range(120):
  gens=rng.sample(axis,3)+rng.sample(cross,2)
  if not attempt(semigroup2(gens,B),"replaced axis generator "+str(gens)):break
 # Target low sum vectors and remove complementary points coherently.
 low=sorted({a+b for a in one for b in one if a+b<=25});targets=[p for p in itertools.product(low,repeat=2) if p!=(0,0)];rng.shuffle(targets)
 for j,target in enumerate(targets[:160]):
  points=set(base);u,v=target
  for a,b in sorted(base,key=lambda p:rng.random()):
   c,d=u-a,v-b
   if (a,b) not in points or (c,d) not in points:continue
   if (a,b)==(0,0):points.discard((c,d))
   elif (c,d)==(0,0):points.discard((a,b))
   elif rng.random()<.5:points.discard((a,b))
   else:points.discard((c,d))
  if not attempt(points,"coordinated removal of sum "+str(target)):break
 proc.stdin.close();proc.wait(timeout=10)
 report={"run_id":os.environ["GITHUB_RUN_ID"],"source_sha":os.environ["GITHUB_SHA"],"cases":len(rows),"elapsed_seconds":time.monotonic()-start,"baseline_score":pbase["score"],"best_score":best["score"],"new_record":False,"passes_promising_screen":best["score"]>1.272558052,"best_label":best["label"],"scope":"Exact finite histograms with floating entropy optimization only. Product identity checked. New integer-label encoding and finite-type certificate required for acceptance; no symmetry or semigroup completeness claim."}
 (OUT/"report.json").write_text(json.dumps(report,indent=2));print("BLOCK2_FINAL "+json.dumps(report),flush=True)
if __name__=="__main__":main()
