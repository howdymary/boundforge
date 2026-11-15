"""Independent complete 2D-kernel family checker. No search/scanner imports."""
import collections,itertools,math
from fractions import Fraction as Q
def rank(rows):
 a=[[Q(x)for x in r]for r in rows]
 if not a:return 0
 i=0
 for j in range(len(a[0])):
  hit=next((k for k in range(i,len(a))if a[k][j]),None)
  if hit is None:continue
  a[i],a[hit]=a[hit],a[i];c=a[i][j];a[i]=[x/c for x in a[i]]
  for k in range(i+1,len(a)):
   c=a[k][j]
   if c:a[k]=[x-c*y for x,y in zip(a[k],a[i])]
  i+=1
  if i==len(a):break
 return i
def check_family(m,controls,event):
 assert event["nullity"]==2 and event["scan"]["complete_slice"]
 p=event["point_before"];v=event["direction"];assert len(p)==len(v)==m
 assert p[0]==[0,0]and v[0]==[0,0]
 pf=[x for pair in p[1:]for x in pair];vf=[x for pair in v[1:]for x in pair];d=2*(m-1)
 assert rank([pf,vf])==2
 allrows=[]
 for a,b in controls:
  for i in range(m):
   for j in range(i):
    row=[0]*d
    for at,sgn in [(i,1),(j,-1)]:
     if at:row[2*(at-1)]+=a*sgn;row[2*(at-1)+1]+=b*sgn
    allrows.append(row)
 retained=[allrows[i]for i in event["retained_basis_ids"]];assert rank(retained)==d-2
 for r in retained:
  assert sum(a*b for a,b in zip(r,pf))==0 and sum(a*b for a,b in zip(r,vf))==0
 forms=list(map(tuple,controls))+[(1,-1)];affine=[[(a*x+b*y,a*dx+b*dy)for (x,y),(dx,dy)in zip(p,v)]for a,b in forms];critical=set()
 for values in affine:
  for (A,B),(C,D)in itertools.combinations(values,2):
   if B!=D:critical.add(Q(C-A,B-D))
 generic=0
 while generic in critical:generic+=1
 parameters=sorted(critical)+[Q(generic)];best=None;feasible=0
 for t in parameters+[None]:
  values=[[B if t is None else A+t*B for A,B in row]for row in affine]
  if len(set(values[-1]))<m:continue
  feasible+=1;key=tuple(sorted(math.prod(c**c for c in collections.Counter(row).values())for row in values[:-1]))
  if best is None or key>best:best=key
 assert best==tuple(event["scan"]["best_key"])
 return {"valid":True,"complete_projective_family":True,"best_key":list(best),"critical_parameters":len(critical),"feasible_representatives":feasible,"method":"Fresh rational rank and direct coordinate aggregation; no event-union or modular code"}
