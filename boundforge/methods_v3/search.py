"""Bounded primitive search, identical operators for every policy."""
import math,random,time
from .tasks import bits
ACTIONS=["ruin5","ruin20","ruin50","anchor1","anchor2","restart"]
def greedy(task,s,rng,counters):
 order=list(range(task.n));rng.shuffle(order)
 for v in order:
  if s>>v&1:continue
  counters["tested"]+=1
  if task.legal(v,s):s|=1<<v
 return s
def hitting(blockers,limit):
 if not blockers:return 0
 if limit<=0:return None
 e=min(blockers,key=int.bit_count);best=None
 for v in bits(e):
  bit=1<<v;r=hitting([x for x in blockers if not x&bit],limit-1)
  if r is not None:
   cand=bit|r
   if best is None or cand.bit_count()<best.bit_count():best=cand
 return best
def step(task,s,action,rng,counters):
 if action==5:return greedy(task,0,rng,counters)
 if action<3:
  frac=[.05,.2,.5][action];chosen=list(bits(s));k=min(len(chosen),max(1,round(len(chosen)*frac)))
  for v in rng.sample(chosen,k):s^=1<<v
 else:
  outside=[v for v in range(task.n)if not s>>v&1]
  if not outside:return s
  anchors=rng.sample(outside,min(len(outside),action-2));base=0
  for v in anchors:
   if not task.legal(v,base):return s
   base|=1<<v
  blocks=[]
  for v in anchors:blocks.extend(task.blockers(v,s))
  if len(anchors)==2:
   # Hyperedges with both anchors create additional one-vertex removals.
   for e in task.edges:
    if e&base==base and (e^base)&s==e^base:blocks.append(e^base)
  remove=hitting(blocks,6)
  if remove is None:return s
  s=(s&~remove)|base
 return greedy(task,s,rng,counters)
def quantum(task,s,action,seed,allowance):
 rng=random.Random(seed);start=time.process_time();c={"tested":0,"steps":0};best=s;current=s
 while time.process_time()-start<allowance:
  current=step(task,current,action,rng,c);c["steps"]+=1
  if current.bit_count()>best.bit_count():best=current
  elif current.bit_count()<best.bit_count()-max(2,best.bit_count()//5):current=best
 assert task.valid(best)
 return {"state":best,"score":best.bit_count(),"cpu":time.process_time()-start,**c}
def episode(task,policy,seed,budget=1.0):
 from .tasks import independent_check
 start=time.process_time();wall=time.monotonic();rng=random.Random(seed);counts=[0]*6;sums=[0.0]*6;weights=[1.0]*6;totaltests=totalsteps=0;overhead=0.0;trace=[]
 c={"tested":0};state=greedy(task,0,rng,c);initial=state.bit_count();best=state;timebest=time.process_time()-start;totaltests+=c["tested"];turn=0
 while time.process_time()-start<budget-.005:
  before=state;left=budget-(time.process_time()-start);probe=[];decision_start=time.process_time()
  if policy in ["probe","shuffled_probe"]:
   for a in range(6):
    allowance=min(.004,max(0,(budget-(time.process_time()-start))*.05))
    if allowance<=0:break
    r=quantum(task,before,a,seed*100003+turn*101+a,allowance);probe.append((a,r));totaltests+=r["tested"];totalsteps+=r["steps"]
   if len(probe)<6:break
   ranking=sorted(probe,key=lambda x:(x[1]["score"],-x[1]["cpu"]),reverse=True)
   action=ranking[0][0]if policy=="probe"else rng.randrange(6)
   state=max([state]+[r["state"]for a,r in probe],key=int.bit_count)
   evidence={"saved_state":str(before),"probe_scores":[r["score"]for a,r in probe],"probe_cpu":[r["cpu"]for a,r in probe],"chosen_from_measured_ranking":policy=="probe"}
  elif policy.startswith("fixed"):action=int(policy[-1]);evidence={}
  elif policy=="schedule":action=turn%6;evidence={}
  elif policy=="random":action=rng.randrange(6);evidence={}
  elif policy=="ucb":
   action=next((a for a in range(6)if counts[a]==0),max(range(6),key=lambda a:sums[a]/max(1,counts[a])+math.sqrt(2*math.log(turn+2)/max(1,counts[a])));evidence={"counts":list(counts),"rewards":list(sums)}
  elif policy=="alns":
   action=rng.choices(range(6),weights=weights)[0];evidence={"weights":list(weights)}
  else:raise ValueError(policy)
  overhead+=time.process_time()-decision_start-sum(r["cpu"]for a,r in probe)
  allowance=min(.035,max(0,budget-(time.process_time()-start)))
  if allowance<=0:break
  r=quantum(task,state,action,seed*7777+turn,allowance);totaltests+=r["tested"];totalsteps+=r["steps"];gain=max(0,r["score"]-before.bit_count())
  counts[action]+=1;sums[action]+=gain;weights[action]=.8*weights[action]+.2*(1+gain)
  # Preserve current and best separately; bounded deterioration permits exploration.
  state=r["state"]
  if state.bit_count()>best.bit_count():best=state;timebest=time.process_time()-start
  trace.append({"turn":turn,"action":ACTIONS[action],"before":before.bit_count(),"after":state.bit_count(),"best":best.bit_count(),"gain":gain,"evidence":evidence,"cpu":time.process_time()-start,"quantum_cpu":r["cpu"]})
  turn+=1
 checkstart=time.process_time();verified=independent_check(task,best);verifycpu=time.process_time()-checkstart
 return {"task":task.name,"kind":task.kind,"task_sha256":task.sha,"policy":policy,"seed":seed,"initial":initial,"best":best.bit_count(),"best_state":str(best),"cpu":time.process_time()-start,"wall":time.monotonic()-wall,"time_to_best_cpu":timebest,"decision_overhead_cpu":overhead,"verification_cpu":verifycpu,"tested":totaltests,"primitive_steps":totalsteps,"trace":trace,"check":verified}
