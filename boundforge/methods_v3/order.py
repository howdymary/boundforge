"""Counterfactual ordering pilot. Standard sequence methods are explicit controls."""
import argparse,collections,hashlib,itertools,json,math,os,pathlib,random,statistics,time
from .search import ACTIONS,greedy,step
from .tasks import make,independent_check
PAIRS=list(itertools.permutations(range(6),2))
UNORDERED=list(itertools.combinations(range(6),2))
def batch(task,state,action,seed,steps=4):
 rng=random.Random(seed);best=state;c={"tested":0};started=time.process_time()
 for _ in range(steps):
  state=step(task,state,action,rng,c)
  if state.bit_count()>best.bit_count():best=state
 assert task.valid(state)and task.valid(best)
 return {"state":state,"best":best,"score":best.bit_count(),"cpu":time.process_time()-started,"tested":c["tested"],"primitives":steps}
def join_best(*rows):return max((r["best"]for r in rows),key=int.bit_count)
def crossover(task,state,a,b,seed):
 ra=seed*1009+a;rb=seed*1009+b
 sa=batch(task,state,a,ra);sb=batch(task,state,b,rb)
 ab=batch(task,sa["state"],b,rb);ba=batch(task,sb["state"],a,ra)
 bestab=join_best(sa,ab);bestba=join_best(sb,ba);base=state.bit_count()
 return {"ab":ab,"ba":ba,"best":join_best(sa,sb,ab,ba),"bestab":bestab,"bestba":bestba,"single_scores":[sa["score"],sb["score"]],"order_scores":[bestab.bit_count(),bestba.bit_count()],"contrast":bestab.bit_count()-bestba.bit_count(),"enabling":max(sa["score"],sb["score"])<=base<max(bestab.bit_count(),bestba.bit_count()),"cpu":sum(r["cpu"]for r in [sa,sb,ab,ba]),"tested":sum(r["tested"]for r in [sa,sb,ab,ba]),"primitives":16}
def run(task,policy,seed,budget,fixed):
 begin=time.process_time();wall=time.monotonic();rng=random.Random(seed);c={"tested":0};state=greedy(task,0,rng,c);best=state;initial=state.bit_count();counts=[0]*30;values=[0.0]*30;paircounts=[0]*15;diff=[0.0]*15;absab=[0.0]*15;absba=[0.0]*15;singlecounts=[0]*6;singlevalues=[0.0]*6;trans=collections.defaultdict(lambda:[0.0,0]);previous=0;previous_success=False;stagnant=0;trace=[];tested=c["tested"];primitives=0;selected=0;enabling=0;prediction=[]
 while time.process_time()-begin<budget:
  old=state;oldscore=old.bit_count();turn=len(trace);base_seed=seed*100003+turn*1777;start=time.process_time();detail={};pi=None
  if policy in ["paired_order","shuffled_order","paired_absolute"]and stagnant>=2:
   pi=max(range(15),key=lambda i:(math.inf if not paircounts[i]else max(absab[i],absba[i])/paircounts[i]+math.sqrt(2*math.log(turn+2)/paircounts[i])))
   a,b=UNORDERED[pi];n=paircounts[pi];predicted=(a,b)if n==0 or diff[pi]>=0 else(b,a)
   q=crossover(task,old,a,b,base_seed);enabling+=int(q["enabling"]);paircounts[pi]+=1;absab[pi]+=max(0,q["order_scores"][0]-oldscore);absba[pi]+=max(0,q["order_scores"][1]-oldscore)
   if n and q["contrast"]:prediction.append({"correct":(predicted==(a,b))==(q["contrast"]>0),"previous_samples":n,"observed_contrast":q["contrast"]})
   contrast=q["contrast"]*(-1 if policy=="shuffled_order"and rng.random()<.5 else 1);diff[pi]+=contrast
   if policy=="paired_absolute":orientation=(a,b)if absab[pi]>=absba[pi]else(b,a)
   else:orientation=(a,b)if diff[pi]>=0 else(b,a)
   chosen=q["ab"]if orientation==(a,b)else q["ba"];state=chosen["state"]
   if q["best"].bit_count()>best.bit_count():best=q["best"]
   tested+=q["tested"];primitives+=q["primitives"];selected+=1
   detail={"probe":True,"saved_state":str(old),"unordered_pair":[a,b],"single_scores":q["single_scores"],"order_scores":q["order_scores"],"enabling":q["enabling"],"observed_contrast":q["contrast"],"credited_contrast":contrast,"samples":paircounts[pi],"chosen_orientation":orientation,"probe_cpu":q["cpu"],"prior_prediction":predicted,"retained_best":q["best"].bit_count()}
  else:
   if policy.startswith("fixed:"):pair=tuple(map(int,policy.split(":")[1].split(",")))
   elif policy=="fixed":pair=tuple(fixed)
   elif policy=="pair_ucb":
    pending=[i for i in range(30)if not counts[i]]
    idx=pending[0]if pending else max(range(30),key=lambda i:values[i]/counts[i]+math.sqrt(2*math.log(turn+2)/counts[i]));pair=PAIRS[idx]
   elif policy=="conditional":
    row=[trans[(previous,previous_success,a)]for a in range(6)]
    pending=[a for a in range(6)if not row[a][1]]
    a=pending[0]if pending else max(range(6),key=lambda a:row[a][0]/row[a][1]+math.sqrt(2*math.log(turn+2)/row[a][1]));pair=(a,)
   elif policy=="epsilon":
    pending=[a for a in range(6)if not singlecounts[a]]
    a=pending[0]if pending else(rng.randrange(6)if rng.random()<.1 else max(range(6),key=lambda a:singlevalues[a]/singlecounts[a]));pair=(a,)
   else:pair=tuple(fixed)
   path=[]
   for a in pair:
    q=batch(task,state,a,base_seed+a);path.append(q);state=q["state"];tested+=q["tested"];primitives+=q["primitives"]
    if q["best"].bit_count()>best.bit_count():best=q["best"]
   endscore=max(r["score"]for r in path);gain=max(0,endscore-oldscore)
   if len(pair)==2:
    idx=PAIRS.index(pair);counts[idx]+=1;values[idx]+=gain
   a=pair[-1];singlecounts[a]+=1;singlevalues[a]+=gain;entry=trans[(previous,previous_success,a)];entry[0]+=gain;entry[1]+=1
   previous=a;previous_success=bool(gain);detail={"probe":False,"pair":pair,"path_scores":[r["score"]for r in path]}
  progressed=best.bit_count()>initial if not trace else best.bit_count()>trace[-1]["best"]
  stagnant=0 if progressed else stagnant+1
  if state.bit_count()<best.bit_count()-max(2,best.bit_count()//8):state=best
  trace.append({"turn":turn,"before":oldscore,"current":state.bit_count(),"best":best.bit_count(),"cpu":time.process_time()-begin,"intervention_cpu":time.process_time()-start,"detail":detail})
 search_cpu=time.process_time()-begin;v=time.process_time();check=independent_check(task,best);verify=time.process_time()-v
 return {"task":task.name,"task_sha256":task.sha,"kind":task.kind,"policy":policy,"seed":seed,"initial":initial,"best":best.bit_count(),"best_state":str(best),"search_cpu":search_cpu,"verification_cpu":verify,"total_cpu":time.process_time()-begin,"wall":time.monotonic()-wall,"tested":tested,"primitive_steps":primitives,"paired_interventions":selected,"enabling_observations":enabling,"orientation_predictions":prediction,"trace":trace,"check":check}
def main():
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True);dev=[]
 for spec in [("graph",160,9201,.14),("cap",4,0,0),("deletion",8,0,0)]:
  task=make(*spec)
  for pair in PAIRS:
   for seed in [8101,8102]:dev.append(run(task,"fixed:"+",".join(map(str,pair)),seed,.15,pair))
  (out/"development.json").write_text(json.dumps(dev))
 tasks=sorted(set(r["task"]for r in dev));scores={}
 for pair in PAIRS:
  pol="fixed:"+",".join(map(str,pair));scores[pair]=sum(statistics.mean((r["best"]-r["initial"])/max(1,r["initial"])for r in dev if r["policy"]==pol and r["task"]==t)for t in tasks)
 fixed=max(PAIRS,key=lambda p:scores[p]);freeze={"selected_pair":fixed,"development_score":scores[fixed],"rule":"equal-task mean fractional gain; max across30 fixed pairs; development only","source_sha":os.environ.get("GITHUB_SHA")}
 (out/"selected-fallback.json").write_text(json.dumps(freeze,indent=2));print("FALLBACK "+json.dumps(freeze),flush=True)
 rows=[];policies=["fixed","pair_ucb","conditional","epsilon","paired_order","shuffled_order","paired_absolute"]
 for ti,spec in enumerate([("graph",224,9301,.1),("graph",288,9302,.06),("cap",5,0,0),("deletion",10,0,0)]):
  start=time.process_time();task=make(*spec);buildcpu=time.process_time()-start
  for seed in range(8201,8206):
   shift=(ti+seed)%len(policies);order=policies[shift:]+policies[:shift]
   for pol in order:
    rows.append(run(task,pol,seed,2,fixed));(out/"validation.json").write_text(json.dumps(rows))
   print(json.dumps({"task":task.name,"seed":seed,"rows":len(rows),"build_cpu":buildcpu}),flush=True)
 report={"stage":"exploratory_validation","run_id":os.environ.get("GITHUB_RUN_ID"),"source_sha":os.environ.get("GITHUB_SHA"),"development_episodes":len(dev),"validation_episodes":len(rows),"fixed_pair":fixed,"development_cpu":sum(r["total_cpu"]for r in dev),"validation_cpu":sum(r["total_cpu"]for r in rows),"novelty":"Unestablished; sequence learning and enabling are prior art. The crossover estimator and its usefulness are hypotheses.","summaries":{t:{pol:{"mean":statistics.mean(r["best"]for r in rows if r["task"]==t and r["policy"]==pol),"values":[r["best"]for r in rows if r["task"]==t and r["policy"]==pol],"cpu":sum(r["total_cpu"]for r in rows if r["task"]==t and r["policy"]==pol),"enabling":sum(r["enabling_observations"]for r in rows if r["task"]==t and r["policy"]==pol)}for pol in policies}for t in sorted(set(r["task"]for r in rows))}}
 (out/"report.json").write_text(json.dumps(report,indent=2));print("REPORT "+json.dumps(report),flush=True)
if __name__=="__main__":main()
