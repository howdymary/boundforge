
"""Numerical disk-automorphism extension. No float result is a record."""
import json,time,os,pathlib
import numpy as np
from scipy.optimize import minimize
from scipy.signal import lfilter
HERE=pathlib.Path(__file__).resolve().parent
OUT=HERE/"c59";OUT.mkdir(exist_ok=True)
N=40;r=.302825279492
rs=r**np.arange(N+1);weights=np.outer(rs,rs)
def coeff(t,a,b,S=None):
 U=(1+a)*(1-b)*np.array([[1.,-1.],[1.,-1.]])
 V=np.array([[1+a*b,a+b],[a+b,1+a*b]])
 P=U+1j*t*V;Q=V+1j*t*U
 p,q=(P,Q) if S is None else (S*Q-P,S*Q+P)
 c=np.zeros((N+1,N+1),complex)
 for j in range(N+1):
  inp=np.zeros(N+1,complex)
  if j<2:inp[:2]=p[j,:]
  if j:inp-=q[1,0]*c[j-1,:]+q[1,1]*np.r_[0,c[j-1,:-1]]
  c[j,:]=lfilter([1],[q[0,0],q[0,1]],inp)
 return c
def criterion(z):
 t=np.exp(z[0]);a,b=np.tanh(z[1:]);c=coeff(t,a,b)
 return float(np.sum(np.abs(c)*weights)-abs(c[0,0])-c[0,0].real)
def main():
 start=time.monotonic();deadline=start+120
 rng=np.random.default_rng(5901)
 base=[np.log(3067398171/2500000000),0,0]
 bv=criterion(base);best=np.array(base);trace=[]
 def fun(z):
  if time.monotonic()>deadline:raise TimeoutError
  return -criterion(z)
 try:
  for i in range(14):
   z=base if i==0 else np.array(base)+rng.normal(0,.3 if i<7 else .8,3)
   opt=minimize(fun,z,method="Nelder-Mead",options={"maxiter":700,"xatol":2e-10,"fatol":1e-14})
   v=criterion(opt.x)
   trace.append({"start":i,"variables":opt.x.tolist(),"criterion":v,"calls":opt.nfev,"termination":str(opt.message)})
   if v>bv:bv=v;best=opt.x
 except TimeoutError:trace.append({"status":"120 second pilot deadline"})
 t=np.exp(best[0]);a,b=np.tanh(best[1:]);S=10**8
 c=coeff(t,a,b,S)
 report={"run_id":os.environ["GITHUB_RUN_ID"],"source_sha":os.environ["GITHUB_SHA"],"incumbent_radius":str(r),"N":N,"baseline_herglotz_excess":criterion(base),"best_herglotz_excess":bv,"best":{"t":float(t),"a":float(a),"b":float(b),"S":S},"finite_schur_majorant_float":float(np.sum(np.abs(c)*weights)),"trace":trace,"seconds":time.monotonic()-start,"scope":"Numerical screen only. Disk automorphism preserves Schur property. Herglotz criterion is limiting guidance, not a finite certificate. No new-record acceptance."}
 (OUT/"report.json").write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=="__main__":main()
