"""Numerical proposal engine for C3e/C3a. No numerical score accepts a record."""
import collections,hashlib,json,math,os,pathlib,random,time
import numpy as np
from scipy.optimize import minimize
HERE=pathlib.Path(__file__).resolve().parent
def semigroup(gens,B):
 s={0}
 for a in range(B+1):
  if a in s:s.update(a+g for g in gens if a+g<=B)
 return sorted(s)
def data(mask):
 sums=set();cost={}
 for a in mask:
  for b in mask:
   sums.add(a+b);d=a-b;c=a+b
   if c<cost.get(d,10**9):cost[d]=c
 hist=collections.Counter(cost.values())
 return np.array(sorted(sums),dtype=float),np.array(sorted(hist),dtype=float),np.array([hist[k] for k in sorted(hist)],dtype=float),cost
def optimize(mask,starts=None):
 sums,costs,mults,kappa=data(mask)
 def calc(z):
  u,v=z;wx=mults*np.exp(u*costs);Z=wx.sum();mu=np.dot(wx,costs)/Z;var=np.dot(wx,costs*costs)/Z-mu*mu
  wy=np.exp(v*sums);P=wy.sum();nu=np.dot(wy,sums)/P
  rho=math.log(Z)-mu*u;sigma=math.log(P)-mu*v
  if sigma<1e-12 or rho<1e-12:return 1e3,np.zeros(2)
  val=rho/sigma
  grad=np.array([var*(rho*v-sigma*u)/sigma**2,-rho*(nu-mu)/sigma**2])
  return -val,-grad
 best=None
 for x,y in starts or [(.815,.8514),(.93,.945)]:
  r=minimize(calc,np.log([x,y]),jac=True,method="L-BFGS-B",bounds=[(-3,-.0001),(-3,-.0001)],options={"maxiter":150,"ftol":1e-14,"gtol":1e-10})
  score=-float(r.fun)
  if best is None or score>best["score"]:best={"score":score,"C3a_limit":2-1/score,"x":float(np.exp(r.x[0])),"y":float(np.exp(r.x[1])),"optimizer_success":bool(r.success),"message":str(r.message),"function_evaluations":int(r.nfev),"mask":mask,"mask_sha256":hashlib.sha256(json.dumps(mask).encode()).hexdigest(),"sum_support":len(sums),"differences":len(kappa)}
 return best
def main():
 out=HERE/"pilot";out.mkdir(exist_ok=True);start=time.monotonic();rng=random.Random(2601114);rows=[];best=None;seen=set()
 def attempt(mask,label):
  nonlocal best
  mask=sorted(set(mask));key=tuple(mask)
  if key in seen:return
  seen.add(key);r=optimize(mask);r.update(label=label,elapsed_seconds=time.monotonic()-start);rows.append(r)
  if best is None or r["score"]>best["score"]:
   best=r;(out/"best.json").write_text(json.dumps(best,indent=2));print("MASK_BEST "+json.dumps(best),flush=True)
  (out/"runs.json").write_text(json.dumps(rows))
 attempt(semigroup([4,5],160),"reproduce baseline semigroup, optimized tilts")
 baseline=best.copy()
 pairs=[(a,b) for a in range(2,19) for b in range(a+1,32) if math.gcd(a,b)==1]
 rng.shuffle(pairs)
 for a,b in pairs:
  if time.monotonic()-start>120:break
  attempt(semigroup([a,b],160),"semigroup:"+str([a,b]))
 triples=list(__import__("itertools").combinations(range(3,19),3));rng.shuffle(triples)
 for g in triples[:300]:
  if time.monotonic()-start>150:break
  if math.gcd(math.gcd(g[0],g[1]),g[2])==1:attempt(semigroup(g,160),"semigroup:"+str(g))
 # Arbitrary masks, not an assumed semigroup completeness reduction.
 for j in range(300):
  if time.monotonic()-start>180:break
  parent=best["mask"] if j%3 else baseline["mask"];s=set(parent)
  for _ in range(1+j%3):
   q=rng.randrange(1,65)
   if q in s:s.remove(q)
   else:s.add(q)
  attempt(sorted(s),"bounded mask edit:"+str(j))
 report={"run_id":os.environ["GITHUB_RUN_ID"],"source_sha":os.environ["GITHUB_SHA"],"elapsed_seconds":time.monotonic()-start,"masks":len(rows),"baseline":baseline,"best":best,"numerical_gain_over_reoptimized_baseline":best["score"]-baseline["score"],"new_record":False,"scope":"Numerical screening only. Two-tilt optimization and finite masks are prior art; neither global optimality nor rigorous improvement is established."}
 (out/"report.json").write_text(json.dumps(report,indent=2));print("MASK_FINAL "+json.dumps(report),flush=True)
if __name__=="__main__":main()
