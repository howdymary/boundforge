"""Exact circuit repair and basis-change controller; shared objective and action interface."""
import hashlib,json,math,random,time
from .linear import Problem,repairs,entropy
from .certify import recover,verify,verify_intervals,actual_groups
POLICIES=["coordinate","random_flat","circuit","random_pivot","guided_pivot","shuffled_core"]
def coord_score(problem,points):
 hs=[entropy(actual_groups(points,s))for s in problem.controls]
 return {"ratio":math.log(problem.m)/max(hs),"key":tuple(sorted(hs,reverse=True))}
def sample_row(problem,space,rng):
 e=problem.evaluate(space);worst=max(range(len(e["entropies"])),key=lambda s:e["entropies"][s])
 choices=[i for i,(s,u,v,r)in enumerate(problem.public)if s==worst]if rng.random()<.8 else list(range(len(problem.public)))
 rng.shuffle(choices)
 for i in choices[:24]:
  trial=space.add(problem.public[i][3],i)
  if trial is not None:return i,trial
 return None,None
def pivot(problem,space,rng):
 choices=[i for i in range(len(problem.public))if i not in space.ids];rng.shuffle(choices)
 for q in choices[:40]:
  r,coeff=space.reduce(problem.public[q][3],True)
  if any(r):continue
  options=[i for i,c in coeff.items()if c]
  if not options:continue
  removed=rng.choice(options);new=problem.rebuild([i for i in space.ids if i!=removed]+[q])
  assert len(new.ids)==len(space.ids)and new.key()==space.key()
  return new,{"inserted_equivalent_row":q,"removed_basis_row":removed,"flat_unchanged":True}
 return None,None
def propose(problem,space,policy,rng):
 row,trial=sample_row(problem,space,rng)
 if trial is None:return space,{"diagnosis":"sampled_rows_dependent","scope":"24 sampled rows; not exhaustion"}
 cores,proof=problem.obstruction(trial,row)
 event={"proposed_row":row,"forced_target_pairs":proof,"basis_before":list(space.ids),"diagnosis":"legal_addition"if not cores else"target_collision_forced"}
 if not cores:return trial,event
 if policy=="random_flat":
  removed=rng.sample(space.ids,min(len(space.ids),rng.choice([1,2])));candidate=problem.rebuild([i for i in space.ids if i not in removed]+[row]);event["removed"]=removed
  return (candidate if problem.valid(candidate)else space),event
 usecores=cores
 if policy=="shuffled_core":
  perm=list(space.ids);rng.shuffle(perm);mapping=dict(zip(space.ids,perm));usecores=[frozenset(mapping[i]for i in c)for c in cores];event["diagnosis_control"]="shuffled labels, exact acceptance retained"
 hits,checked=repairs(usecores,space.ids,1);event["repair_subsets_checked"]=checked
 event["no_one_row_repair"]=not hits
 if not hits and policy in ["random_pivot","guided_pivot"]:
  oldkey=space.key();tested=[]
  for attempt in range(8 if policy=="guided_pivot"else 1):
   alternative,move=pivot(problem,space,rng)
   if alternative is None:continue
   alttrial=alternative.add(problem.public[row][3],row)
   assert alttrial is not None
   altcores,altproof=problem.obstruction(alttrial,row);althits,n=repairs(altcores,alternative.ids,1);event["repair_subsets_checked"]+=n
   tested.append({**move,"one_row_repair_available":bool(althits),"new_target_pairs":altproof})
   if althits or policy=="random_pivot":
    space=alternative;trial=alttrial;cores=altcores;usecores=altcores;hits=althits;event["basis_change"]=move;break
  event["representation_probes"]=tested;assert space.key()==oldkey
 if not hits:
  hits,n=repairs(usecores,space.ids,2);event["repair_subsets_checked"]+=n
 if not hits:
  event["diagnosis"]="no_repair_within_two_basis_deletions"
  event["scope"]="Exact for this independent basis and one proposed row only; no flat/global impossibility"
  return space,event
 removed=rng.choice(hits);candidate=problem.rebuild([i for i in space.ids if i not in removed]+[row]);event["removed"]=list(removed)
 if not problem.valid(candidate):event["acceptance"]="refuted after shuffled diagnostic";return space,event
 event["acceptance"]="exact target separation"
 return candidate,event
def episode(spec,policy,seed,cpu=2):
 m,controls=spec;start=time.process_time();wall=time.monotonic();problem=Problem(m,controls);rng=random.Random(seed);space=problem.initial;current=problem.evaluate(space);best=space;bestscore=current;points=list(problem.initial_points);bestpoints=points;trace=[];turn=0;lastbest=0;tested=0;repairs_count=0
 while time.process_time()-start<cpu:
  begin=time.process_time();before=current
  if policy=="coordinate":
   candidate=list(points);count=1 if rng.random()<.8 else min(3,m-1)
   for i in rng.sample(range(1,m),count):
    if rng.random()<.65:
     j=rng.randrange(m);a,b=rng.choice(problem.controls);x,y=candidate[i];xx,yy=candidate[j]
     if a==1:x=xx+b*(yy-y)
     elif a==0 and b==1:y=yy
     else:raise ValueError("coordinate baseline only supports unit first coefficient")
     candidate[i]=(x,y)
    else:
     x,y=candidate[i];scale=rng.choice([1,m,m*m]);candidate[i]=(x+rng.randint(-scale,scale),y+rng.randint(-scale,scale))
   tested+=1
   if len({x-y for x,y in candidate})!=m:continue
   value=coord_score(problem,candidate);event={"diagnosis":"coordinate proposal","changed_points":count}
   if value["key"]<current["key"]or rng.random()<.025:points=candidate;current=value
   if value["key"]<bestscore["key"]:bestpoints=candidate;bestscore=value;lastbest=time.process_time()-start
  else:
   candidate,event=propose(problem,space,policy,rng);tested+=1
   value=problem.evaluate(candidate);repairs_count+=event.get("repair_subsets_checked",0)
   if value["key"]<current["key"]or rng.random()<.025:space=candidate;current=value
   if value["key"]<bestscore["key"]:best=candidate;bestscore=value;lastbest=time.process_time()-start
  event.update(turn=turn,before_ratio=before["ratio"],after_ratio=current["ratio"],best_ratio=bestscore["ratio"],cpu=time.process_time()-start,intervention_cpu=time.process_time()-begin)
  trace.append(event);turn+=1
 searchcpu=time.process_time()-start;certstart=time.process_time()
 if policy=="coordinate":best=problem.from_points(bestpoints)
 witness=recover(problem,best);check=verify(witness);second=verify_intervals(witness)
 assert abs(problem.evaluate(best)["ratio"]-bestscore["ratio"])<1e-10
 return {"task":{"m":m,"controls":controls},"policy":policy,"seed":seed,"search_cpu":searchcpu,"certification_cpu":time.process_time()-certstart,"total_cpu":time.process_time()-start,"wall":time.monotonic()-wall,"initial_ratio":problem.evaluate(problem.initial)["ratio"],"best_ratio":bestscore["ratio"],"best_entropies":bestscore["key"],"time_to_best_cpu":lastbest,"proposals":tested,"repair_subsets_checked":repairs_count,"representation_changes":sum("basis_change"in e for e in trace),"directed_pivots_enabled":sum(e.get("no_one_row_repair",False)and"basis_change"in e and any(p["one_row_repair_available"]for p in e.get("representation_probes",[]))for e in trace),"prime_bits":problem.p.bit_length(),"determinant_bound":str(problem.norm2**problem.d),"witness":witness,"check":check,"second_check":second,"trace":trace,"scope":"Exploratory uniform-mass finite support search; no record or general-method claim"}
