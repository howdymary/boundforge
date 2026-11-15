"""Exact event scan for a rational trajectory. Standard algebra; no novelty claim."""
import collections,hashlib,itertools,json,math,random,time
from fractions import Fraction as Q
from .linear import Problem,partitions
from .certify import rational_kernel,actual_groups,verify,verify_intervals
def product(groups):return math.prod(c**c for c in collections.Counter(groups).values())
def objective(points,controls):
 return tuple(sorted(product(actual_groups(points,s))for s in controls))
def ratio(key,m):return math.log(m)/(math.log(m)-math.log(key[0])/m)
def normalize(points):
 origin=points[0];points=[(Q(x)-origin[0],Q(y)-origin[1])for x,y in points];den=math.lcm(*(v.denominator for p in points for v in p));ints=[(int(x*den),int(y*den))for x,y in points];g=math.gcd(*(abs(v)for p in ints for v in p))or 1
 return [(x//g,y//g)for x,y in ints]
def event_scan(points,direction,controls,target=(1,-1),deadline=None):
 m=len(points);slopes=list(map(tuple,controls))+[tuple(target)];base=[];counts=[];products=[];events=collections.defaultdict(lambda:collections.defaultdict(list));forbidden=set();affines=[]
 for s,(a,b)in enumerate(slopes):
  values=[(a*x+b*y,a*vx+b*vy)for (x,y),(vx,vy)in zip(points,direction)];affines.append(values);labels=partitions(values);base.append(labels);sizes=list(collections.Counter(labels).values());counts.append(sizes);products.append(math.prod(c**c for c in sizes))
  for i in range(m):
   for j in range(i):
    A,B=values[i];C,D=values[j]
    if B==D:continue
    t=Q(C-A,B-D)
    if s==len(controls):forbidden.add(t)
    else:events[t][s].append((labels[i],labels[j]))
 assert len(set(base[-1]))==m
 generic=0
 while generic in events or generic in forbidden:generic+=1
 records=[{"parameter":[generic,1],"generic":True,"valid":True,"products":products[:-1],"key":sorted(products[:-1])}]
 complete=True
 for t in sorted(set(events)|forbidden):
  if deadline is not None and time.process_time()>=deadline:complete=False;break
  if t in forbidden:records.append({"parameter":[t.numerator,t.denominator],"valid":False,"reason":"exact target collision"});continue
  ps=products[:-1].copy()
  for s,edges in events[t].items():
   parent={};mass={}
   def find(x):
    parent.setdefault(x,x)
    while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
    return x
   for u,v in edges:
    u=find(u);v=find(v)
    if u==v:continue
    a=mass.get(u,counts[s][u]);b=mass.get(v,counts[s][v]);ps[s]=ps[s]//(a**a)//(b**b)*((a+b)**(a+b));parent[v]=u;mass[u]=a+b
  records.append({"parameter":[t.numerator,t.denominator],"valid":True,"products":ps,"key":sorted(ps)})
 # Projective infinity corresponds to the direction alone.
 if len({a*x+b*y for x,y in direction for a,b in [target]})==m:
  ps=[product([B for A,B in values])for values in affines[:-1]];records.append({"parameter":None,"infinity":True,"valid":True,"products":ps,"key":sorted(ps)})
 valid=[r for r in records if r["valid"]];best=max(tuple(r["key"])for r in valid)
 return {"records":records,"best_key":best,"complete_slice":complete,"events_total":len(set(events)|forbidden),"events_visited":len(records)-1,"generic_parameter":generic,"point_count":m}
def realize(points,direction,record):
 if record.get("infinity"):return normalize(direction)
 t=Q(*record["parameter"]);return normalize([(x+t*vx,y+t*vy)for (x,y),(vx,vy)in zip(points,direction)])
def parallel(a,b):
 i=next((i for i,x in enumerate(a)if x),None)
 return i is None or all(a[i]*y==x*b[i]for x,y in zip(a,b))
def direction_for(problem,points,state,rng,release):
 kept=[i for i in state.ids if i not in release];sub=problem.rebuild(kept);kernel=rational_kernel([problem.public[i][3]for i in kept],problem.d);flat=[v for p in points[1:]for v in p]
 vectors=[v for v in kernel if not parallel(flat,v)]
 if not vectors:return None,{"diagnosis":"no_nonparallel_kernel_direction","nullity":len(kernel)}
 v=rng.choice(vectors);scale=math.lcm(*(x.denominator for x in v));direction=[(0,0)]+list(zip([int(x*scale)for x in v[::2]],[int(x*scale)for x in v[1::2]]))
 return direction,{"nullity":len(kernel),"released_basis_rows":list(release),"retained_flat_key":sub.key(),"retained_basis_ids":kept,"projective_family_complete_if_slice_complete":len(kernel)==2}
def episode(spec,policy,seed,cpu=2,certify=True):
 from .search import propose
 m,controls=spec;start=time.process_time();problem=Problem(m,controls);rng=random.Random(seed);state=problem.initial;points=problem.initial_points;current=objective(points,controls);best=current;beststate=state;bestpoints=list(points);trace=[];cache={};turn=0;force_large=False
 while time.process_time()-start<cpu:
  begin=time.process_time()
  if policy in ["circuit","batch_repair"]:
   cand,event=propose(problem,state,policy,rng,deadline=start+cpu);groups=problem.evaluate(cand)["groups"];key=tuple(sorted(product(g)for g in groups))
   if key>current or rng.random()<.025:state=cand;current=key
   if key>best:best=key;beststate=cand;bestpoints=None
  elif policy=="coordinate":
   candidate=list(points);count=1 if rng.random()<.8 else min(3,m-1)
   for i in rng.sample(range(1,m),count):
    j=rng.randrange(m);a,b=rng.choice(problem.controls);x,y=candidate[i];xx,yy=candidate[j]
    if rng.random()<.65:
     if a:x=Q(a*xx+b*(yy-y),a)
     else:y=yy
    else:
     scale=rng.choice([1,m,m*m]);x+=rng.randint(-scale,scale);y+=rng.randint(-scale,scale)
    candidate[i]=(x,y)
   if len({x-y for x,y in candidate})<m:continue
   key=objective(candidate,controls);event={"diagnosis":"coordinate mutation"}
   if key>current or rng.random()<.025:points=candidate;current=key
   if key>best:best=key;bestpoints=normalize(candidate);beststate=None
  else:
   if policy in ["coordinate_event","random_event"]:
    if policy=="coordinate_event":
     v=[0]*problem.d;v[rng.randrange(problem.d)]=1;direction=[(0,0)]+list(zip(v[::2],v[1::2]))
    else:direction=[(0,0)]+[(rng.randint(-2,2),rng.randint(-2,2))for _ in range(1,m)]
    info={"nullity":None,"projective_family_complete_if_slice_complete":False}
   else:
    release_size=min(2,len(state.ids))if force_large else (1 if rng.random()<.7 else min(2,len(state.ids)));force_large=False
    release=tuple(rng.sample(state.ids,release_size))if state.ids else ()
    direction,info=direction_for(problem,points,state,rng,release)
    if direction is None:turn+=1;continue
   cache_key=info.get("retained_flat_key")if info.get("nullity")==2 else None
   if policy=="state_memory_event"and cache_key:cache_key=state.key()+":"+cache_key
   if policy in ["memory_event","state_memory_event"]and cache_key in cache and tuple(cache[cache_key]["best_key"])<=current:
    force_large=True
    event={"diagnosis":"certified_projective_family_covered","record_retrieved":cache_key,"record_origin_turn":cache[cache_key]["origin_turn"],"decision_changed":"skip event reevaluation; require a two-row release on the next action","scope":"Exact same retained row space, uniform masses, controls and target within this episode","family_best_key":cache[cache_key]["best_key"],**info}
   else:
    scan=event_scan(points,direction,controls,deadline=start+cpu);valid=[r for r in scan["records"]if r["valid"]];key=max(tuple(r["key"])for r in valid)
    options=[r for r in valid if tuple(r["key"])==key]if key>current else valid
    chosen=rng.choice(options);candidate=realize(points,direction,chosen);actual=objective(candidate,controls);assert actual==tuple(chosen["key"])
    event={"diagnosis":"complete_event_scan"if scan["complete_slice"]else"event_scan_budget_exhausted","basis_before":list(state.ids),"direction":[list(p)for p in direction],"point_before":[list(p)for p in points],"scan":scan,"chosen_parameter":chosen["parameter"],**info}
    if policy in ["memory_event","state_memory_event"]and cache_key and scan["complete_slice"]:
     cache[cache_key]={"best_key":list(scan["best_key"]),"origin_turn":turn};event["record_written"]=cache_key
    if policy=="scheduled_event"and actual<=current:force_large=True
    if actual>current or rng.random()<.025:
     points=candidate;current=actual;state=problem.from_points(points)
    if actual>best:best=actual;bestpoints=candidate;beststate=None
  event.update(turn=turn,current_key=list(current),best_key=list(best),cpu=time.process_time()-start,intervention_cpu=time.process_time()-begin);trace.append(event);turn+=1
 searchcpu=time.process_time()-start
 if bestpoints is None:
  from .certify import recover
  witness=recover(problem,beststate)
 else:
  pp=normalize(bestpoints);witness={"points":[list(p)for p in pp],"controls":[list(s)for s in controls],"target":[1,-1],"uniform_denominator":m}
 check=verify(witness)if certify else {};second=verify_intervals(witness)if certify else {}
 assert objective(witness["points"],controls)==best
 return {"task":{"m":m,"controls":controls},"policy":policy,"seed":seed,"best_key":list(best),"best_ratio":ratio(best,m),"search_cpu":searchcpu,"total_cpu":time.process_time()-start,"trace":trace,"witness":witness,"check":check,"second_check":second,"cache_entries":len(cache),"scope":"Exploratory uniform collision-objective search; no new-method or record claim"}
