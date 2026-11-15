"""Reusable controller evaluation with task-specific validity and score adapters."""
import json,hashlib,math
from controller import Controller,diagnosis
from worker import quantum
def digest(s):return hashlib.sha256(json.dumps(sorted(s)).encode()).hexdigest()
def episode(task,freeze,arm,seed,steps=24,ms=250):
 state=task["state"];ctrl=Controller(arm,freeze,seed);trace=[];stale=0;label="progress"
 # Equal common warm-up protocol; all arms charge its actual CPU.
 warm=quantum(task,state,0,seed,ms);state=warm["state"];best=warm["best_score"];best_family=warm["best_family"];ports=warm["best_ports"]
 initial=max(warm["initial_score"],1);cpu=warm["cpu_seconds"];tested=warm["tested"]
 label=diagnosis(warm,digest(task["state"]),digest(state),0)
 for step in range(steps):
  a,why=ctrl.choose(label,step);old=digest(state);before=best
  x=quantum(task,state,a,seed*100000+step,ms);state=x["state"];cpu+=x["cpu_seconds"];tested+=x["tested"]
  if x["best_score"]>best+1e-14:best=x["best_score"];best_family=x["best_family"];ports=x["best_ports"]
  reward=max(0,best-before)/initial
  ctrl.update(label,a,reward);stale=stale+1 if reward<=0 else 0
  newlabel=diagnosis(x,old,digest(state),stale)
  trace.append({"step":step,"diagnosis":label,"next_diagnosis":newlabel,"action":a,"decision":why,"before_hash":old,"after_hash":digest(state),"best_score":best,"current_score":x["score"],"reward":reward,"cpu_seconds":x["cpu_seconds"],"wall_seconds":x["wall_seconds"],"tested":x["tested"],"rejected":x["rejected"],"pair_rejected":x.get("pair_rejected"),"triple_rejected":x.get("triple_rejected"),"last_conflict":x.get("last_conflict"),"termination":"bounded CPU quantum"})
  label=newlabel
 return {"task":task["id"],"kind":task["kind"],"n":task["n"],"param":task["param"],"arm":arm,"seed":seed,"initial_score":warm["initial_score"],"warm_score":warm["best_score"],"best_score":best,"best_family":best_family,"ports":ports,"cpu_seconds":cpu,"tested":tested,"trace":trace}
