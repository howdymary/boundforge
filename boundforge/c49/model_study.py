"""Exploratory model component study; never changes the frozen held-out policies."""
import hashlib,json,os,pathlib,shutil,statistics,subprocess
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"model_study";OUT.mkdir(exist_ok=True)
from budget import Ledger
from model_policy import propose
from services import exa,read
from controller import diagnosis
from tasks import digest
def main():
 shutil.copyfile(HERE/"evaluation/budget.sqlite",OUT/"budget.sqlite");ledger=Ledger(OUT)
 freeze=json.loads((HERE/"freeze/freeze.json").read_text());rows=json.loads((HERE/"pilot/paired.json").read_text());events=[]
 def log(kind,payload):
  e={"kind":kind,**payload};events.append(e);(OUT/"trace.jsonl").write_text("\n".join(map(json.dumps,events))+"\n");print("C49_MODEL_EVENT "+json.dumps(e),flush=True)
 # Inspect CLI contract read-only; failures cannot expose API credentials.
 r=subprocess.run(["tinker","billing","usage","--help"],capture_output=True,text=True)
 log("billing_cli_contract",{"returncode":r.returncode,"help":r.stdout[:2500]})
 sources=exa(ledger,"Ropke Pisinger adaptive operator selection rejection constraints large neighborhood search diagnostic memory",log)
 snippets=[{"url":x["url"],"title":x["title"],"excerpt":(x.get("text") or "")[:500]} for x in sources]
 # A production follow-up uses the remembered development record, if actually retrieved.
 recalled=read(ledger,"model_researcher","boundforge-c49-43679935507-controller",log)
 summary=freeze["summary"]|{"archived_controller_source_present":recalled}
 try:rules=propose(ledger,summary,snippets,log);error=None
 except Exception as e:
  rules=[];error={"type":type(e).__name__,"detail":str(e)[:200]}
  if isinstance(e,subprocess.CalledProcessError):error["stderr"]=(e.stderr or "")[:1000]
  log("model_unavailable",error)
 def value(rule):
  vals=[]
  for row in rows:
   p=row["probe"];label=diagnosis(p,digest(row["state"]),digest(p["state"]))
   a=rule[label][0];x=row["interventions"][a];vals.append(max(0,x["best_score"]-p["score"])/max(1,p["score"]))
  return statistics.mean(vals)
 report={"source_sha":os.environ["GITHUB_SHA"],"run_id":os.environ["GITHUB_RUN_ID"],"rules":rules,"valid_rules":len(rules),"development_values":[value(r) for r in rules],"numerical_development_value":value(freeze["numerical_rule"]),"frozen_evaluation_changed":False,"scope":"Exploratory component check on development data only; not evidence of held-out model advantage.","error":error,"ledger":ledger.summary()}
 (OUT/"report.json").write_text(json.dumps(report,indent=2));print("C49_MODEL_FINAL "+json.dumps(report),flush=True)
if __name__=="__main__":main()
