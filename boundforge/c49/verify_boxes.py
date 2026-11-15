"""Independent finite certificate implementation: disjoint Cartesian boxes, not BDDs.
Written after reading primary sources; not claimed clean-room or a new verification method.
Does not import the search, BDD checker, or search-side exact module.
"""
import argparse,collections,functools,itertools,json,pathlib
from fractions import Fraction
def check(cert):
 n=cert["n"];ports=cert["ports"];s=cert["masks"]
 if type(n)is not int or not 3<=n<=28:raise ValueError("ground-set scope")
 if len(ports)!=2 or any(type(p)is not int or not 0<=p<n for p in ports) or ports[0]==ports[1]:raise ValueError("ports")
 if not 1<=len(s)<=300000 or any(type(x)is not int or not 0<=x<1<<n for x in s) or len(s)!=len(set(s)):raise ValueError("mask range or duplicate")
 a=min(n,8);b=min(n-a,10);groups=collections.defaultdict(lambda:collections.defaultdict(list))
 for x in s:groups[x&((1<<a)-1)][(x>>a)&((1<<b)-1)].append(x>>(a+b))
 boxes=[]
 for core,rows in groups.items():
  fibres=collections.defaultdict(list)
  for u,vs in rows.items():fibres[tuple(sorted(vs))].append(u)
  boxes.extend((core,tuple(sorted(us)),vs) for vs,us in fibres.items())
 assert sum(len(u)*len(v) for c,u,v in boxes)==len(s)
 @functools.lru_cache(None)
 def subset(u,v,strict=False):
  return any(x&y==x and (not strict or x!=y) for x in u for y in v)
 @functools.lru_cache(None)
 def flower(u,v,w,nonconstant=False):
  # Equal intersections iff z contains x&y and avoids x^y.
  for x in u:
   for y in v:
    k=x&y;zfree=x^y
    if any(z&k==k and not z&zfree and (not nonconstant or not(x==y==z)) for z in w):return True
  return False
 for i,(c,u,v) in enumerate(boxes):
  if subset(u,u,True) or subset(v,v,True):raise ValueError("containment within Cartesian block")
  for j,(d,w,z) in enumerate(boxes):
   if i!=j and c&d==c and subset(u,w) and subset(v,z):raise ValueError("containment between blocks")
 for i,j,k in itertools.combinations_with_replacement(range(len(boxes)),3):
  c,u,v=boxes[i];d,w,z=boxes[j];e,h,t=boxes[k]
  if i==k:
   if flower(u,u,u,True) or flower(v,v,v,True):raise ValueError("sunflower within block")
  elif c&d==c&e==d&e and flower(u,w,h) and flower(v,z,t):raise ValueError("sunflower between blocks")
 counts=[sum(((x>>ports[0])&1)*2+((x>>ports[1])&1)==k for x in s) for k in range(4)]
 if min(counts)<1:raise ValueError("nonpositive port count")
 trace=counts[1]+counts[2];det=counts[1]*counts[2]-counts[0]*counts[3];power=n-2
 # Direct integer comparison of rational x^power with the larger characteristic root.
 def smaller(x):
  y=x**power
  return 2*y<=trace or y*y-trace*y+det<0
 low=Fraction(0);high=Fraction(2)
 while smaller(high):high*=2
 for _ in range(200):
  mid=(low+high)/2
  if smaller(mid):low=mid
  else:high=mid
 if cert.get("claimed_rate_lower") and not smaller(Fraction(cert["claimed_rate_lower"])):raise ValueError("unsupported rate claim")
 return {"valid":True,"members":len(s),"counts":counts,"exponent":power,"boxes":len(boxes),"rate_interval_rational":[str(low),str(high)]}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("certificate");a=ap.parse_args()
 try:print(json.dumps(check(json.loads(pathlib.Path(a.certificate).read_text()))))
 except Exception as e:print(json.dumps({"valid":False,"reason":str(e)}));raise SystemExit(1)
if __name__=="__main__":main()
