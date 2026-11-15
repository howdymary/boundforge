"""Controller behavior, exact acceptance, credential separation and credit integrity."""
import base64,copy,json,pathlib,threading
from fractions import Fraction as F
import pytest
from boundforge.autoresearch.policy import choose,diagnose
from boundforge.autoresearch.trace import Trace
from boundforge.autoresearch import remote_budget as rb
def memory(label="PRECISION_FLOOR",target="C51a",context="x"):
 return {"operator":"float_local","diagnosis":label,"event_id":"measured123","evidence":{"gain_in_ulps":1},"target":target,"context_sha256":context}
def test_evidence_changes_next_action_and_cites_memory():
 h=[memory()];action,why=choose(h,context={"target":"C51a","context_sha256":"x"})
 assert action=="precision_equioscillation"and why["retrieved"]==["measured123"]
 assert choose([memory("OPTIMIZER_FAILURE")])[0]=="precision_restart"
 assert choose(h,"fixed_float")[0]=="float_local"
 assert choose(h,"fixed_precision")[0]=="precision_equioscillation"
def test_irrelevant_failure_is_not_reused():
 action,why=choose([memory(target="OTHER")],context={"target":"C51a","context_sha256":"x"})
 assert action=="float_local"and why["retrieved"]==[]
def test_diagnosis_uses_measured_ulp_not_prose():
 label,ev=diagnose({"operator":"float_local","gain":"1e-16","ulp":"1e-16","explanation":"I proved no solution exists"})
 assert label=="PRECISION_FLOOR"and ev["gain_in_ulps"]==1
def test_trace_tamper_is_detected(tmp_path):
 tr=Trace(tmp_path);tr.add("probe",gain=1);tr.save({"status":"running"})
 assert len(Trace(tmp_path).events)==1
 p=tmp_path/"decisions.jsonl";p.write_text(p.read_text().replace('"gain":1','"gain":2'))
 with pytest.raises(ValueError):Trace(tmp_path)
class FakeGitHub:
 def __init__(self):
  self.state={"campaign":"submission-2026-11-15","initial_caps":{"exa":119.14},"hard_caps":{"exa":.25},"frozen":{},"reservations":[]};self.version=0
 def __call__(self,args,body=None):
  if body is None:return {"sha":str(self.version),"content":base64.b64encode(json.dumps(self.state).encode()).decode()}
  if body["sha"]!=str(self.version):raise rb.Refused("CAS conflict")
  self.state=json.loads(base64.b64decode(body["content"]));self.version+=1;return {}
SPEC={"campaign_cap":.25,"initial_cap":119.14,"old_unresolved_hold":2.46,"external_pending_guard":20}
def test_shared_ledger_counts_unknown_holds_and_never_pools_credits():
 g=FakeGitHub();rb.reserve("one","exa",.2,SPEC,119.14,"pending","a",g)
 with pytest.raises(rb.Refused):rb.reserve("two","exa",.1,SPEC,119.14,"new","b",g)
 rb.settle("one",None,g);assert g.state["reservations"][0]["actual"]is None
 rb.settle("one",.1,g);rb.reserve("two","exa",.1,SPEC,119.14,"new","b",g)
 assert len(g.state["reservations"])==2
def test_excessive_receipt_freezes_provider_without_releasing_hold():
 g=FakeGitHub();rb.reserve("one","exa",.05,SPEC,119.14,"pending","a",g)
 with pytest.raises(rb.Refused):rb.settle("one",.06,g)
 assert g.state["frozen"]["exa"]and g.state["reservations"][0]["actual"]is None
def test_new_credits_do_not_raise_initial_cap():
 g=FakeGitHub();g.state["initial_caps"]["exa"]=20
 with pytest.raises(rb.Refused):rb.reserve("one","exa",.05,{**SPEC,"initial_cap":1000},1000,"new","a",g)
def test_rigorous_acceptance_refuses_numerical_record_only(tmp_path):
 from boundforge.autoresearch.run import certificate
 bad={"K":"3.568185442233685","alpha":"3.961543111810228","lower_bound":"0.6","N":12};p=tmp_path/"bad.json";p.write_text(json.dumps(bad))
 with pytest.raises(ValueError):certificate(p,tmp_path,bad,"0")
def test_whole_loop_resume_and_changed_reference_refusal(tmp_path):
 from boundforge.autoresearch.run import main,HERE
 out=tmp_path/"loop"
 args=["--out",str(out),"--sandbox","process","--max-steps","3","--wall-seconds","60"]
 a=main(args);assert a["status"]=="certified_historical_replay"and len(a["experiments"])>=2
 b=main(args+["--resume"]);assert a==b
 new=json.loads((HERE/"frontier.json").read_text());new["incumbent"]["name"]="changed";q=tmp_path/"changed.json";q.write_text(json.dumps(new))
 with pytest.raises(ValueError):main(args+["--resume","--registry",str(q)])
