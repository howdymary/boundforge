"""Exactly specified finite hereditary construction tasks. No saved record imports."""
import hashlib,itertools,json,random
def bits(s):
 while s:
  b=s&-s;yield b.bit_length()-1;s^=b
class Task:
 def __init__(self,name,n,edges,kind,metadata):
  self.name=name;self.n=n;self.edges=sorted(set(edges));self.kind=kind;self.metadata=metadata;self.inc=[[]for _ in range(n)]
  for e in self.edges:
   for v in bits(e):self.inc[v].append(e^(1<<v))
  self.sha=hashlib.sha256(json.dumps([name,n,self.edges,metadata],sort_keys=True).encode()).hexdigest()
 def legal(self,v,s):return not any(s&p==p for p in self.inc[v])
 def valid(self,s):return 0<=s<(1<<self.n)and all(s&e!=e for e in self.edges)
 def blockers(self,v,s):return [p for p in self.inc[v]if s&p==p]
def cap_third(a,b,d):
 c=0;p=1
 for _ in range(d):c+=(-(a%3+b%3)%3)*p;a//=3;b//=3;p*=3
 return c
def deletion_outputs(v,n):
 s=format(v,"0"+str(n)+"b")
 return {int(s[:i]+s[i+1:j]+s[j+1:],2)for i in range(n)for j in range(i+1,n)}
def make(kind,size,seed,param=0):
 if kind=="graph":
  r=random.Random(seed);edges=[(1<<i)|(1<<j)for i in range(size)for j in range(i+1,size)if r.random()<param]
  return Task("graph-"+str(size)+"-"+str(param)+"-"+str(seed),size,edges,kind,{"seed":seed,"density":param})
 if kind=="cap":
  n=3**size;edges=[]
  for a in range(n):
   for b in range(a+1,n):
    c=cap_third(a,b,size)
    if c>b:edges.append((1<<a)|(1<<b)|(1<<c))
  return Task("cap-"+str(size),n,edges,kind,{"dimension":size})
 if kind=="deletion":
  n=1<<size;by={};edges=set()
  for v in range(n):
   for o in deletion_outputs(v,size):
    for u in by.get(o,[]):edges.add((1<<u)|(1<<v))
    by.setdefault(o,[]).append(v)
  return Task("deletion-"+str(size),n,edges,kind,{"length":size,"deletions":2})
 raise ValueError(kind)
def independent_check(task,s):
 chosen=list(bits(s));assert len(chosen)==s.bit_count()and all(0<=v<task.n for v in chosen)
 if task.kind=="graph":
  r=random.Random(task.metadata["seed"]);p=task.metadata["density"];ss=set(chosen)
  for i in range(task.n):
   for j in range(i+1,task.n):
    edge=r.random()<p
    assert not(edge and i in ss and j in ss)
 elif task.kind=="cap":
  d=task.metadata["dimension"]
  for a,b,c in itertools.combinations(chosen,3):
   aa,bb,cc=a,b,c;line=True
   for _ in range(d):
    if (aa%3+bb%3+cc%3)%3:line=False;break
    aa//=3;bb//=3;cc//=3
   assert not line
 else:
  n=task.metadata["length"];seen={}
  for v in chosen:
   word=format(v,"0"+str(n)+"b");outputs=set()
   for keep in itertools.combinations(range(n),n-2):outputs.add("".join(word[i]for i in keep))
   for o in outputs:
    assert o not in seen,(seen.get(o),v,o)
    seen[o]=v
 return {"valid":True,"members":len(chosen),"definition_checker":task.kind,"task_sha256":task.sha}
