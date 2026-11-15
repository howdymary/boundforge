"""Credential-free proposal worker: no repository imports, certificates or answers."""
import json,math,sys,time,resource
import numpy as np
from scipy.optimize import minimize,minimize_scalar
import mpmath as mp
def float_peaks(K,a,N=16):
 n=np.arange(N+1);T=n*(n+1)/2;k=2*n+1;c=2*K**(-T)*np.exp(1j*a*T)
 grid=np.linspace(0,np.pi/2,1025);vals=np.abs(c@np.cos(np.outer(k,grid)))
 inds=np.flatnonzero((vals[1:-1]>=vals[:-2])&(vals[1:-1]>=vals[2:]))+1
 peaks=[(0.,float(abs(c.sum()))),(np.pi/2,float(abs(np.dot(c,np.cos(k*np.pi/2)))))]
 for i in inds:
  fn=lambda t:-abs(np.dot(c,np.cos(k*t)))
  q=minimize_scalar(fn,bounds=(grid[i-1],grid[i+1]),method="bounded",options={"xatol":1e-14})
  peaks.append((float(q.x),float(-q.fun)))
 return sorted(peaks,key=lambda z:-z[1])
def float_local(req):
 K=float(req["incumbent"]["K"]);a=float(req["incumbent"]["alpha"]);start=time.monotonic();deadline=start+req["seconds"];rng=np.random.default_rng(req["seed"])
 base=float_peaks(K,a);baseline=1/base[0][1];best=(baseline,K,a);calls=0
 z0=np.array([math.log(K),a])
 if req.get("restart"):z0+=rng.normal(0,1e-6,2)
 def fun(z):
  nonlocal best,calls
  calls+=1
  if time.monotonic()>deadline:raise TimeoutError
  k=math.exp(z[0])
  if not 2<k<6:return 100
  p=float_peaks(k,z[1]);b=1/p[0][1]
  if b>best[0]:best=(b,k,float(z[1]))
  return -b
 try:r=minimize(fun,z0,method="Nelder-Mead",options={"maxiter":400,"xatol":1e-12,"fatol":1e-16});status=str(r.message)
 except TimeoutError:status="bounded deadline"
 candidate={"name":"double-precision proposal, not certified","K":repr(best[1]),"alpha":repr(best[2]),"lower_bound":format(best[0],".18f"),"N":12}
 inside=[t for t,v in base if 1e-5<t<math.pi/2-1e-5]
 return {"status":"proposal","candidate":candidate,"baseline_test_theta":repr(inside[0]if inside else 0.),"operator":"float_local","baseline_beta":repr(baseline),"best_beta":repr(best[0]),"gain":repr(best[0]-baseline),"ulp":repr(math.ulp(baseline)),"parameters":{"K":repr(best[1]),"alpha":repr(best[2])},"peaks":[{"theta":t,"modulus":v}for t,v in base],"calls":calls,"termination":status}
def square(K,a,t,N):
 P=mp.mpc(0);dk=mp.mpc(0);da=mp.mpc(0);dt=mp.mpc(0)
 for n in range(N+1):
  T=n*(n+1)//2;k=2*n+1;c=2*mp.exp(1j*a*T)*K**(-T);v=c*mp.cos(k*t)
  P+=v;dk-=T*v/K;da+=1j*T*v;dt-=k*c*mp.sin(k*t)
 return tuple(2*mp.re(mp.conj(P)*v)for v in [P/2,dk,da,dt])
def precision(req):
 mp.mp.dps=req.get("precision",100);N=20;inc=req["incumbent"];K0=mp.mpf(inc["K"]);a0=mp.mpf(inc["alpha"])
 peaks=float_peaks(float(K0),float(a0));inside=[x for x in peaks if 1e-5<x[0]<math.pi/2-1e-5]
 if not inside:return {"status":"optimizer_failure","reason":"no interior peak found"}
 t0=mp.mpf(str(inside[0][0]));old_t=mp.findroot(lambda t:square(K0,a0,t,N)[3],t0);old=max(square(K0,a0,0,N)[0],square(K0,a0,old_t,N)[0]);oldbeta=1/mp.sqrt(old)
 if req.get("restart"):
  K0+=mp.mpf(str(np.random.default_rng(req["seed"]).normal(0,1e-7)))
 def eq(K,a,t):
  A,Ak,Aa,_=square(K,a,0,N);B,Bk,Ba,Bt=square(K,a,t,N)
  return A-B,Bt,Aa*Bk-Ak*Ba
 K,a,t=mp.findroot(eq,(K0,a0,t0),tol=mp.mpf(10)**(-mp.mp.dps+20),maxsteps=60)
 digits=mp.mp.dps-25
 ks=mp.nstr(K,digits,strip_zeros=False,min_fixed=-999,max_fixed=999);as_=mp.nstr(a,digits,strip_zeros=False,min_fixed=-999,max_fixed=999)
 K=mp.mpf(ks);a=mp.mpf(as_);tt=mp.findroot(lambda u:square(K,a,u,N)[3],t)
 modulus=mp.sqrt(max(square(K,a,0,N)[0],square(K,a,tt,N)[0]));beta=1/modulus;gain=beta-oldbeta
 if gain<=0:return {"status":"no_gain","baseline_beta":str(oldbeta),"best_beta":str(beta),"gain":str(gain)}
 claim=None;claimdigits=None
 # Minimal even decimal precision that clears the estimated actual baseline.
 for d in range(10,81,2):
  q=mp.floor(beta*10**d)/10**d
  if q>oldbeta:
   claim=mp.nstr(q,d+1,strip_zeros=False,min_fixed=-999,max_fixed=999);claimdigits=d;break
 if claim is None:return {"status":"precision_floor","gain":str(gain),"precision":mp.mp.dps}
 slack=1/mp.mpf(claim)-modulus;cn=None
 for n in range(1,21):
  tail=2*K**(-((n+1)*(n+2)//2))/(1-K**(-(n+2)))
  if tail<slack/100:cn=n;break
 if cn is None:return {"status":"tail_budget_failure","slack":str(slack)}
 return {"status":"proposal","operator":"precision_equioscillation","candidate":{"name":"autonomous computed parameter proposal","K":ks,"alpha":as_,"lower_bound":claim,"N":cn},"baseline_beta":str(oldbeta),"best_beta":str(beta),"gain":str(gain),"baseline_test_theta":mp.nstr(old_t,70,min_fixed=-999,max_fixed=999),"precision":mp.mp.dps,"claim_digits":claimdigits,"tail_depth_selected":cn,"numerical_proof_slack":str(slack),"residuals":[str(v)for v in eq(K,a,tt)],"mechanism":"standard equioscillation and stationarity, prior art"}
def main():
 req=json.load(sys.stdin);start=time.monotonic();cpu_start=time.process_time()
 try:r=float_local(req)if req["operator"]=="float_local"else precision(req)
 except Exception as e:r={"status":"optimizer_failure","error_type":type(e).__name__,"detail":str(e)[:200]}
 r["elapsed_seconds"]=time.monotonic()-start;r["cpu_seconds"]=time.process_time()-cpu_start;r["peak_rss_kib"]=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;r["request_sha256"]=__import__("hashlib").sha256(json.dumps(req,sort_keys=True,separators=(",",":")).encode()).hexdigest()
 print(json.dumps(r))
if __name__=="__main__":main()
