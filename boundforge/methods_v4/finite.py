"""Two finite-entropy checks independent of formal-series coefficient selection."""
import collections,math
from fractions import Fraction as Q
def arb_values(probabilities,maps,margins,bits):
 from flint import arb,fmpq,ctx
 ctx.prec=bits;hs=[]
 for mapping in maps:
  masses=collections.defaultdict(Q)
  for label,p in zip(mapping,probabilities):masses[str(label)]+=p
  h=arb(0)
  for p in masses.values():
   if p:
    v=arb(fmpq(p.numerator,p.denominator));h-=v*v.log()
  hs.append(h)
 return [sum((arb(fmpq(Q(c).numerator,Q(c).denominator))*h for c,h in zip(row,hs)),arb(0))for row in margins]
def interval_values(probabilities,maps,margins,bits):
 from mpmath import iv
 iv.prec=bits+32;entropies=[]
 for labels in maps:
  values={}
  for i in range(len(probabilities)):
   key=str(labels[i]);values[key]=values.get(key,Q(0))+probabilities[i]
  total=iv.mpf(0)
  for mass in values.values():
   if mass>0:
    t=iv.mpf(mass.numerator)/mass.denominator;total-=t*iv.ln(t)
  entropies.append(total)
 return [sum((iv.mpf(Q(c).numerator)/Q(c).denominator*h for c,h in zip(row,entropies)),iv.mpf(0))for row in margins]
def endpoints(interval):
 out=[]
 for sign,mantissa,exponent,bc in interval._mpi_:out.append(Q((-1 if sign else 1)*mantissa)*Q(2)**exponent)
 return out
def certify(polys,maps,margins,e,bits):
 e=Q(e);base=[Q(p[0])for p in polys];proposed=[sum(Q(v)*e**k for k,v in enumerate(p))for p in polys]
 assert min(base)>=0 and min(proposed)>=0 and sum(base)==sum(proposed)==1
 a0=arb_values(base,maps,margins,bits);a1=arb_values(proposed,maps,margins,bits);ad=[x-y for x,y in zip(a1,a0)];b0=interval_values(base,maps,margins,bits);b1=interval_values(proposed,maps,margins,bits);bd=[endpoints(x-y)for x,y in zip(b1,b0)]
 signs=[]
 for x,(lo,hi)in zip(ad,bd):
  sign=1 if bool(x>0)and lo>0 else(-1 if bool(x<0)and hi<0 else 0);signs.append(sign)
 return {"epsilon":str(e),"precision_bits":bits,"arb_differences":[str(x)for x in ad],"independent_interval_differences":[list(map(str,x))for x in bd],"signs":signs,"strict_all_margins":all(x==1 for x in signs),"candidate_probabilities":list(map(str,proposed))}
