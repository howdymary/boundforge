"""Fit only on development interventions and publish an immutable evaluation contract."""
import collections,hashlib,json,os,pathlib,shutil,statistics,sys
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"freeze";OUT.mkdir(exist_ok=True)
from controller import LABELS,diagnosis
from tasks import digest
from budget import Ledger
from services import exa,write,read
def main():
 previous=HERE/"pilot";shutil.copyfile(previous/"budget.sqlite",OUT/"budget.sqlite")
 ledger=Ledger(OUT);events=[]
 def log(kind,payload):
  e={"kind":kind,**payload};events.append(e);(OUT/"trace.jsonl").write_text("\n".join(map(json.dumps,events))+"\n");print("C49_FREEZE_EVENT "+json.dumps(e),flush=True)
 rows=json.loads((previous/"paired.json").read_text());context={label:[[0,0.] for _ in range(6)] for label in LABELS};examples=[];global_gains=[[] for _ in range(6)]
 for row in rows:
  probe=row["probe"];label=diagnosis(probe,digest(row["state"]),digest(probe["state"]),0)
  for x in row["interventions"]:
   reward=max(0,x["best_score"]-probe["score"])/max(1,probe["score"])
   context[label][x["action"]][0]+=1;context[label][x["action"]][1]+=reward;global_gains[x["action"]].append(reward)
  examples.append({"task":row["task"]["id"],"diagnosis":label,"outcomes":[{"action":x["action"],"reward":max(0,x["best_score"]-probe["score"])/max(1,probe["score"])} for x in row["interventions"]]})
 fixed=max(range(6),key=lambda a:(statistics.mean(global_gains[a]),-a))
 summary={"context":context,"mean_reward":[statistics.mean(x) for x in global_gains],"fixed_action":fixed,"pilot_variance":[statistics.pstdev(x) for x in global_gains],"note":"F10 did not improve; uniform8 showed action-dependent gains. Two development families only."}
 log("development_summary",summary)
 # A new in-loop literature question after the measured pilot, supplied to actual policy proposals.
 sources=exa(ledger,"adaptive operator selection constraint rejection diagnosis ruin recreate neighborhood selection combinatorial search Ropke Pisinger Fialho",log)
 snippets=[{"url":x["url"],"title":x["title"],"excerpt":(x.get("text") or "")[:650]} for x in sources]
 from model_policy import propose
 try:rules=propose(ledger,summary,snippets,log)
 except Exception as e:rules=[];log("model_unavailable",{"error":type(e).__name__,"detail":str(e)[:180]})
 def value(rule):
  return sum(next(x["reward"] for x in ex["outcomes"] if x["action"]==rule[ex["diagnosis"]][0]) for ex in examples)/len(examples)
 numerical={k:sorted(range(6),key=lambda a:(-(context[k][a][1]/max(1,context[k][a][0])),-statistics.mean(global_gains[a]),a)) for k in LABELS}
 selected=max(rules,key=value) if rules else numerical
 log("rule_selection",{"valid_model_rules":len(rules),"model_development_values":[value(r) for r in rules],"numerical_development_value":value(numerical),"selection_scope":"development only; model hypothesis, not established advantage"})
 # Both roles write and read; only source-presence/hashes are public.
 source=write(ledger,"experimenter",json.dumps({"recommended_action":fixed,"summary":summary}),log)
 recalled=read(ledger,"controller",source,log)
 source2=write(ledger,"controller",json.dumps({"recommendation_used":recalled,"fixed":fixed,"rule":selected,"scope":"development selection only"}),log)
 read(ledger,"experimenter",source2,log)
 freeze={"source_sha":os.environ["GITHUB_SHA"],"run_id":os.environ["GITHUB_RUN_ID"],"pilot_run":"43679514101","paired_archive_sha256":hashlib.sha256((previous/"paired.json").read_bytes()).hexdigest(),
 "rule":selected,"numerical_rule":numerical,"context":context,"fixed":fixed,"model_rules":rules,"summary":summary,
 "memory_source_present":recalled,"seeds":[410,420,430,440,450,460,470],"steps":24,"quantum_cpu_ms":250,
 "arms":["fixed","scheduled","ucb","no_memory","full","numeric","shuffled"],
 "heldout_tasks":["H11","uniform9","MIS64-a","MIS64-b","cap4"],
 "scope":"35 task/start pairs; seeds are not independent mathematical problems. Transfer adapters differ; no broad generalization guarantee.",
 "code_hashes":{p:hashlib.sha256((HERE/p).read_bytes()).hexdigest() for p in ["controller.py","episode.py","worker.py","search.cpp","tasks.py"]}}
 (OUT/"freeze.json").write_text(json.dumps(freeze,indent=2));(OUT/"report.json").write_text(json.dumps({"freeze":freeze,"ledger":ledger.summary()},indent=2))
 print("C49_FREEZE_FINAL "+json.dumps(freeze|{"ledger":ledger.summary()}),flush=True)
if __name__=="__main__":main()
