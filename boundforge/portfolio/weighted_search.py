"""Structural correction: weighted digit budgets, numerical proposal only.
For cost w(a)>=0, k_-(d)=min(w(a)+w(b):a-b=d), k_+(s) similarly.
Symmetric difference type witnesses have equal budgets; the sum-envelope proof
uses k_+. Positional encoding remains carry-free in the original digit labels.
"""
import hashlib,json,math,os,pathlib,random,time
import numpy as np
from scipy.optimize import minimize
try:from .masked_search import semigroup
except ImportError:from masked_search import semigroup
HERE=pathlib.Path(__file__).resolve().parent
class Problem:
 def __init__(self,mask):
  self.mask=np.array(mask);self.size=len(mask);ii,jj=np.meshgrid(np.arange(self.size),np.arange(self.size),indexing="ij");self.i=ii.ravel();self.j=jj.ravel()
  self.d=np.array([int(a-b) for a,b in zip(self.mask[self.i],self.mask[self.j])]);self.s=self.mask[self.i]+self.mask[self.j]
  self.ds=sorted(set(self.d));self.ss=sorted(set(self.s));self.dg=[np.where(self.d==d)[0] for d in self.ds];self.sg=[np.where(self.s==s)[0] for s in self.ss]
 def fun(self,z):
  u,v=z[:2];w=np.r_[0,z[2:]];pair=w[self.i]+w[self.j]
  di=np.array([g[np.argmin(pair[g])] for g in self.dg]);si=np.array([g[np.argmin(pair[g])] for g in self.sg]);km=pair[di];kp=pair[si]
  ex=np.exp(u*km);Z=ex.sum();p=ex/Z;mu=p@km;var=p@(km*km)-mu*mu;ey=np.exp(v*kp);P=ey.sum();q=ey/P;nu=q@kp
  rho=math.log(Z)-mu*u;sigma=math.log(P)-mu*v
  if sigma<1e-10 or rho<1e-10:return 1000.,np.zeros_like(z)
  val=rho/sigma;gk=p*(-u*u*(km-mu)*sigma+rho*v*(1+u*(km-mu)))/(sigma*sigma);gs=-rho*v*q/(sigma*sigma);gw=np.zeros(self.size)
  np.add.at(gw,self.i[di],gk);np.add.at(gw,self.j[di],gk);np.add.at(gw,self.i[si],gs);np.add.at(gw,self.j[si],gs)
  grad=np.r_[var*(rho*v-sigma*u)/sigma**2,-rho*(nu-mu)/sigma**2,gw[1:]]
  return -val,-grad
def main():
 out=HERE/"weighted";out.mkdir(exist_ok=True);start=time.monotonic();rng=np.random.default_rng(1449);rows=[];best=None
 masks=[semigroup([4,5],80),semigroup([4,5],160),semigroup([3,4],80),semigroup([5,6],100)]
 for run in range(36):
  if time.monotonic()-start>180:break
  mask=masks[run%len(masks)];pr=Problem(mask);a=np.array(mask,dtype=float)
  w=a.copy()
  if run>=4:
   if run%3==0:w=a*(1+rng.normal(0,.02,size=len(a)))
   elif run%3==1:w=a+math.sqrt(run)*np.sin(a*rng.uniform(.04,.35))
   else:w=a+rng.normal(0,.3,size=len(a))
   w=np.maximum(w,.001);w[0]=0
  z=np.r_[np.log([.815,.8514]),w[1:]];calls=0;localbest=None
  def fn(v):
   nonlocal calls,localbest,best
   calls+=1
   if time.monotonic()-start>195:raise TimeoutError("global weighted pilot limit")
   value,g=pr.fun(v)
   if localbest is None or -value>localbest["score"]:
    localbest={"score":-float(value),"C3a_limit":2-1/(-float(value)) if value<0 else None,"mask":mask,"costs":[0]+list(map(float,v[2:])),"log_x":float(v[0]),"log_y":float(v[1]),"run":run,"calls":calls}
    if best is None or localbest["score"]>best["score"]:
     best=localbest.copy();(out/"best.json").write_text(json.dumps(best,indent=2));print("WEIGHT_BEST "+json.dumps({k:v for k,v in best.items() if k not in ["mask","costs"]}),flush=True)
   return value,g
  try:r=minimize(fn,z,jac=True,method="L-BFGS-B",bounds=[(-3,-.0001),(-3,-.0001)]+[(.001,2*max(mask))]*(len(mask)-1),options={"maxiter":100,"ftol":1e-12,"gtol":1e-8,"maxls":25});status=str(r.message)
  except TimeoutError as e:status=str(e)
  rows.append({"run":run,"mask_size":len(mask),"calls":calls,"best":localbest,"status":status,"elapsed":time.monotonic()-start});(out/"runs.json").write_text(json.dumps(rows))
 report={"run_id":os.environ["GITHUB_RUN_ID"],"source_sha":os.environ["GITHUB_SHA"],"elapsed_seconds":time.monotonic()-start,"runs":len(rows),"best":best,"new_record":False,"scope":"Numerical weighted-budget structural correction; no exact acceptance or claimed method novelty. Nonsmooth min-witness costs make optimizer status provisional."}
 (out/"report.json").write_text(json.dumps(report,indent=2));print("WEIGHT_FINAL "+json.dumps({k:v for k,v in report.items() if k!="best"}|{"best_score":best["score"]}),flush=True)
if __name__=="__main__":main()
