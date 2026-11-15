"""Replay witnesses and every retained complete-family memory certificate."""
import argparse,hashlib,io,json,pathlib,subprocess,zipfile
from fractions import Fraction as Q
from .certify import verify,verify_intervals
from .verify_family import check_family,rank
def main():
 p=argparse.ArgumentParser();p.add_argument("--artifact",type=int,required=True);p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
 raw=subprocess.check_output(["gh","api",f"repos/howdymary/boundforge/actions/artifacts/{a.artifact}/zip"]);z=zipfile.ZipFile(io.BytesIO(raw))
 def episodes():
  for name in z.namelist():
   if name.startswith("group-"):yield from json.loads(z.read(name))
 families=[];chains=[];hits=0;cross=0;count=0
 for r in episodes():
  count+=1
  c=verify(r["witness"]);d=verify_intervals(r["witness"]);lo,hi=map(Q,c["ratio_interval"]);l,u=map(Q,d["ratio_interval_rational"]);assert max(lo,l)<=min(hi,u)
  task=r["task"];byturn={e["turn"]:e for e in r["trace"]};checked={}
  for e in r["trace"]:
   if "record_written"in e:
    key=e["record_written"]
    result=check_family(task["m"],task["controls"],e)
    if key in checked:assert result["best_key"]==checked[key]["best_key"]
    checked[key]=result
    families.append({"task":task,"policy":r["policy"],"seed":r["seed"],"turn":e["turn"],"record":key,"event_sha256":hashlib.sha256(json.dumps(e,sort_keys=True).encode()).hexdigest(),"check":result})
   if e.get("diagnosis")=="certified_projective_family_covered":
    hits+=1;cross+=bool(e.get("cross_state_reuse"));source=byturn[e["record_origin_turn"]];key=source["record_written"];assert key==e["record_retrieved"]and key in checked
    assert tuple(checked[key]["best_key"])<=tuple(e["current_key"])
    # Compare the actual row spaces over Q, independently of their modular hashes.
    m=task["m"];dimen=2*(m-1);public=[]
    for aa,bb in task["controls"]:
     for i in range(m):
      for j in range(i):
       v=[0]*dimen
       for at,sgn in [(i,1),(j,-1)]:
        if at:v[2*(at-1)]+=aa*sgn;v[2*(at-1)+1]+=bb*sgn
       public.append(v)
    union=[public[i]for i in set(source["retained_basis_ids"]+e["retained_basis_ids"])];assert rank(union)==dimen-2
    next_event=next((n for n in r["trace"]if n["turn"]>e["turn"]and n.get("triggered_by_record")==key),None)
    chains.append({"policy":r["policy"],"task":task,"seed":r["seed"],"retrieval_turn":e["turn"],"source_turn":source["turn"],"cross_state":e.get("cross_state_reuse",False),"decision":e["decision_changed"],"intervention_turn":None if next_event is None else next_event["turn"],"released_rows":None if next_event is None else next_event.get("released_basis_rows"),"measured_global_best_improved":None if next_event is None else tuple(next_event["best_key"])>tuple(e["best_key"]),"scope":"Measured next consequence, not an isolated causal effect or general advantage"})
 report={"artifact_id":a.artifact,"artifact_sha256":hashlib.sha256(raw).hexdigest(),"episodes":count,"all_witnesses_reverified_by_two_arithmetic_backends":True,"retained_complete_family_certificates":len(families),"all_complete_families_independently_verified":True,"memory_hits":hits,"cross_state_hits":cross,"chains":len(chains),"new_method_claim":False,"record_claim":False}
 (out/"family-checks.json").write_text(json.dumps(families,indent=2));(out/"memory-chains.json").write_text(json.dumps(chains,indent=2));(out/"report.json").write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
if __name__=="__main__":main()
