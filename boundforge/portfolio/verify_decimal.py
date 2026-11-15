"""Independent decimal-interval finite-type checker. No shared math/search imports.
Different cost reconstruction, Decimal directed intervals and Robbins-Stirling.
Decimal.ln is correctly rounded HALF_EVEN: adjacent representables enclose it.
"""
import argparse,json,pathlib
from decimal import Decimal as D,Context,ROUND_FLOOR,ROUND_CEILING,ROUND_HALF_EVEN
from fractions import Fraction
P=110;down=Context(prec=P,rounding=ROUND_FLOOR);up=Context(prec=P,rounding=ROUND_CEILING);near=Context(prec=P,rounding=ROUND_HALF_EVEN)
def interval(x):return (D(x),D(x))
def add(a,b):return down.add(a[0],b[0]),up.add(a[1],b[1])
def neg(a):return a[1].copy_negate(),a[0].copy_negate()
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 vals=[(x,y) for x in a for y in b];return min(down.multiply(x,y) for x,y in vals),max(up.multiply(x,y) for x,y in vals)
def div(a,b):
 if b[0]<=0<=b[1]:raise ValueError("zero interval divisor")
 vals=[(x,y) for x in a for y in b];return min(down.divide(x,y) for x,y in vals),max(up.divide(x,y) for x,y in vals)
def ln(a):
 if a[0]<=0:raise ValueError("positive log")
 return down.next_minus(near.ln(a[0])),up.next_plus(near.ln(a[1]))
def powi(a,n):
 r=interval(1)
 while n:
  if n&1:r=mul(r,a)
  a=mul(a,a);n//=2
 return r
def fact(n):
 if n==0:return interval(0)
 # Robbins with a common log(2pi)/2 constant omitted: it cancels below except
 # (1-number_of_types) times the constant. Enclose log(2pi)/2 in [0.9189,0.9190].
 main=sub(mul(add(interval(n),div(interval(1),interval(2))),ln(interval(n))),interval(n))
 return add(add(main,(D("0.9189"),D("0.9190"))),div(interval(1),(D(12*n+1),D(12*n))))
def check(cert):
 mask=cert["mask"]
 if not isinstance(mask,list) or mask!=sorted(set(mask)) or len(mask)<2 or mask[0]!=0 or any(type(a)is not int or not 0<=a<=2000 for a in mask):raise ValueError("alphabet")
 N=int(cert["N"]);xn,xd=map(int,cert["x"]);yn,yd=map(int,cert["y"])
 if N<2 or not 0<xn<xd or not 0<yn<yd:raise ValueError("tilts")
 present=set(mask);diffs=sorted({b-a for a in mask for b in mask if b>a})
 cost={}
 for d in diffs:
  for a in range(mask[-1]+1):
   if a in present and a+d in present:cost[d]=2*a+d;break
 # Exact floors by a separate common-denominator integer polynomial.
 exponent=max(cost.values());weights={d:pow(xn,cost[d])*pow(xd,exponent-cost[d]) for d in diffs};zero=pow(xd,exponent);normal=zero+2*sum(weights.values())
 counts={d:N*weights[d]//normal for d in diffs};n0=N-2*sum(counts.values());L=sum(counts[d]*cost[d] for d in diffs)
 if n0<=0 or not any(counts.values()) or L<mask[-1]:raise ValueError("nontrivial type")
 if cert.get("counts") is not None and cert["counts"]!={str(d):str(counts[d]) for d in diffs}:raise ValueError("type mismatch")
 if "n0" in cert and int(cert["n0"])!=n0:raise ValueError("n0 mismatch")
 if "L" in cert and int(cert["L"])!=L:raise ValueError("L mismatch")
 logD=sub(fact(N),fact(n0))
 for d in diffs:logD=sub(logD,mul(interval(2),fact(counts[d])))
 # Exact sum polynomial as integers, then correctly-rounded decimal log interval.
 sums=sorted({a+b for a in mask for b in mask});deg=max(sums);pnum=sum(pow(yn,s)*pow(yd,deg-s) for s in sums);pden=pow(yd,deg)
 logP=ln(div(interval(pnum),interval(pden)));logy=ln(div(interval(yn),interval(yd)))
 logS=sub(mul(interval(N),logP),mul(interval(2*L),logy))
 if logD[0]<=0 or logS[0]<=0:raise ValueError("functional sign")
 ratio=div(logD,logS)
 if cert.get("claim") and Fraction(ratio[0])<=Fraction(cert["claim"]):raise ValueError("unsupported strict claim")
 return {"valid":True,"N":str(N),"n0":str(n0),"L":str(L),"base":2*mask[-1]+1,"counts":{str(d):str(counts[d]) for d in diffs},"rate_interval_decimal":list(map(str,ratio)),"precision":P,"scope":"Independent exact type reconstruction plus directed Decimal intervals and Robbins bounds. Conservative log(2pi)/2 enclosure [0.9189,0.9190]."}
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("certificate");a=ap.parse_args();print(json.dumps(check(json.loads(pathlib.Path(a.certificate).read_text()))))
