"""Method2: NTT of signed height jumps, followed by exact event integration.
Shares no prefix/interpolation logic or coefficient implementation with Method1.
"""
import argparse,collections,json,pathlib,subprocess,tempfile
from fractions import Fraction
HERE=pathlib.Path(__file__).resolve().parent
def check(cert):
 n=cert["n"];Q=int(cert["Q"]);h=cert["heights_int"];translation=Fraction(*map(int,cert.get("translation_cells",["0","1"])));P=translation.numerator;R=translation.denominator
 if type(n)is not int or n<2 or n%2 or len(h)!=n or Q<1 or any(type(v)is not int or not 0<=v<=Q for v in h) or sum(h)*2!=n*Q:raise ValueError("invalid input")
 nonzero=[i for i,x in enumerate(h) if x]
 if translation < -nonzero[0] or translation > n-1-nonzero[-1]:raise ValueError("shifted support")
 jumps=[h[0]]+[h[i]-h[i-1] for i in range(1,n)]+[-h[-1]]
 with tempfile.TemporaryDirectory() as td:
  exe=pathlib.Path(td)/"ntt";subprocess.run(["g++","-O3","-std=c++17",str(HERE/"ntt.cpp"),"-o",str(exe)],check=True)
  r=json.loads(subprocess.check_output([str(exe)],input=(str(n+1)+"\n"+" ".join(map(str,jumps))+"\n").encode()))
 prod=1;steps=[]
 for p in r["primes"]:steps.append((prod,p,pow(prod,-1,p)));prod*=p
 bound=(n+1)*max(abs(x) for x in jumps)**2
 if prod<=2*bound:raise ValueError("signed jump CRT range")
 events=collections.defaultdict(int)
 for k in range(2*n+1):
  c=0
  for j,(scale,p,inv) in enumerate(steps):c+=((r["coefficients"][j][k]-c)%p)*inv%p*scale
  if c>prod//2:c-=prod
  if abs(c)>bound:raise ValueError("jump coefficient range")
  if c:events[(k-n)*R]+=c
 # g has jumps -Delta f at shifted internal knots and +1/-1 at0/2.
 # R''(x)=-sum Delta f(p) Delta g(q) delta(x-(q-p)).
 for i,jump in enumerate(jumps):
  if jump:
   events[-P-i*R]-=Q*jump
   events[n*R-P-i*R]+=Q*jump
 value=0;slope=0;peak=0;location=0;previous=min(events)
 for location_key in sorted(events):
  value+=slope*(location_key-previous)
  if value<0:raise ValueError("negative exact overlap")
  if value>peak:peak=value;location=location_key
  slope+=events[location_key];previous=location_key
 if value!=0 or slope!=0:raise ValueError("event integration fails closure")
 result=Fraction(2*peak,n*Q*Q*R)
 return {"valid":True,"score":str(result),"n":n,"translation_cells":str(translation),"event_count":len(events),"argmax_lag_cells":str(Fraction(location,R)),"all_real_shifts":True,"final_value":str(value),"final_slope":str(slope),"algorithm":"six-prime exact signed jump-correlation and event integration"}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("certificate");a=p.parse_args();print(json.dumps(check(json.loads(pathlib.Path(a.certificate).read_text()))))
