"""Exact coefficients of finite-pushforward entropy perturbations.
H(e)=sum_k [A_k log(1/e)+B_k] e^k + higher terms.
Symbolic expansion is standard; methodological advantage remains a hypothesis.
"""
import collections,math
from fractions import Fraction as Q
class Logs:
 def __init__(self,c=0,terms=None):self.c=Q(c);self.terms={}if terms is None else dict(terms)
 def add(self,other,scale=1):
  scale=Q(scale);self.c+=scale*other.c
  for base,coef in other.terms.items():
   self.terms[base]=self.terms.get(base,Q(0))+scale*coef
   if not self.terms[base]:del self.terms[base]
  return self
 def scaled(self,scale):return Logs().add(self,scale)
 def zero(self):return not self.c and not self.terms
 def interval(self,bits=256):
  from flint import arb,fmpq,ctx
  ctx.prec=bits;v=arb(fmpq(self.c.numerator,self.c.denominator))
  for base,coef in self.terms.items():v+=arb(fmpq(coef.numerator,coef.denominator))*arb(fmpq(base.numerator,base.denominator)).log()
  return v
 def sign(self):
  if self.zero():return 0,{"exact_zero":True}
  for bits in [128,256,512,1024,2048]:
   value=self.interval(bits)
   if bool(value>0):return 1,{"bits":bits,"interval":str(value)}
   if bool(value<0):return -1,{"bits":bits,"interval":str(value)}
  return None,{"status":"unresolved logarithmic coefficient; not assumed zero"}
 def data(self):return {"constant":str(self.c),"logs":{str(k):str(v)for k,v in self.terms.items()}}
def logq(q):
 q=Q(q);assert q>0;out=Logs()
 for value,sign in [(q.numerator,1),(q.denominator,-1)]:
  for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]:
   count=0
   while value%p==0:value//=p;count+=1
   if count:out.add(Logs(terms={Q(p):Q(count*sign)}))
  if value>1:out.add(Logs(terms={Q(value):Q(sign)}))
 return out
def mul(a,b,K):
 out=[Q(0)]*(K+1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   if i+j<=K:out[i+j]+=x*y
 return out
def entropy_poly(coeffs,K):
 coeffs=[Q(x)for x in coeffs]+[Q(0)]*max(0,K+1-len(coeffs));coeffs=coeffs[:K+1];first=next((i for i,x in enumerate(coeffs)if x),None)
 A=[Q(0)]*(K+1);B=[Logs()for _ in range(K+1)]
 if first is None:return A,B
 c=coeffs[first];assert c>0,"negative leading mass"
 u=[Q(0)]*(K+1)
 for j in range(1,K-first+1):u[j]=coeffs[first+j]/c
 logseries=[Q(0)]*(K+1);power=[Q(1)]+[Q(0)]*K
 for n in range(1,K+1):
  power=mul(power,u,K);scale=Q(1 if n%2 else -1,n)
  for j,x in enumerate(power):logseries[j]+=scale*x
 regular=mul(coeffs,logseries,K);lc=logq(c)
 for k in range(K+1):A[k]=first*coeffs[k];B[k]=lc.scaled(-coeffs[k]);B[k].c-=regular[k]
 return A,B
def check_polynomials(polys):
 assert polys
 degree=max(map(len,polys));sums=[sum((Q(p[k])if k<len(p)else Q(0))for p in polys)for k in range(degree)]
 assert sums[0]==1 and all(x==0 for x in sums[1:]),"not a normalized probability perturbation"
 radius=Q(1,2)
 for poly in polys:
  p=list(map(Q,poly));r=next((i for i,x in enumerate(p)if x),None)
  if r is None:continue
  assert p[r]>0,"negative leading mass"
  remainder=sum(-x for x in p[r+1:]if x<0)
  if remainder:radius=min(radius,p[r]/(2*remainder))
 return radius
def compile(polys,maps,margins,K=4):
 polys=[list(map(Q,p))for p in polys];radius=check_polynomials(polys);assert all(len(m)==len(polys)for m in maps);assert all(len(row)==len(maps)for row in margins)
 mapped=[]
 for mapping in maps:
  groups={}
  for label,poly in zip(mapping,polys):
   key=str(label);groups.setdefault(key,[Q(0)]*(K+1))
   for k,x in enumerate(poly):
    if k<=K:groups[key][k]+=x
  A=[Q(0)]*(K+1);B=[Logs()for _ in range(K+1)]
  for p in groups.values():
   aa,bb=entropy_poly(p,K)
   for k in range(K+1):A[k]+=aa[k];B[k].add(bb[k])
  mapped.append((A,B))
 compiled=[]
 for row in margins:
  A=[Q(0)]*(K+1);B=[Logs()for _ in range(K+1)]
  for c,(aa,bb)in zip(row,mapped):
   for k in range(K+1):A[k]+=Q(c)*aa[k];B[k].add(bb[k],Q(c))
  leading={"sign":0,"status":"zero through tested order; not identically zero"}
  for k in range(1,K+1):
   if A[k]:
    leading={"sign":1 if A[k]>0 else -1,"order":k,"kind":"logarithmic","coefficient":str(A[k]),"ordinary":B[k].data()};break
   sign,proof=B[k].sign()
   if sign!=0:leading={"sign":sign,"order":k,"kind":"ordinary","coefficient":B[k].data(),"proof":proof};break
  compiled.append({"A":A,"B":B,"leading":leading})
 return {"mapped":mapped,"margins":compiled,"safe_radius":radius,"order":K}
def evaluate_polys(polys,e):
 e=Q(e);out=[sum(Q(x)*e**k for k,x in enumerate(p))for p in polys];assert min(out)>=0 and sum(out)==1;return out
def proposed_bits(compiled):
 radius=compiled["safe_radius"];bits=max(8,radius.denominator.bit_length()-radius.numerator.bit_length()+3)
 for margin in compiled["margins"]:
  lead=margin["leading"]
  if lead.get("sign")!=1:continue
  if lead["kind"]=="logarithmic":
   k=lead["order"];a=margin["A"][k];b=margin["B"][k].interval(256)
   try:estimate=float(b)
   except (ValueError,OverflowError):estimate=-1e6
   if math.isfinite(estimate):bits=max(bits,math.ceil(max(0,-estimate/float(a))/math.log(2))+24)
 return bits
def json_result(result):
 return {"order":result["order"],"safe_radius":str(result["safe_radius"]),"proposed_epsilon_bits":proposed_bits(result),"margins":[{"A":list(map(str,m["A"])),"B":[x.data()for x in m["B"]],"leading":m["leading"]}for m in result["margins"]]}
