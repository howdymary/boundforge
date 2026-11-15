"""Evidence-conditioned experiment selection. Adaptation, not new algorithm."""
import math
def diagnose(result):
 if result.get("status")=="optimizer_failure":return "OPTIMIZER_FAILURE",{"error_type":result.get("error_type"),"detail":result.get("detail",result.get("reason"))}
 if result.get("candidate"):return "UNCERTIFIED_NUMERICAL_GAIN",{"gain":result["gain"],"precision":result["precision"],"claim_digits":result["claim_digits"],"tail_depth":result["tail_depth_selected"]}
 if result.get("operator")=="float_local":
  gain=float(result["gain"]);ulp=float(result["ulp"])
  if gain<=8*ulp:return "PRECISION_FLOOR",{"gain":result["gain"],"ulp":result["ulp"],"gain_in_ulps":gain/ulp,"criterion":"gain <=8 ulps; no exact improvement inferred"}
 if result.get("status")=="tail_budget_failure":return "TAIL_BUDGET_FAILURE",{"slack":result["slack"]}
 return "SAMPLED_STAGNATION",{"status":result.get("status"),"gain":result.get("gain"),"scope":"finite attempted procedure, not a proof of exhaustion"}
def choose(history,policy="diagnostic",context=None):
 if context is not None:history=[h for h in history if all(h.get(k)==v for k,v in context.items())]
 if policy=="fixed_float":return "float_local",{"reason":"fixed-float control","retrieved":[]}
 if policy=="fixed_precision":return "precision_equioscillation",{"reason":"strong fixed high-precision control","retrieved":[]}
 if not history:return "float_local",{"reason":"cheap local probe before paying higher-precision cost","retrieved":[]}
 last=history[-1];label=last["diagnosis"];retrieved=[r["event_id"]for r in history if r["diagnosis"]==label]
 if label in ["PRECISION_FLOOR","SAMPLED_STAGNATION","TAIL_BUDGET_FAILURE"]:action="precision_equioscillation"if sum(r["operator"]=="precision_equioscillation"for r in history)<2 else "precision_restart"
 elif label=="OPTIMIZER_FAILURE":action="precision_restart"
 elif label=="CERTIFICATION_FAILURE":action="precision_restart"
 else:action="precision_equioscillation"
 return action,{"reason":"measured "+label+" -> "+action,"retrieved":retrieved,"evidence":last["evidence"],"memory_scope":"same target and input hash only; no broad impossibility conclusion"}
