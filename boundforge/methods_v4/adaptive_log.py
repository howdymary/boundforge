"""Independent exact dyadic logarithm intervals; no search or Arb imports."""
import math
from fractions import Fraction as Q
def ceildiv(a,b):return -((-a)//b)
def _unit_log_bounds(q,bits):
 assert 1<=q<=2;S=1<<bits;t=(q-1)/(q+1);lo=t.numerator*S//t.denominator;hi=ceildiv(t.numerator*S,t.denominator)
 if not hi:return Q(0),Q(0)
 zlo=lo*lo//S;zhi=ceildiv(hi*hi,S);plo,phi=lo,hi;lower=upper=0
 for n in range(1,bits+64):
  den=2*n-1;lower+=2*plo//den;upper+=ceildiv(2*phi,den)
  plo=plo*zlo//S;phi=ceildiv(phi*zhi,S)
  if phi<=4:
   # Remaining series <=2*t^(2n+1)/((2n+1)*(1-t^2)).
   tail=ceildiv(2*phi*S,(2*n+1)*(S-zhi));return Q(lower,S),Q(upper+tail,S)
 raise ArithmeticError("log series did not contract")
def logarithm(q,bits=1024):
 q=Q(q);assert q>0
 if q==1:return Q(0),Q(0)
 k=q.numerator.bit_length()-q.denominator.bit_length();r=q/(Q(2)**k)
 while r<1:r*=2;k-=1
 while r>=2:r/=2;k+=1
 guard=48+abs(k).bit_length();a,b=_unit_log_bounds(r,bits+guard);c,d=_unit_log_bounds(Q(2),bits+guard)
 return (a+k*c,b+k*d)if k>=0 else(a+k*d,b+k*c)
def entropy(probabilities,bits=1024):
 assert all(p>=0 for p in probabilities)and sum(probabilities)==1;lower=upper=Q(0)
 for p in probabilities:
  if not p:continue
  a,b=logarithm(p,bits);lower-=p*b;upper-=p*a
 return lower,upper
def certificate_bounds(c,bits=1024):
 B=c["base"];ns=c["counts"];laws=c["laws"];assert type(B)is int and B>=2 and len(ns)==len(laws)>0 and all(type(n)is int and n>0 for n in ns)
 forms=[(1,-1),(1,0),(0,1),(1,1),(1,2)];low=[Q(0)]*5;high=[Q(0)]*5
 for count,law in zip(ns,laws):
  points=law["points"];weights=[Q(*w)for w in law["weights"]];assert len(points)==len(weights)>0 and min(weights)>0 and sum(weights)==1
  assert len(set(map(tuple,points)))==len(points)and all(len(p)==2 and all(type(x)is int for x in p)for p in points)
  for j,(a,b)in enumerate(forms):
   groups={}
   for (x,y),p in zip(points,weights):
    v=a*x+b*y;assert 2*abs(v)<B;groups[v]=groups.get(v,Q(0))+p
   lo,hi=entropy(list(groups.values()),bits);low[j]+=Q(count,sum(ns))*lo;high[j]+=Q(count,sum(ns))*hi
 assert min(low[1:])>0
 return low[0]/max(high[1:]),high[0]/max(low[1:])
