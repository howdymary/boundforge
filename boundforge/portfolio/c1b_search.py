"""Bounded C1b numerical continuation. Existing standard method, no novelty claim."""
import json,math,time
import numpy as np
from scipy.optimize import minimize
from scipy.signal import fftconvolve
def project(a):
 low=-1.;high=1.
 for _ in range(48):
  shift=(low+high)/2;s=np.clip(a+shift,0,1).sum()
  if s<len(a)/2:low=shift
  else:high=shift
 return np.clip(a+(low+high)/2,0,1)
def values(a):return (fftconvolve(a,np.ones(len(a)))-fftconvolve(a,a[::-1]))*(2/len(a))
def soft(a,beta,dual=0,penalty=1e4):
 n=len(a);w=2/n;C=values(a);m=C.max();e=np.exp(beta*(C-m));p=e/e.sum();value=m+math.log(e.sum())/beta
 pref=np.r_[0,np.cumsum(p)];g1=pref[n:]-pref[:-n];g2=fftconvolve(p,a)[n-1:2*n-1];g3=fftconvolve(p[::-1],a)[n-1:2*n-1]
 residual=w*a.sum()-1;gradient=w*(g1-g2-g3)+(dual+2*penalty*residual)*w
 return value+dual*residual+penalty*residual**2,gradient
def quantize(a):
 n=len(a);Q=1<<50;k=[min(Q,max(0,int(round(float(v)*Q)))) for v in a];delta=n*Q//2-sum(k)
 # Unit adjustments distribute rounding repair rather than one large perturbation.
 sign=1 if delta>0 else -1;remaining=abs(delta)
 for i in range(n):
  if not remaining:break
  if (sign>0 and k[i]<Q) or (sign<0 and k[i]>0):k[i]+=sign;remaining-=1
 if remaining:
  for i in range(n):
   change=min(remaining,Q-k[i] if sign>0 else k[i]);k[i]+=sign*change;remaining-=change
   if not remaining:break
 assert sum(k)*2==n*Q
 return {"n":n,"Q":Q,"heights_int":k}
def run(cert,spec):
 start=time.monotonic();deadline=start+spec["seconds"];rng=np.random.default_rng(spec["seed"])
 a=np.repeat(np.array(cert["heights_int"],dtype=float)/cert["Q"],spec["refine"]);n=len(a)
 if spec.get("kick",0):a=project(np.clip(a+rng.normal(0,spec["kick"],n)*(a>0)*(a<1),0,1))
 initial=float(values(a).max());best=a.copy();score=initial;x=a.copy();calls=0;dual=0.;beta=spec["beta"];trace=[];status="complete"
 def retain(candidate):
  nonlocal best,score
  candidate=project(candidate);s=float(values(candidate).max())
  if s<score:best=candidate.copy();score=s
 def fun(candidate):
  nonlocal calls
  calls+=1
  if time.monotonic()>deadline:raise TimeoutError("bounded continuation deadline")
  if calls%40==0:retain(candidate)
  return soft(candidate,beta,dual)
 try:
  for stage in range(20):
   if beta>1e12 or time.monotonic()>deadline:break
   for outer in range(5):
    result=minimize(fun,x,jac=True,method="L-BFGS-B",bounds=[(0,1)]*n,options={"maxiter":2500,"maxcor":30,"ftol":1e-18,"gtol":1e-14,"maxls":30})
    x=result.x;residual=2*x.sum()/n-1;dual+=2e4*residual;retain(x)
    if abs(residual)<1e-13:break
   trace.append({"stage":stage,"beta":beta,"best_float":score,"raw_score":float(values(x).max()),"mass_residual":float(residual),"calls":calls,"elapsed":time.monotonic()-start});beta*=spec["factor"]
 except TimeoutError as e:status=str(e)
 candidate=quantize(best)
 return {"spec":spec,"initial_float":initial,"best_float":score,"float_gain":initial-score,"calls":calls,"trace":trace,"status":status,"elapsed_seconds":time.monotonic()-start,"candidate":candidate,"scope":"Numerical proposal; independently exact verification determines acceptance."}
