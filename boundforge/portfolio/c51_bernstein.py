"""Independent C51a whole-circle certificate: exact Bernstein upper coefficients.
mpmath.iv only encloses transcendental coefficient constants. Rational subdivision.
"""
import argparse,json,math,pathlib
from fractions import Fraction as F
from mpmath import iv
iv.dps=100
def scalar(q):
 q=F(q);return iv.mpf(q.numerator)/q.denominator
def endpoint(t):
 s,m,e,_=t;return F((-1 if s else 1)*m)*(F(2)**e)
def ends(v):return tuple(endpoint(t)for t in v._mpi_)
def upper(v):return ends(v)[1]
def lower(v):return ends(v)[0]
def tail(K,N):return 2*K**(-((N+1)*(N+2)//2))/(1-K**(-(N+2)))
def polys(N):
 R=[[1],[-3,4]]
 for n in range(1,N):
  a,b=R[-1],R[-2];c=[0]*(len(a)+1)
  for i,v in enumerate(a):c[i]-=2*v;c[i+1]+=4*v
  for i,v in enumerate(b):c[i]-=v
  R.append(c)
 return R[:N+1]
def coefficients(K,a,N):
 R=polys(N);q=[iv.mpf(0)for _ in range(2*N+2)]
 for i in range(N+1):
  ti=i*(i+1)//2
  for j in range(i+1):
   tj=j*(j+1)//2;c=4*(1 if i==j else 2)*scalar(K)**(-ti-tj)*iv.cos(scalar(a)*(ti-tj))
   for k,u in enumerate(R[i]):
    for l,v in enumerate(R[j]):q[k+l+1]+=c*u*v
 return q
def split(bs):
 left=[bs[0]];right=[bs[-1]]
 while len(bs)>1:
  bs=[(a+b)/2 for a,b in zip(bs,bs[1:])];left.append(bs[0]);right.append(bs[-1])
 return left,right[::-1]
def check(data):
 K=F(data["K"]);a=F(data["alpha"]);claim=F(data["lower_bound"]);N=data["N"]
 if not(K>1 and 0<claim<1 and 1<=N<=20):raise ValueError("input range")
 T=tail(K,N);threshold=(1/claim-T)**2
 if 1/claim<=T:raise ValueError("tail")
 q=coefficients(K,a,N);d=len(q)-1
 bs=[upper(sum((q[j]*scalar(F(math.comb(k,j),math.comb(d,j)))for j in range(k+1)),iv.mpf(0)))for k in range(d+1)]
 stack=[(bs,0)];nodes=leaves=depthmax=0;maxbound=F(0)
 while stack:
  b,depth=stack.pop();nodes+=1
  if max(b)<threshold:
   leaves+=1;depthmax=max(depthmax,depth);maxbound=max(maxbound,max(b))
  else:
   if depth>=80 or nodes>=100000:raise ValueError("whole-domain cover not established")
   u,v=split(b);stack.extend([(u,depth+1),(v,depth+1)])
 beta=1/(iv.sqrt(scalar(maxbound))+scalar(T))
 assert lower(beta)>claim
 return {"valid":True,"lower_bound":str(claim),"reciprocal_interval":[str(v)for v in ends(beta)],"N":N,"nodes":nodes,"leaves":leaves,"max_depth":depthmax,"entire_circle":True,"infinite_tail":str(T),"method":"Exact rational Bernstein subdivision, interval real cosine cross-coefficients","analytic_dependency":"He–Tang Theorem2.8, arXiv2602.12217"}
def witness_upper(data,theta):
 K=F(data["K"]);a=F(data["alpha"]);N=data["N"];t=scalar(F(theta));rr=iv.mpf(0);ii=iv.mpf(0)
 for n in range(N+1):
  T=n*(n+1)//2;b=2*scalar(K)**(-T)*iv.cos((2*n+1)*t);rr+=b*iv.cos(scalar(a)*T);ii+=b*iv.sin(scalar(a)*T)
 modlo=lower(iv.sqrt(rr*rr+ii*ii))-tail(K,N)
 assert modlo>0
 return 1/modlo
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("certificate");a=p.parse_args();print(json.dumps(check(json.loads(pathlib.Path(a.certificate).read_text()))))
