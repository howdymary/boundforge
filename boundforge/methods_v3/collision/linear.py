"""Exact finite-field linear algebra with a per-task determinant safety proof."""
import collections,functools,hashlib,itertools,json,math
@functools.lru_cache(None)
def mersenne_prime(exponent):
 assert exponent in (127,521)
 assert all(exponent%q for q in range(2,math.isqrt(exponent)+1))
 p=(1<<exponent)-1;s=4
 for _ in range(exponent-2):s=(s*s-2)%p
 assert s==0,"Lucas-Lehmer primality check"
 return p
def prime_for(d,norm2):
 for e in (127,521):
  p=mersenne_prime(e)
  if norm2**d<p*p:return p
 raise ValueError("determinant bound exceeds supported exact field")
class Space:
 def __init__(self,d,p):
  self.d=d;self.p=p;self.rows=[];self.ids=[]
 def reduce(self,row,provenance=False):
  p=self.p;v=[int(x)%p for x in row];expr={}
  for pivot,b,origin in self.rows:
   c=v[pivot]
   if not c:continue
   v=[(x-c*y)%p for x,y in zip(v,b)]
   if provenance:
    for k,a in origin.items():
     expr[k]=(expr.get(k,0)+c*a)%p
     if not expr[k]:del expr[k]
  return tuple(v),expr
 def add(self,row,ident):
  v,expr=self.reduce(row,True)
  if not any(v):return None
  j=next(j for j,x in enumerate(v)if x);inv=pow(v[j],-1,self.p);b=tuple(x*inv%self.p for x in v)
  origin={k:-a*inv%self.p for k,a in expr.items()};origin[ident]=inv
  new=Space(self.d,self.p);new.rows=sorted(self.rows+[(j,b,origin)]);new.ids=self.ids+[ident]
  return new
 def key(self):
  rows=[list(b)for j,b,o in self.rows];pivots=[j for j,b,o in self.rows]
  for ii in reversed(range(len(rows))):
   j=pivots[ii]
   for kk in range(ii):
    c=rows[kk][j]
    if c:rows[kk]=[(x-c*y)%self.p for x,y in zip(rows[kk],rows[ii])]
  return hashlib.sha256(json.dumps(rows,separators=(",",":")).encode()).hexdigest()
def partitions(values):
 labels={};groups=[]
 for v in values:
  if v not in labels:labels[v]=len(labels)
  groups.append(labels[v])
 return groups
def entropy(groups):
 n=len(groups);return math.log(n)-sum(c*math.log(c)/n for c in collections.Counter(groups).values())
class Problem:
 def __init__(self,m,controls,target=(1,-1)):
  assert 2<=m<=64 and len(set(map(tuple,controls)))==len(controls)
  self.m=m;self.controls=list(map(tuple,controls));self.target=tuple(target);self.d=2*(m-1)
  self.norm2=max(2*(a*a+b*b)for a,b in self.controls+[self.target]);self.p=prime_for(self.d,self.norm2)
  self.public=[(s,i,j,self.row(a,b,i,j))for s,(a,b)in enumerate(self.controls)for i in range(m)for j in range(i)]
  self.initial_points=[(i-i//2,-(i//2))for i in range(m)]
  self.initial=self.from_points(self.initial_points)
 def row(self,a,b,i,j=0):
  v=[0]*self.d
  for at,sgn in [(i,1),(j,-1)]:
   if at:v[2*(at-1)]+=sgn*a;v[2*(at-1)+1]+=sgn*b
  return tuple(v)
 def signatures(self,space,slope):
  a,b=slope;return [space.reduce(self.row(a,b,i))[0]for i in range(self.m)]
 def valid(self,space):return len(set(self.signatures(space,self.target)))==self.m
 def evaluate(self,space):
  groups=[partitions(self.signatures(space,s))for s in self.controls];hs=[entropy(g)for g in groups]
  return {"ratio":math.log(self.m)/max(hs),"key":tuple(sorted(hs,reverse=True)),"groups":groups,"entropies":hs}
 def from_points(self,points):
  space=Space(self.d,self.p)
  for ident,(s,i,j,row)in enumerate(self.public):
   a,b=self.controls[s]
   if a*(points[i][0]-points[j][0])+b*(points[i][1]-points[j][1])==0:
    new=space.add(row,ident)
    if new is not None:space=new
  assert self.valid(space);return space
 def rebuild(self,ids):
  space=Space(self.d,self.p)
  for ident in ids:
   new=space.add(self.public[ident][3],ident)
   if new is not None:space=new
  return space
 def obstruction(self,trial,new_id):
  sig=self.signatures(trial,self.target);groups=collections.defaultdict(list)
  for i,v in enumerate(sig):groups[v].append(i)
  cores=[];proofs=[]
  for members in groups.values():
   for i,j in itertools.combinations(members,2):
    residue,coeff=trial.reduce(self.row(*self.target,i,j),True)
    assert not any(residue)and coeff.get(new_id)
    core=frozenset(k for k,v in coeff.items()if v and k!=new_id)
    cores.append(core);proofs.append({"target_pair":[i,j],"support":sorted(core)})
  return cores,proofs
def repairs(cores,ids,limit=2):
 if not cores:return [()],0
 if any(not c for c in cores):return [],0
 pool=sorted(set().union(*cores));tested=0
 for size in range(1,limit+1):
  hits=[]
  for comb in itertools.combinations(pool,size):
   tested+=1
   if all(any(x in c for x in comb)for c in cores):hits.append(comb)
  if hits:return hits,tested
 return [],tested
