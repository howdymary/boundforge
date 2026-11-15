"""Descriptive development analysis; does not retune frozen policies."""
import collections,hashlib,json,pathlib,statistics
from controller import diagnosis
HERE=pathlib.Path(__file__).resolve().parent
def analyze(rows):
 def digest(s):return hashlib.sha256(json.dumps(sorted(s)).encode()).hexdigest()
 examples=[]
 for row in rows:
  p=row["probe"];examples.append({"group":(row["task"]["id"],row["state_index"]),"label":diagnosis(p,digest(row["state"]),digest(p["state"]),0),"rewards":[max(0,x["best_score"]-p["score"])/max(1,p["score"]) for x in row["interventions"]]})
 result=[]
 for x in examples:
  train=[y for y in examples if y["group"]!=x["group"]]
  global_means=[statistics.mean(y["rewards"][a] for y in train) for a in range(6)]
  glob=max(range(6),key=lambda a:(global_means[a],-a))
  local=[y for y in train if y["label"]==x["label"]]
  means=[statistics.mean(y["rewards"][a] for y in local) for a in range(6)] if local else global_means
  context=max(range(6),key=lambda a:(means[a],global_means[a],-a))
  result.append({"task":x["group"][0],"state":x["group"][1],"diagnosis":x["label"],"global_action":glob,"diagnostic_action":context,"global_reward":x["rewards"][glob],"diagnostic_reward":x["rewards"][context]})
 return {"scope":"Post-hoc development diagnostic utility only; leave one saved-state block out, three seeds per block. Not broad family hold-out, preregistered validation or causal proof. All six interventions have equal CPU and identical post-probe starts within each row.","labels":dict(collections.Counter(x["label"] for x in examples)),"global_mean":statistics.mean(x["global_reward"] for x in result),"diagnostic_mean":statistics.mean(x["diagnostic_reward"] for x in result),"different_actions":sum(x["global_action"]!=x["diagnostic_action"] for x in result),"different_reward_rows":sum(abs(x["global_reward"]-x["diagnostic_reward"])>1e-14 for x in result),"rows":result}
if __name__=="__main__":
 print(json.dumps(analyze(json.loads((HERE/"results/pilot/paired.json").read_text())),indent=2))
