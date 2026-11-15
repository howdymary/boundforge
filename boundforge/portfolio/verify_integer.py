"""Exact masked-family finite-type certificate checker, integer logarithm enclosures.
No numerical search imports. Written after reading prior certificates; not clean-room.
"""
import argparse,hashlib,json,pathlib
from fractions import Fraction
BITS=384;ONE=1<<BITS;TERMS=180
def ceildiv(a,b):return -(-a//b)
def atanh(p,q):
 if not 0<=p<q:raise ValueError("atanh domain")
 p2=p*p;q2=q*q;lo=p*ONE//q;hi=ceildiv(p*ONE,q);a=b=0
 for j in range(TERMS):
  a+=lo//(2*j+1);b+=ceildiv(hi,2*j+1)
  lo=lo*p2//q2;hi=ceildiv(hi*p2,q2)
 tail=ceildiv(hi*q2,(2*TERMS+1)*(q2-p2))
 return 2*a,2*(b+tail)
LN2=atanh(1,3)
def logint(n):
 if n<1:raise ValueError("positive logarithm argument")
 e=n.bit_length()-1;v=1<<e;a,b=atanh(n-v,n+v)
 return e*LN2[0]+a,e*LN2[1]+b
def lograt(r):
 a,b=logint(r.numerator);c,d=logint(r.denominator)
 return a-d,b-c
def factorial(n):
 if n==0:return 0,0
 a,b=logint(n)
 # Elementary Stirling: (n+1/2)ln n-n <= ln(n!) <= same +1 for n>=1.
 return (2*n+1)*a//2-n*ONE,ceildiv((2*n+1)*b,2)-n*ONE+ONE
def reconstruct(cert):
 mask=cert["mask"]
 if len(mask)<2 or mask!=sorted(set(mask)) or any(type(x)is not int or x<0 for x in mask) or mask[0]!=0 or mask[-1]>2000:raise ValueError("mask")
 N=int(cert["N"]);x=Fraction(*map(int,cert["x"]));y=Fraction(*map(int,cert["y"]))
 if N<2 or not 0<x<1 or not 0<y<1:raise ValueError("type parameters")
 costs={};witness={}
 for a in mask:
  for b in mask:
   d=a-b;k=a+b
   if k<costs.get(d,10**9):costs[d]=k;witness[d]=(a,b)
 assert costs[0]==0 and all(costs[d]==costs[-d] for d in costs)
 powers={k:x**k for k in set(costs.values())};Z=sum(powers[k] for k in costs.values())
 counts={d:int(N*powers[costs[d]]//Z) for d in costs if d>0};n0=N-2*sum(counts.values());L=sum(counts[d]*costs[d] for d in counts)
 if n0<1 or not any(counts.values()) or L<mask[-1]:raise ValueError("nontrivial finite type")
 if "counts" in cert and cert["counts"]!={str(d):str(counts[d]) for d in sorted(counts)}:raise ValueError("type count mismatch")
 if "n0" in cert and int(cert["n0"])!=n0:raise ValueError("zero count mismatch")
 if "L" in cert and int(cert["L"])!=L:raise ValueError("budget mismatch")
 sums={a+b for a in mask for b in mask};P=sum(y**s for s in sums)
 dlow,dhigh=factorial(N);l,h=factorial(n0);dlow-=h;dhigh-=l
 for count in counts.values():
  l,h=factorial(count);dlow-=2*h;dhigh-=2*l
 pl,ph=lograt(P);yl,yh=lograt(y)
 slow=N*pl-2*L*yh;shigh=N*ph-2*L*yl
 if not 0<dlow<=dhigh or not 0<slow<=shigh:raise ValueError("log bound sign")
 lower=Fraction(dlow,shigh);upper=Fraction(dhigh,slow)
 if cert.get("claim") and not lower>Fraction(cert["claim"]):raise ValueError("claimed rate not strictly certified")
 return {"valid":True,"schema":"masked-family-type-v1","N":str(N),"n0":str(n0),"L":str(L),"base":2*mask[-1]+1,"mask_size":len(mask),"sum_support":len(sums),"difference_support":len(costs),"counts":{str(d):str(counts[d]) for d in sorted(counts)},"witnesses":{str(d):list(witness[d]) for d in sorted(counts)},"rate_interval":[str(lower),str(upper)],"decimal_display":str(float(lower)),"log_D_interval_fixed":[str(dlow),str(dhigh)],"log_S_interval_fixed":[str(slow),str(shigh)],"fixed_point_bits":BITS,"scope":"Capacity lower bound from a completely specified finite budgeted word family and carry-free projection. Interval encloses the certified log-multinomial/log-envelope functional, not an upper bound on the true constant."}
def main():
 a=argparse.ArgumentParser();a.add_argument("certificate");args=a.parse_args();raw=pathlib.Path(args.certificate).read_bytes();r=reconstruct(json.loads(raw));r["certificate_sha256"]=hashlib.sha256(raw).hexdigest();print(json.dumps(r))
if __name__=="__main__":main()
