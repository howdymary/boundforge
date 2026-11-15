"""Explicit task adapters; F/H mathematical definitions attributed to Cla2026."""
import itertools,random,hashlib,json
def ingredients():
 edges=list(itertools.combinations(range(5),2));F=set()
 for v in range(5):F.add(sum(1<<i for i,e in enumerate(edges) if v in e))
 for a in itertools.combinations(range(5),2):F.add(sum(1<<i for i,(u,v) in enumerate(edges) if (u in a)!=(v in a)))
 for t in itertools.combinations(range(10),4):
  deg=[sum(v in edges[i] for i in t) for v in range(5)]
  # A graph with four edges and degrees1,1,1,2,3 must be the connected chair.
  if sorted(deg)==[1,1,1,2,3]:F.add(1023^sum(1<<i for i in t))
 H=set()
 for seed in [[0,1,2,3,4,5,6],[0,1,2,3,4,6,7],[0,1,2,6,9]]:
  for a in {x*x%11 for x in range(1,11)}:
   for b in range(11):H.add(sum(1<<((a*x+b)%11) for x in seed))
 assert len(F)==75 and len(H)==121
 return sorted(F),sorted(H)
def isvalid_c49(family,n):
 if len(family)!=len(set(family)) or any(type(x)is not int or not 0<=x<1<<n for x in family):return False
 for a,b in itertools.combinations(family,2):
  if a&b in (a,b):return False
 for a,b,c in itertools.combinations(family,3):
  if a&b==a&c==b&c:return False
 return True
def uniform(n,seed):
 rng=random.Random(seed);pool=[sum(1<<i for i in c) for c in itertools.combinations(range(n),n//2)];rng.shuffle(pool);s=[]
 for x in pool:
  if all(not (a&b==a&x==b&x) for a,b in itertools.combinations(s,2)):s.append(x)
 return sorted(s)
def digest(s):return hashlib.sha256(json.dumps(sorted(s)).encode()).hexdigest()
def dev_tasks():
 F,H=ingredients()
 return [{"id":"F10","kind":0,"n":10,"param":0,"state":F},{"id":"uniform8","kind":0,"n":8,"param":0,"state":uniform(8,1101)}]
def heldout_tasks():
 F,H=ingredients()
 return [{"id":"H11","kind":0,"n":11,"param":0,"state":H},{"id":"uniform9","kind":0,"n":9,"param":0,"state":uniform(9,2202)},
 {"id":"MIS64-a","kind":1,"n":64,"param":3303,"state":[]},{"id":"MIS64-b","kind":1,"n":64,"param":4404,"state":[]},
 {"id":"cap4","kind":2,"n":4,"param":0,"state":[]}]
