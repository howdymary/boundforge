"""Small paired functional comparison, not a general-method efficacy study."""
import json,pathlib,statistics,time
from .run import main as run
HERE=pathlib.Path(__file__).resolve().parent
def main():
 out=HERE/"comparison-output";out.mkdir(exist_ok=True);rows=[]
 for seed in [51301,51302,51303]:
  for policy in ["diagnostic","fixed_float","fixed_precision"]:
   path=out/(policy+"-"+str(seed));start=time.monotonic()
   r=run(["--out",str(path),"--sandbox","docker","--policy",policy,"--seed",str(seed),"--max-steps","3","--wall-seconds","60"])
   row={"seed":seed,"policy":policy,"status":r["status"],"accepted_bound":r["accepted"]["lower_bound"]if r["accepted"]else None,"experiments":len(r["experiments"]),"verified_external_reference_improvements":len(r["verified_reference_improvements"]),"continuation_goal":r["existing_project_result"]["lower_bound"],"loop_wall_seconds":r["elapsed_seconds"],"end_to_end_seconds":time.monotonic()-start,"worker_cpu_seconds":sum(json.loads((path/("result-"+str(i)+".json")).read_text()).get("cpu_seconds",0)for i in range(len(r["experiments"]))),"maximum_allowances":{"steps":3,"loop_wall_seconds":60},"providers_enabled":False}
   rows.append(row);(out/"rows.json").write_text(json.dumps(rows,indent=2))
 summary={"rows":rows,"medians":{p:{"loop_wall_seconds":statistics.median(r["loop_wall_seconds"]for r in rows if r["policy"]==p),"end_to_end_seconds":statistics.median(r["end_to_end_seconds"]for r in rows if r["policy"]==p),"successes":sum(r["status"]=="certified_historical_replay"for r in rows if r["policy"]==p)}for p in ["diagnostic","fixed_float","fixed_precision"]},"scope":"Same incumbent and3paired random seeds, not3independent math tasks or held-out instances. Common maximum allowances, actual CPU/wall and verification costs differ and are reported. Docker build is common setup. No claim of broad controller advantage; strongest fixed high-precision procedure is included."}
 (out/"summary.json").write_text(json.dumps(summary,indent=2));print(json.dumps(summary))
if __name__=="__main__":main()
