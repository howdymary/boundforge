"""Contextual operator selection; an adaptation of AOS, not an asserted new algorithm."""
import copy,math,random
LABELS=["pair","triple","mismatch","repeat","stalled","progress"]
def diagnosis(x,old_hash,new_hash,stale=0):
 if x.get("cardinality_rate_mismatches",0):return "mismatch"
 if new_hash==old_hash:return "repeat"
 if stale>=3:return "stalled"
 if x.get("tested",0) and x.get("rejected",0)/x["tested"]>.7:
  return "pair" if x.get("pair_rejected",0)>x.get("triple_rejected",0) else "triple"
 return "progress"
class Controller:
 def __init__(self,arm,freeze,seed):
  self.arm=arm;self.f=freeze;self.rng=random.Random(seed)
  self.context=copy.deepcopy(freeze["context"]);self.global_stats=[[0,0.] for _ in range(6)]
  self.history=[]
 def choose(self,label,step):
  ranks=self.f["rule"].get(label,list(range(6)))
  if self.arm=="fixed":return self.f["fixed"],{"policy":"development-selected fixed"}
  if self.arm=="scheduled":return step%6,{"policy":"fixed round-robin"}
  if self.arm=="no_memory":return ranks[0],{"policy":"frozen model rule; no persistent archive"}
  if self.arm=="ucb":stats=self.global_stats;key="global"
  else:
   key=self.rng.choice(LABELS) if self.arm=="shuffled" else label
   stats=self.context.setdefault(key,[[0,0.] for _ in range(6)])
  before=self.f["fixed"]
  if self.rng.random()<.15:a=self.rng.randrange(6);mode="epsilon exploration"
  else:
   count=sum(s[0] for s in stats)
   priorities=[s[1]/max(1,s[0])+.001*math.sqrt(math.log(count+2)/(s[0]+1)) for s in stats]
   if self.arm not in ["numeric","ucb"]:
    priorities=[v+1e-7*(6-ranks.index(i)) for i,v in enumerate(priorities)]
   a=max(range(6),key=lambda i:(priorities[i],-i));mode="empirical context UCB" if key!="global" else "global UCB"
  return a,{"policy":mode,"context_read":key,"archive_counts":[s[0] for s in stats],"counterfactual_fixed_action":before,"choice_differs_from_fixed":a!=before}
 def update(self,label,action,reward):
  for stats in [self.global_stats,self.context.setdefault(label,[[0,0.] for _ in range(6)])]:
   stats[action][0]+=1;stats[action][1]+=reward
