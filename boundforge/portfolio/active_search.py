"""Standard active-knot sequential LP with coarse perturbations, bounded worker."""
import time,math
import numpy as np
from scipy.fft import rfft,irfft,next_fast_len
from scipy.optimize import linprog
def run(cert,spec):
 start=time.monotonic();end=start+spec["seconds"];n=len(cert["v_int"]);x=np.array(cert["v_int"],float);x=x/x.sum()*n;L=next_fast_len(2*n-1,real=True);B=spec["blocks"];edges=np.linspace(0,n,B+1,dtype=int);lengths=np.diff(edges);trace=[];best=x.copy()
 def conv(a,b):return irfft(rfft(a,L)*rfft(b,L),L)[:2*n-1]
 c=conv(x,x);initial=2*np.abs(c).max()/n;bv=initial;radius=spec["radius"]
 nonneg=cert["constant"]=="C_1a"
 for iteration in range(12):
  if time.monotonic()>end-15:break
  c=conv(x,x);peak=np.abs(c).max();idx=np.argpartition(np.abs(c),-min(2048,len(c)))[-min(2048,len(c)):]
  pref=np.r_[0,np.cumsum(x)]
  cutstatus=[];sol=None
  bounds=[(-radius,radius)]*B
  if nonneg:
   bounds=[(max(-radius,-x[edges[j]:edges[j+1]].min()),radius)for j in range(B)]
  for cut in range(5):
   if time.monotonic()>end-15:break
   idx=np.unique(idx);sg=np.sign(c[idx]);sg[sg==0]=1
   A=2*(pref[np.clip(idx[:,None]-edges[:-1][None,:]+1,0,n)]-pref[np.clip(idx[:,None]-edges[1:][None,:]+1,0,n)])
   # Normalize all constraints by n. Delta variable is change from peak/n.
   eq=np.r_[lengths/n,0.][None,:]
   Aub=np.column_stack((sg[:,None]*A/n,-np.ones(len(idx))))
   rhs=(peak-sg*c[idx])/n
   opt=linprog(np.r_[np.zeros(B),1.],A_ub=Aub,b_ub=rhs,A_eq=eq,b_eq=[0],bounds=bounds+[(None,None)],method="highs",options={"time_limit":min(25,max(.1,end-time.monotonic()-10)),"dual_feasibility_tolerance":1e-9,"primal_feasibility_tolerance":1e-9})
   if not opt.success:cutstatus.append({"cut":cut,"status":str(opt.message)});break
   h=np.repeat(opt.x[:-1],lengths);linear=c+2*conv(x,h);viol=np.flatnonzero(np.abs(linear)>peak+n*opt.x[-1]+1e-8)
   cutstatus.append({"cut":cut,"constraints":len(idx),"violations":len(viol),"predicted_score":2*(peak/n+opt.x[-1])})
   sol=h
   if not len(viol):break
   if len(viol)>2048:viol=viol[np.argsort(np.abs(linear[viol]))[-2048:]]
   idx=np.r_[idx,viol]
  if sol is None:break
  cross=2*conv(x,sol);quad=conv(sol,sol);chosen=None
  for alpha in [1.,.5,.25,.125,.0625,.03125,.015625]:
   cand=x+alpha*sol
   if nonneg and cand.min()<-1e-11:continue
   cc=c+alpha*cross+alpha*alpha*quad;score=2*np.abs(cc).max()/n
   if score<bv:
    bv=float(score);best=cand.copy();chosen=alpha
  trace.append({"iteration":iteration,"radius":radius,"best":bv,"alpha":chosen,"cuts":cutstatus,"elapsed":time.monotonic()-start})
  if chosen is None:
   radius*=.2
   if radius<1e-9:break
  else:x=best.copy()
 scale=2**56/np.max(np.abs(best));ints=[int(v)for v in np.rint(best*scale)]
 if nonneg:ints=[max(0,v)for v in ints]
 return {"spec":spec,"initial_float":float(initial),"best_float":bv,"trace":trace,"elapsed_seconds":time.monotonic()-start,"candidate":{"constant":cert["constant"],"v_int":ints},"scope":"Conventional sequential linear programming; full FFT screen then independent exact certification. No novelty or local-optimality claim."}
