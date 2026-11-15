"""Complete equality-stratum compiler for fixed-k rational support additions.
Standard affine-arrangement enumeration; contribution/novelty remains a hypothesis.
"""
import itertools,time
from fractions import Fraction as Q
from .masks import affine,dot
def canonical(rows,rhs,d):
 ans=affine(rows,rhs,d)
 return None if ans is None else ans
def generic_flat(p,basis,equations):
 varying=[(a,b)for a,b in equations if any(dot(a,v)for v in basis)]
 for t in range(len(basis)*len(varying)+1):
  x=tuple(p[i]+sum(v[i]*Q(t)**(j+1)for j,v in enumerate(basis))for i in range(len(p)))
  if all(dot(a,x)!=b for a,b in varying):return x
 raise AssertionError("finite hyperplane avoidance failed")
def equality_maps(old,new,forms):
 maps=[]
 for a in forms:
  labels={};mapping=[]
  for x in list(old)+list(new):
   value=dot(a,x);labels.setdefault(value,len(labels));mapping.append(labels[value])
  maps.append(tuple(mapping))
 return tuple(maps)
def compile_partitions(old,forms,k,max_flats=20000):
 d=len(forms[0]);D=d*k;assert k>0 and old
 equations={}
 def put(a,b):
  solved=canonical([a],[b],D)
  if solved is not None and solved[2]:equations.setdefault(solved[2][0],(tuple(map(Q,a)),Q(b)))
 for j,a in enumerate(forms):
  for i in range(k):
   row=[Q(0)]*D;row[i*d:(i+1)*d]=map(Q,a)
   for b in {dot(a,x)for x in old}:put(row,b)
  for i,l in itertools.combinations(range(k),2):
   row=[Q(0)]*D
   for h,v in enumerate(a):row[i*d+h]=Q(v);row[l*d+h]=-Q(v)
   put(row,0)
 equations=list(equations.values());root=canonical([],[],D);flats={root[2]:root};front=[root];parts={};start=time.process_time();solves=0;complete=True
 while front:
  p,basis,key=front.pop();x=generic_flat(p,basis,equations);new=[x[i*d:(i+1)*d]for i in range(k)];maps=equality_maps(old,new,forms)
  parts.setdefault(maps,{"new_points":new,"rank":D-len(basis)})
  if not basis:continue
  rows=[row[:-1]for row in key];rhs=[row[-1]for row in key]
  for a,b in equations:
   if not any(dot(a,v)for v in basis):continue
   solves+=1;child=canonical(rows+[a],rhs+[b],D)
   if child is None or child[2]in flats:continue
   if len(flats)>=max_flats:complete=False;break
   flats[child[2]]=child;front.append(child)
  if not complete:break
 return {"partitions":parts,"complete":complete,"flats":len(flats),"equations":len(equations),"solves":solves,"cpu":time.process_time()-start}
