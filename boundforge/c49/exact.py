"""Exact rational isolation of positive two-port transfer rates."""
from fractions import Fraction
def above(counts,exponent,x):
 a,b,c,d=counts # N00,N01,N10,N11
 trace=b+c;det=b*c-a*d;y=x**exponent
 return 2*y<=trace or y*y-trace*y+det<0
def bounds(counts,exponent,bits=180):
 assert exponent>0 and all(type(x)is int and x>0 for x in counts)
 lo=Fraction(1);hi=Fraction(2)
 while above(counts,exponent,hi):hi*=2
 for _ in range(bits):
  mid=(lo+hi)/2
  if above(counts,exponent,mid):lo=mid
  else:hi=mid
 return lo,hi
def dec(x,up=False,digits=45):
 s=10**digits;q=(x.numerator*s)//x.denominator
 if up and Fraction(q,s)<x:q+=1
 return str(q//s)+"."+str(q%s).zfill(digits)
def rate_interval(counts,exponent):
 lo,hi=bounds(counts,exponent)
 return {"counts":counts,"exponent":exponent,"lower":str(lo),"upper":str(hi),"decimal":[dec(lo),dec(hi,True)]}
def improves(counts,exponent,bar_counts=(33980,64728,64728,88867),bar_exp=26):
 if tuple(counts)==tuple(bar_counts) and exponent==bar_exp:return False
 lo,hi=bounds(counts,exponent);bl,bh=bounds(bar_counts,bar_exp)
 return lo>bh
