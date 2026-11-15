"""Independent exact C1b verifier using six-prime NTT and CRT."""
import argparse,json,pathlib,subprocess,tempfile
from fractions import Fraction
HERE=pathlib.Path(__file__).resolve().parent
def check(cert):
 n=cert["n"];den=cert["Q"];h=cert["heights_int"]
 if type(n)is not int or n<2 or n%2 or len(h)!=n or type(den)is not int or not den>0:raise ValueError("n/Q")
 if any(type(x)is not int or not 0<=x<=den for x in h):raise ValueError("box")
 if sum(h)*2!=n*den:raise ValueError("exact integral")
 with tempfile.TemporaryDirectory() as td:
  exe=pathlib.Path(td)/"ntt";subprocess.run(["g++","-O3","-std=c++17",str(HERE/"ntt.cpp"),"-o",str(exe)],check=True)
  r=json.loads(subprocess.check_output([str(exe)],input=(str(n)+"\n"+" ".join(map(str,h))+"\n").encode()))
 primes=r["primes"];prod=1;tables=[]
 for p in primes:tables.append((prod,p,pow(prod,-1,p)));prod*=p
 if prod<=n*den*den:raise ValueError("insufficient CRT range")
 prefix=[0]
 for x in h:prefix.append(prefix[-1]+x)
 maximum=-1;arg=None
 for k in range(2*n-1):
  c=0
  for j,(scale,p,inv) in enumerate(tables):c+=((r["coefficients"][j][k]-c)%p)*inv%p*scale
  if not 0<=c<=n*den*den:raise ValueError("CRT coefficient range")
  shift=n-1-k;l=max(0,-shift);u=min(n,n-shift);overlap=den*(prefix[u]-prefix[l])-c
  if overlap>maximum:maximum=overlap;arg=shift
 result=Fraction(2*maximum,n*den*den)
 return {"valid":True,"score":str(result),"argmax_shift":arg,"n":n,"shifts":2*n-1,"algorithm":"six exact NTTs plus unique nonnegative CRT reconstruction","CRT_product":str(prod),"coefficient_bound":str(n*den*den)}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("certificate");a=p.parse_args();print(json.dumps(check(json.loads(pathlib.Path(a.certificate).read_text()))))
