"""Recover reporting from retained completed work; never rerun billable searches."""
import argparse,hashlib,io,json,pathlib,statistics,subprocess,zipfile
from .certify import verify,verify_intervals
def safe_ratio(numerator,denominator):return numerator/denominator if denominator>0 else None
def main():
 p=argparse.ArgumentParser();p.add_argument("--artifact",type=int,required=True);p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
 raw=subprocess.check_output(["gh","api",f"repos/howdymary/boundforge/actions/artifacts/{a.artifact}/zip"]);z=zipfile.ZipFile(io.BytesIO(raw));rows=[];timings=[]
 for name in z.namelist():
  d=json.loads(z.read(name))
  if name.startswith("group-"):rows.extend(d)
  elif name.startswith("timing-"):timings.append(d)
 assert len(rows)==120 and len(timings)==8
 for r in rows:
  r["replayed_check"]=verify(r["witness"]);r["replayed_second_check"]=verify_intervals(r["witness"])
 summaries={}
 for m in [8,12,16]:
  for k in [4,5]:
   summaries[str(m)+"-"+str(k)]={}
   for policy in ["batch_repair","naive_best_repair","circuit","coordinate"]:
    rr=sorted([r for r in rows if r["task"]["m"]==m and len(r["task"]["controls"])==k and r["policy"]==policy],key=lambda r:r["seed"])
    assert len(rr)==5
    summaries[str(m)+"-"+str(k)][policy]={"values":[r["best_ratio"]for r in rr],"mean":statistics.mean(r["best_ratio"]for r in rr),"cpu":sum(r["total_cpu"]for r in rr),"proposals":sum(r["proposals"]for r in rr),"repair_subsets_checked":sum(r["repair_subsets_checked"]for r in rr)}
 pairs=[]
 for r in timings:
  shared=r["results"]["True"];naive=r["results"]["False"];assert shared["flat"]==naive["flat"]and shared["event"]["counterfactual_records"]==naive["event"]["counterfactual_records"]
  pairs.append({"spec":r["spec"],"naive_cpu":naive["cpu"],"shared_cpu":shared["cpu"],"speedup":safe_ratio(naive["cpu"],shared["cpu"]),"timing_caution":"CPU clock quantized near10ms; zero denominator is below resolution, not infinite speedup","subsets":shared["event"]["repair_subsets_checked"],"exact_family_equal":True})
 report={"original_run_id":"43752478807","original_source_sha":"0e73726321ec7809007869d8a962c161967c31a8","artifact_id":a.artifact,"artifact_sha256":hashlib.sha256(raw).hexdigest(),"original_workflow_status":"failure after completed experiments due to zero CPU timing division","recovery":"report rebuilt from complete saved files; witnesses replayed through both checkers; no billable experiments rerun","episodes":len(rows),"all_reverified":all(r["replayed_check"]["valid"]and r["replayed_second_check"]["valid"]for r in rows),"worker_total_cpu":sum(r["total_cpu"]for r in rows),"max_search_cpu_overshoot":max(r["search_cpu"]-2 for r in rows),"timing_pairs":pairs,"summaries":summaries,"modal_hold_usd":6.4,"new_method_claim":False,"record_claim":False}
 (out/"report.json").write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
if __name__=="__main__":main()
