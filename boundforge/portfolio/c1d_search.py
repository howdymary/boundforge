"""Classical bounded p-norm continuation for the absolute signed objective."""
import json,math,time
import numpy as np
from scipy.fft import rfft,irfft,next_fast_len
from scipy.optimize import minimize
def evaluate(x):
 n=len(x);L=next_fast_len(2*n-1,real=True);c=irfft(rfft(x,L)**2,L)[:2*n-1];return 2*n*np.abs(c).max()/x.sum()**2
def fg(x,p,L):
 X=rfft(x,L);c=irfft(X*X,L)[:2*len(x)-1];a=np.abs(c);M=a.max();S=x.sum()
 if M==0 or S==0:return 1e10,np.zeros_like(x)
 z=a/M;power=z**(p-1);total=np.dot(power,z);val=math.log(M)+math.log(total)/p-2*math.log(abs(S));gc=np.sign(c)*power/(M*total)
 gradient=2*irfft(rfft(gc,L)*np.conj(X),L)[:len(x)]-2/S
 return val,gradient
def run(cert,spec):
 start=time.monotonic();end=start+spec["seconds"];rng=np.random.default_rng(spec["seed"]);x=np.repeat(np.array(cert["v_int"],dtype=float),spec["refine"]);n=len(x);x=x/x.sum()*(2*n);L=next_fast_len(2*n-1,real=True);initial=float(evaluate(x));best=x.copy();bv=initial;trace=[];calls=0
 if spec["kick"]:x=x+rng.normal(0,spec["kick"],n);x=x/x.sum()*(2*n)
 p=spec["p0"];status="complete"
 def keep(a):
  nonlocal best,bv
  score=float(evaluate(a))
  if score<bv:bv=score;best=a/a.sum()*(2*n)
 def fun(a):
  nonlocal calls
  calls+=1
  if time.monotonic()>end:raise TimeoutError("C1d worker deadline")
  if calls%100==0:keep(a)
  return fg(a,p,L)
 try:
  for stage in range(30):
   if p>3e12 or time.monotonic()>end:break
   r=minimize(fun,x,jac=True,method="L-BFGS-B",options={"maxiter":2500,"maxcor":20,"ftol":1e-17,"gtol":1e-300,"maxls":25})
   x=r.x/r.x.sum()*(2*n);keep(x);trace.append({"stage":stage,"p":p,"score":float(evaluate(x)),"best":bv,"calls":calls,"elapsed":time.monotonic()-start,"status":str(r.message)});p*=2
 except TimeoutError as e:status=str(e)
 scale=2.0**56/np.abs(best).max();ints=[int(v) for v in np.rint(best*scale)]
 return {"spec":spec,"initial_float":initial,"best_float":bv,"calls":calls,"trace":trace,"candidate":{"constant":"C_1d","v_int":ints},"status":status,"elapsed_seconds":time.monotonic()-start,"scope":"Numerical proposal only, conventional p-norm continuation, no new method claim."}
