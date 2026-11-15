"""Exploratory high-precision equioscillation; not certified acceptance."""
import json,os,pathlib
import mpmath as mp
mp.mp.dps=100
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"c51precision";OUT.mkdir(exist_ok=True)
N=16
def square(K,a,t):
 P=mp.mpc(0);dK=mp.mpc(0);da=mp.mpc(0);dt=mp.mpc(0)
 for n in range(N+1):
  T=n*(n+1)//2;k=2*n+1;c=2*mp.exp(1j*a*T)*K**(-T);v=c*mp.cos(k*t)
  P+=v;dK-=T*v/K;da+=1j*T*v;dt-=k*c*mp.sin(k*t)
 return tuple(2*mp.re(mp.conj(P)*v)for v in [P/2,dK,da,dt])
def equations(K,a,t):
 A,Ak,Aa,_=square(K,a,0);B,Bk,Ba,Bt=square(K,a,t)
 return A-B,Bt,Aa*Bk-Ak*Ba
def value(K,a):
 t=mp.findroot(lambda t:square(K,a,t)[3],mp.mpf(".64554"));return 1/mp.sqrt(max(square(K,a,0)[0],square(K,a,t)[0])),t
def main():
 K,a,t=mp.findroot(equations,(mp.mpf("3.568185442233685"),mp.mpf("3.961543111810228"),mp.mpf(".64554")),tol=mp.mpf("1e-85"),maxsteps=60)
 newbeta=1/mp.sqrt(square(K,a,t)[0]);baselines={}
 for name,ks,aa in [("Sothanaphan","3.568182317714","3.961543335688"),("Roehrig","3.5681854310698435","3.9615431126097391"),("WorkingReport","3.568185442233685","3.961543111810228")]:
  bv,tt=value(mp.mpf(ks),mp.mpf(aa));baselines[name]={"K":ks,"alpha":aa,"beta_numerical":str(bv),"interior_peak":str(tt),"gain_numerical":str(newbeta-bv)}
 report={"run_id":os.environ["GITHUB_RUN_ID"],"source_sha":os.environ["GITHUB_SHA"],"K":str(K),"alpha":str(a),"theta":str(t),"beta_numerical":str(newbeta),"residuals":[str(v)for v in equations(K,a,t)],"baselines":baselines,"scope":"Exploratory parameter refinement below original 1e-9 pilot gate, not a preregistered success. Equioscillation/stationarity only, not global parameter optimality. Certification and fresh frontier audit required."}
 (OUT/"report.json").write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=="__main__":main()
