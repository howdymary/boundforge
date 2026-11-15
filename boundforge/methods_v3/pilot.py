"""Development only: hard task pilot and paired-probe controls."""
import argparse,json,os,pathlib,statistics,time
from .tasks import make
from .search import episode
def main():
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);p.add_argument("--cpu",type=float,default=1);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
 specs=[("graph",n,700+i,d)for i,(n,d)in enumerate([(128,.12),(192,.15),(256,.08)])]+[("cap",d,0,0)for d in [4,5,6]]+[("deletion",n,0,0)for n in [8,9,10]]
 policies=["fixed"+str(a)for a in range(6)]+["schedule","random","ucb","alns","probe","shuffled_probe"];rows=[];build=[]
 for ti,spec in enumerate(specs):
  t=time.process_time();task=make(*spec);build.append({"task":task.name,"cpu":time.process_time()-t,"vertices":task.n,"edges":len(task.edges),"sha256":task.sha})
  for seed in [7101,7102,7103]:
   order=policies[(ti+seed)%len(policies):]+policies[:(ti+seed)%len(policies)]
   for policy in order:
    row=episode(task,policy,seed,a.cpu);rows.append(row);(out/"episodes.json").write_text(json.dumps(rows))
   print(json.dumps({"task":task.name,"seed":seed,"complete":len(rows)}),flush=True)
  summary={p:{"mean":statistics.mean(r["best"]for r in rows if r["task"]==task.name and r["policy"]==p),"cpu":sum(r["cpu"]for r in rows if r["task"]==task.name and r["policy"]==p)}for p in policies}
  print(json.dumps({"task":task.name,"summary":summary}),flush=True)
 report={"stage":"exploratory_development","source_sha":os.environ.get("GITHUB_SHA"),"run_id":os.environ.get("GITHUB_RUN_ID"),"budget_cpu_per_episode":a.cpu,"episodes":len(rows),"build":build,"total_episode_cpu":sum(r["cpu"]for r in rows),"gpu":0,"model_calls":0,"scope":"Different seeds are dependent repetitions; no held-out or novelty claim. Initial pilot allows one primitive overrun per quantum; actual CPU including verification reported."}
 (out/"report.json").write_text(json.dumps(report,indent=2))
if __name__=="__main__":main()
