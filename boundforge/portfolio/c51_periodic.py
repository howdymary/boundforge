"""Periodic coefficient-phase screen; numerical output is never a certificate."""
import hashlib,json,os,pathlib,time
import numpy as np
from scipy.optimize import minimize,minimize_scalar
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"c51";OUT.mkdir(exist_ok=True)
J=np.arange(-10,10);T=J*(J+1)/2;PH=J*(J-1)/2;GRID=2048
def coefficients(z,p):
 K=np.exp(z[0]);alpha=z[1];delta=np.r_[0,z[2:]]
 return K**(-T)[None,:]*np.exp(1j*(alpha*PH[None,:]+delta[(np.arange(p)[:,None]+J)%p]))
def maximum(z,p):
 C=coefficients(z,p);spec=np.zeros((p,GRID),complex);spec[:,J%GRID]=C
 vals=np.abs(np.fft.ifft(spec,axis=1)*GRID)
 return vals.max()
def polished(z,p):
 C=coefficients(z,p);spec=np.zeros((p,GRID),complex);spec[:,J%GRID]=C
 vals=np.abs(np.fft.ifft(spec,axis=1)*GRID);peaks=[]
 for m in range(p):
  inds=np.flatnonzero((vals[m]>=np.roll(vals[m],1))&(vals[m]>=np.roll(vals[m],-1)))
  for i in inds:
   theta=2*np.pi*i/GRID;step=2*np.pi/GRID
   fun=lambda t:-abs(np.sum(C[m]*np.exp(1j*J*t)))
   q=minimize_scalar(fun,bounds=(theta-step,theta+step),method="bounded",options={"xatol":1e-14})
   peaks.append({"class":m,"theta":float(q.x),"modulus":float(-q.fun)})
 return max(v["modulus"]for v in peaks),peaks
def main():
 start=time.monotonic();deadline=start+120;rng=np.random.default_rng(51301);inc=.58507881967446432084;trace=[];best=None
 for p in [1,2,3,4,5]:
  for seed in range(6 if p>1 else 1):
   z=np.r_[np.log(3.5681854310698435),3.9615431126097391,np.zeros(p-1)]
   if seed:z[2:]=rng.normal(0,.03 if seed<3 else .6,p-1)
   initial=z.copy()
   def fun(x):
    if time.monotonic()>deadline:raise TimeoutError
    if not np.log(2.5)<x[0]<np.log(5):return 100+abs(x[0])
    return maximum(x,p)
   try:
    opt=minimize(fun,z,method="Nelder-Mead",options={"maxiter":1200,"xatol":1e-10,"fatol":1e-12})
    value,peaks=polished(opt.x,p)
    row={"period":p,"seed":seed,"initial":initial.tolist(),"parameters":opt.x.tolist(),"grid_modulus":float(opt.fun),"polished_modulus":value,"beta_float":1/value,"peaks":peaks,"calls":opt.nfev,"termination":str(opt.message)}
    trace.append(row)
    if best is None or row["beta_float"]>best["beta_float"]:best=row
   except TimeoutError:trace.append({"period":p,"seed":seed,"status":"pilot deadline"});break
  if time.monotonic()>deadline:break
 report={"run_id":os.environ["GITHUB_RUN_ID"],"source_sha":os.environ["GITHUB_SHA"],"incumbent_certified_lower":str(inc),"best":best,"trace":trace,"seconds":time.monotonic()-start,"passes_promising_gate":best["beta_float"]>inc+1e-9,"scope":"Uncertified screen, periods at most 5, K in (2.5,5), truncation -10..9 and local peak polishing. No global numerical guarantee, no general-method novelty claim."}
 (OUT/"report.json").write_text(json.dumps(report,indent=2));print(json.dumps({"best":best,"seconds":report["seconds"],"passes":report["passes_promising_gate"]}))
if __name__=="__main__":main()
