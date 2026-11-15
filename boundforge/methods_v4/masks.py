"""Exact projection-novelty oracle over Q^d. See MASK_SPEC.md.
Geometry and final cone bounds use rational arithmetic; scipy only proposes weights.
"""
import itertools,time
from fractions import Fraction as Q

def dot(a,b):return sum((Q(x)*Q(y) for x,y in zip(a,b)),Q())
def affine(rows,rhs,d):
 """Canonical RREF affine solution p + span(basis); None if inconsistent."""
 M=[[Q(x) for x in row]+[Q(v)] for row,v in zip(rows,rhs)];piv=[];r=0
 for c in range(d):
  k=next((i for i in range(r,len(M)) if M[i][c]),None)
  if k is None:continue
  M[r],M[k]=M[k],M[r];q=M[r][c];M[r]=[x/q for x in M[r]]
  for i in range(len(M)):
   if i!=r and M[i][c]:
    q=M[i][c];M[i]=[x-q*y for x,y in zip(M[i],M[r])]
  piv.append(c);r+=1
 if any(not any(row[:d]) and row[d] for row in M):return None
 p=[Q(0)]*d
 for i,c in enumerate(piv):p[c]=M[i][d]
 basis=[]
 for c in range(d):
  if c not in piv:
   v=[Q(0)]*d;v[c]=1
   for i,k in enumerate(piv):v[k]=-M[i][c]
   basis.append(v)
 return p,basis,tuple(tuple(row)for row in M[:r])
def generic(p,basis,forms,shadows):
 """Avoid a finite union of proper rational hyperplanes, with finite root bound."""
 varying=[j for j,a in enumerate(forms) if any(dot(a,v) for v in basis)]
 degree=len(basis);limit=degree*sum(len(shadows[j]) for j in varying)
 for t in range(limit+1):
  x=tuple(p[i]+sum(v[i]*Q(t)**(k+1) for k,v in enumerate(basis)) for i in range(len(p)))
  if all(dot(forms[j],x) not in shadows[j] for j in varying):return x,t
 raise AssertionError("Moment-curve root-count bound violated")
def signatures(points,forms,required_new=()):
 """Enumerate all attainable novelty masks, not just a bounded coordinate box."""
 d=len(forms[0]);m=len(forms);assert all(len(a)==d for a in forms)
 assert points and all(len(p)==d for p in points)
 shadows=[{dot(a,p)for p in points} for a in forms];found={};flats=set();trials=0;start=time.process_time()
 for r in range(min(d,m)+1):
  for ids in itertools.combinations(range(m),r):
   rank=affine([forms[i]for i in ids],[0]*r,d)
   if len(rank[1])!=d-r:continue
   for vals in itertools.product(*(sorted(shadows[i])for i in ids)):
    solved=affine([forms[i]for i in ids],vals,d);p,basis,key=solved;trials+=1
    if key in flats:continue
    flats.add(key);x,t=generic(p,basis,forms,shadows)
    mask=tuple(int(dot(a,x)not in S) for a,S in zip(forms,shadows))
    if all(mask[j]for j in required_new):found.setdefault(mask,{"point":x,"basis_rank":r,"curve_parameter":t})
 return {"masks":found,"flats":len(flats),"flat_trials":trials,"cpu":time.process_time()-start,"shadows":shadows}
def cone(masks,margins):
 """Certified primal/dual bounds for max_w min_r (Vw)_r, sum w=1.
 LP output is never accepted without exact re-evaluation. Nonpositive upper bound
 excludes strictly positive logarithmic simultaneous ascent, not all improvement.
 """
 import numpy as np
 from scipy.optimize import linprog
 masks=list(masks);R=len(margins);N=len(masks);assert N and R
 V=[[dot(row,mask) for mask in masks]for row in margins]
 A=np.array([[float(-v)for v in row]+[1.]for row in V])
 result=linprog([0.]*N+[-1.],A_ub=A,b_ub=[0.]*R,A_eq=[[1.]*N+[0.]],b_eq=[1.],bounds=[(0,None)]*N+[(None,None)],method="highs")
 assert result.success,result.message
 def simplex(xs):
  v=[max(Q(0),Q(float(x)).limit_denominator(10**9))for x in xs];s=sum(v);assert s>0;return [x/s for x in v]
 w=simplex(result.x[:N]);mu=simplex([-x for x in result.ineqlin.marginals])
 lower=min(sum(v*x for v,x in zip(row,w))for row in V)
 upper=max(sum(mu[r]*V[r][j]for r in range(R))for j in range(N))
 assert lower<=upper
 status="positive-leading-witness"if lower>0 else"no-positive-leading-ascent"if upper<=0 else"unresolved-rational-gap"
 return {"status":status,"lower":lower,"upper":upper,"weights":w,"dual":mu,"V":V}
