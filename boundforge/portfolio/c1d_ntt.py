"""Independent signed C1d evaluation via six-prime NTT and centered CRT."""
import argparse,json,pathlib,subprocess,tempfile
from fractions import Fraction
HERE=pathlib.Path(__file__).resolve().parent
def check(cert):
 v=cert["v_int"]
 if len(v)<2 or any(type(a)is not int for a in v) or sum(v)==0:raise ValueError("vector/integral")
 n=len(v);bound=n*max(abs(a) for a in v)**2
 with tempfile.TemporaryDirectory() as td:
  exe=pathlib.Path(td)/"ntt";subprocess.run(["g++","-O3","-std=c++17",str(HERE/"ntt.cpp"),"-o",str(exe)],check=True)
  r=json.loads(subprocess.check_output([str(exe),"square"],input=(str(n)+"\n"+" ".join(map(str,v))+"\n").encode()))
 modulus=1;steps=[]
 for p in r["primes"]:steps.append((modulus,p,pow(modulus,-1,p)));modulus*=p
 if modulus<=2*bound:raise ValueError("signed CRT range insufficient")
 peak=0;arg=0
 for k in range(2*n-1):
  x=0
  for j,(scale,p,inverse) in enumerate(steps):x+=((r["coefficients"][j][k]-x)%p)*inverse%p*scale
  if x>modulus//2:x-=modulus
  if abs(x)>bound:raise ValueError("coefficient outside bound")
  if abs(x)>peak:peak=abs(x);arg=k
 value=Fraction(2*n*peak,sum(v)**2)
 return {"valid":True,"score":str(value),"n":n,"argmax_abs_knot":arg,"CRT_modulus":str(modulus),"signed_coefficient_bound":str(bound),"variant":"absolute value at every knot; signed residues uniquely reconstructed"}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("certificate");a=p.parse_args();print(json.dumps(check(json.loads(pathlib.Path(a.certificate).read_text()))))
