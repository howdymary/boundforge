"""Conventional exact-event locations, floating entropy screening, protected final acceptance."""
import collections,copy,hashlib,itertools,json,math,random,time
from fractions import Fraction as Q
from .pencil import normalize
CONTROLS=[(1,0),(0,1),(1,1),(1,2)]
def entropy_masses(values,weights):
 groups=collections.defaultdict(list)
 for value,p in zip(values,weights):groups[value].append(p)
 return math.fsum(-s*math.log(s)for row in groups.values()if(s:=math.fsum(row))>0)
def law_entropies(points,weights):
 return [entropy_masses([a*x+b*y for x,y in points],weights)for a,b in CONTROLS]
def mix_opt(a,b,ta,tb):
 options=[1e-6,1-1e-6]
 for i,j in itertools.combinations(range(4),2):
  den=(a[i]-b[i])-(a[j]-b[j])
  if den:
   t=(b[j]-b[i])/den
   if options[0]<t<options[1]:options.append(t)
 def score(t):return (t*ta+(1-t)*tb)/max(t*x+(1-t)*y for x,y in zip(a,b))
 best=max(options,key=score);return best,score(best)
def scan(points,direction,weights,deadline=None):
 m=len(points);forms=CONTROLS+[(1,-1)];events=collections.defaultdict(lambda:collections.defaultdict(list));forbidden=set();sizes=[];hs=[];affines=[]
 for s,(a,b)in enumerate(forms):
  values=[(a*x+b*y,a*dx+b*dy)for (x,y),(dx,dy)in zip(points,direction)];affines.append(values);labels={};ids=[]
  for value in values:
   if value not in labels:labels[value]=len(labels)
   ids.append(labels[value])
  masses=[[]for _ in labels]
  for i,p in zip(ids,weights):masses[i].append(p)
  mass=[math.fsum(x)for x in masses];sizes.append(mass);hs.append(math.fsum(-x*math.log(x)for x in mass if x>0))
  for i in range(m):
   for j in range(i):
    A,B=values[i];C,D=values[j]
    if B==D:continue
    t=Q(C-A,B-D)
    if s==4:forbidden.add(t)
    else:events[t][s].append((ids[i],ids[j]))
 assert len(set(affines[-1]))==m
 generic=0
 while generic in events or generic in forbidden:generic+=1
 records=[{"parameter":[generic,1],"entropies":hs[:4]}];complete=True;digest=hashlib.sha256();invalid=0
 for t in sorted(set(events)|forbidden):
  if deadline is not None and time.process_time()>=deadline:complete=False;break
  good=t not in forbidden;digest.update((str(t)+":"+str(good)+"\n").encode())
  if not good:invalid+=1;continue
  hh=hs[:4].copy()
  for s,edges in events[t].items():
   parent={};mass={}
   def find(x):
    parent.setdefault(x,x)
    while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
    return x
   for u,v in edges:
    u=find(u);v=find(v)
    if u==v:continue
    a=mass.get(u,sizes[s][u]);b=mass.get(v,sizes[s][v]);c=a+b;hh[s]+=a*math.log(a)+b*math.log(b)-c*math.log(c);parent[v]=u;mass[u]=c
  records.append({"parameter":[t.numerator,t.denominator],"entropies":hh})
 if len({x-y for x,y in direction})==m:records.append({"parameter":None,"entropies":law_entropies(direction,weights)})
 return records,{"complete_event_location_scan":complete,"weighted_ranking":"floating screening, not an exact family-optimality certificate","event_locations":len(set(events)|forbidden),"target_collisions_rejected":invalid,"location_trace_sha256":digest.hexdigest()}
def realize(points,direction,parameter):
 if parameter is None:return normalize(direction)
 t=Q(*parameter);return normalize([(x+t*dx,y+t*dy)for (x,y),(dx,dy)in zip(points,direction)])
def choose_direction(points,weights,arm,rng):
 m=len(points);v=[[0,0]for _ in points]
 def point():return rng.choices(range(m),weights=[max(p,1e-12)**.3 for p in weights])[0]
 if arm in [0,3]:
  for _ in range(1 if arm==0 else 2):v[point()][rng.randrange(2)]+=rng.choice([-1,1])
 else:
  for _ in range(1 if arm==1 else 2):
   a,b=rng.choice(CONTROLS);i=point();value=a*points[i][0]+b*points[i][1];sign=rng.choice([-1,1])
   for j,(x,y)in enumerate(points):
    if a*x+b*y==value:v[j][0]+=sign*b;v[j][1]-=sign*a
 return [tuple(x)for x in v]
def search(certificate,seed,cpu=60):
 start=time.process_time();rng=random.Random(seed);points=[normalize(l["points"])for l in certificate["laws"]];weights=[[float(Q(*w))for w in law["weights"]]for law in certificate["laws"]];targets=[entropy_masses(list(range(len(p))),w)for p,w in zip(points,weights)];ent=[law_entropies(p,w)for p,w in zip(points,weights)];alpha=float(Q(certificate["counts"][0],sum(certificate["counts"])));base=(alpha*targets[0]+(1-alpha)*targets[1])/max(alpha*a+(1-alpha)*b for a,b in zip(*ent));current=best=base;bestpoints=copy.deepcopy(points);bestalpha=alpha;counts=[0]*4;rewards=[0.0]*4;trace=[];turn=0
 while time.process_time()-start<cpu:
  law=rng.randrange(2);unseen=[i for i,c in enumerate(counts)if not c];arm=unseen[0]if unseen else max(range(4),key=lambda i:rewards[i]/counts[i]+math.sqrt(2*math.log(turn+2)/counts[i]));direction=choose_direction(points[law],weights[law],arm,rng);source=points[law];before=current;begin=time.process_time();records,evidence=scan(source,direction,weights[law],start+cpu)
  scored=[]
  for r in records:
   hh=list(ent);hh[law]=r["entropies"];t,value=mix_opt(hh[0],hh[1],*targets);scored.append((value,t,r))
  value,t,record=max(scored,key=lambda x:x[0]);candidate=realize(source,direction,record["parameter"]);height=max(abs(v).bit_length()for p in candidate for v in p)
  retained=False
  if height<=512 and value>best+1e-9:
   best=value;bestpoints=copy.deepcopy(points);bestpoints[law]=candidate;bestalpha=t;retained=True
  selected=(rng.choice(scored)if rng.random()<.1 else(value,t,record));sv,st,sr=selected;candidate2=realize(source,direction,sr["parameter"]);h2=max(abs(v).bit_length()for p in candidate2 for v in p);temperature=.005*(.3+.7*(1-(turn%50)/50))
  accepted=h2<=512 and (sv>=current or rng.random()<math.exp(max(-700,(sv-current)/temperature)))
  if accepted:points[law]=candidate2;ent[law]=sr["entropies"];current=sv;alpha=st
  counts[arm]+=1;rewards[arm]+=max(0,value-before)*100
  trace.append({"turn":turn,"law":law,"operator":["coordinate","projection_block","two_blocks","coordinate_pair"][arm],"point_before":source,"direction":direction,"best_parameter":record["parameter"],"selected_parameter":sr["parameter"],"screened_best":value,"incumbent_best":best,"before":before,"accepted":accepted,"retained":retained,"height_bits":height,"evidence":evidence,"cpu":time.process_time()-start,"intervention_cpu":time.process_time()-begin,"arm_counts":list(counts),"arm_rewards":list(rewards)});turn+=1
 candidate=copy.deepcopy(certificate);candidate["claimed_lower_bound"]=[0,1]
 if best>base+1e-9:
  for law,p in zip(candidate["laws"],bestpoints):law["points"]=[list(x)for x in p]
  den=10**18;num=max(1,min(den-1,round(bestalpha*den)));candidate["counts"]=[num,den-num];candidate["base"]=1+2*max(abs(a*x+b*y)for law in candidate["laws"]for x,y in law["points"]for a,b in CONTROLS+[(1,-1)])
 return {"seed":seed,"search_cpu":time.process_time()-start,"initial_screened":base,"best_screened":best,"screened_improvement":best-base,"candidate":candidate,"trace":trace,"new_method_claim":False,"record_claim":False,"scope":"Conventional bounded production search, floating screening and exact rational event locations; final acceptance outside worker"}
