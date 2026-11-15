"""Recover integer points and check their actual projections, independent of modular scores."""
import collections,math
from fractions import Fraction as Q
def rational_kernel(rows,d):
 a=[[Q(x)for x in row]for row in rows];piv=[];i=0
 for j in range(d):
  hit=next((k for k in range(i,len(a))if a[k][j]),None)
  if hit is None:continue
  a[i],a[hit]=a[hit],a[i];v=a[i][j];a[i]=[x/v for x in a[i]]
  for k in range(len(a)):
   if k==i or not a[k][j]:continue
   c=a[k][j];a[k]=[x-c*y for x,y in zip(a[k],a[i])]
  piv.append(j);i+=1
  if i==len(a):break
 free=[j for j in range(d)if j not in piv];basis=[]
 for j in free:
  v=[Q(0)]*d;v[j]=1
  for k,p in enumerate(piv):v[p]=-a[k][j]
  basis.append(v)
 return basis
def actual_groups(points,slope):
 a,b=slope;labels={};out=[]
 for x,y in points:
  z=a*x+b*y
  if z not in labels:labels[z]=len(labels)
  out.append(labels[z])
 return out
def recover(problem,space):
 expected=problem.evaluate(space)["groups"];rows=[problem.public[i][3]for i in space.ids];basis=rational_kernel(rows,problem.d);assert basis
 forbidden=(len(problem.controls)+1)*problem.m*(problem.m-1)//2
 bound=max(0,(len(basis)-1)*forbidden)
 for t in range(bound+1):
  v=[sum((Q(t)**k)*b[j]for k,b in enumerate(basis))for j in range(problem.d)]
  scale=math.lcm(*(x.denominator for x in v));vv=[int(x*scale)for x in v]
  points=[(0,0)]+list(zip(vv[::2],vv[1::2]))
  if len({a*x+b*y for x,y in points for a,b in [problem.target]})!=problem.m:continue
  if [actual_groups(points,s)for s in problem.controls]!=expected:continue
  assert all(sum(c*x for c,x in zip(r,vv))==0 for r in rows)
  return {"points":[list(p)for p in points],"controls":[list(s)for s in problem.controls],"target":list(problem.target),"uniform_denominator":problem.m,"moment_parameter":t,"moment_root_bound":bound,"basis_ids":space.ids,"predicted_groups":expected}
 raise AssertionError("generic rational embedding failed")
def verify(witness):
 """Use protected exact rational logarithm code; no modular assumptions."""
 from boundforge.verify_independent import logarithm,decimal
 points=witness["points"];m=len(points);assert m==witness["uniform_denominator"]and m>1
 assert len(set(map(tuple,points)))==m
 target=actual_groups(points,witness["target"]);assert len(set(target))==m
 ent=[]
 for s in witness["controls"]:
  groups=actual_groups(points,s);lo=hi=Q(0)
  for c in collections.Counter(groups).values():
   p=Q(c,m);a,b=logarithm(p);lo-=p*b;hi-=p*a
  ent.append((lo,hi))
 l,u=logarithm(Q(m));lo=l/max(b for a,b in ent);hi=u/max(a for a,b in ent)
 assert lo>0
 return {"valid":True,"ratio_interval":[decimal(lo),decimal(hi,True)],"method":"Integer projections and protected exact rational atanh log bounds","target_injective":True}
def verify_intervals(witness):
 """Second arithmetic backend; recompute projected counts directly."""
 from mpmath import iv
 iv.dps=80;m=len(witness["points"]);hs=[]
 for a,b in witness["controls"]:
  values=collections.Counter(a*x+b*y for x,y in witness["points"]);h=iv.mpf(0)
  for count in values.values():
   p=iv.mpf(count)/m;h-=p*iv.ln(p)
  hs.append(h)
 a,b=witness["target"];assert len({a*x+b*y for x,y in witness["points"]})==m
 # max of interval endpoints, not lexicographic interval ordering.
 def endpoints(x):
  out=[]
  for s,man,exp,bc in x._mpi_:out.append(Q((-1 if s else 1)*man)*Q(2)**exp)
  return out
 lows,ups=zip(*(endpoints(h)for h in hs));target=endpoints(iv.ln(m))
 return {"valid":True,"ratio_interval_rational":[str(target[0]/max(ups)),str(target[1]/max(lows))],"method":"Independent direct coordinate aggregation with mpmath interval logarithms"}
