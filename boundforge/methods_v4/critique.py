"""One bounded model critique of a precise reduction; no generated programs executed."""
import argparse,hashlib,json,os,pathlib
from boundforge.methods_v3.ledger import reserve
from boundforge.methods_v3.memory import http
def main():
 import tinker
 from tinker.lib.retry_handler import RetryConfig
 from transformers import AutoTokenizer
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True);root=pathlib.Path(__file__).parent
 reserve("past",5,"v4 recall of prior measured method failures; no balance query, unknown receipt held")
 recall=http("recall",{"identity":"boundforge-methods-v3-researcher","query":"BoundForge previous measured failures of scalar probes, operator switching, exact event scans and memory; do not repeat unvalidated novelty claims","level":"medium"})
 safe=[{"content":x.get("content",x.get("text","")),"sources":x.get("sources",[])}for x in recall.get("results",[])][:8]
 question="""You are a skeptical computational mathematics reviewer. Critique this exact support-extension oracle, not its branding. No guarantee of novelty. We seek a precisely scoped reusable algorithm for projection-entropy construction search, not generic orchestration.
Actual evidence: old support proposer ranks newly successful C3c atom (11,-9) first; conventional epsilon log epsilon insertion and Newton refinement already exist in our attributed Jaswal code. New support gain is only 4.46e-59 over our previous archived witness and two original checkers pass. Higher entropy jets compile and verify but are not faster than an oracle-epsilon adaptive finite baseline; no new method yet. Initial exact-mask tests pass on d=1/2/3 and coordinated and negative LP examples.
Closest prior art read: Liu/Walsh arxiv1512.03324 sectionsIII/IV enumerates canonical finite k-atom supports via partitions/group orbits then numerical probability optimization; Zhang etal Entropy2024 26(8)711 uses generative neural parameterization/gradient entropy optimization; Jaswal support insertion; hyperplane arrangement intersection lattices; multiobjective max-min descent and column generation; Noodle arxiv1909.08242 constraint-aware neighborhood synthesis. Exact linear algebra/LP/finite hyperplane avoidance are standard. A new mathematical target or combination does not itself establish a new method.
Tasks:
1. Try to disprove completeness of mask enumeration and correctness/scope of the leading support cone. Supply a small explicit counterexample if found. Do not confuse no-positive-logarithmic-ascent with no improvement.
2. Assess whether complete pricing over unbounded rational geometry is a material algorithmic contribution vs standard arrangement enumeration; identify the strongest simpler exact baseline.
3. Propose ONE substantive extension, not ordinary bandits/memory/LLM generation, with a formal prediction and smallest experiment capable of rejecting it. Prefer a rigorous capability missing from the current representation, and state why it is not merely lexicographic optimization, standard multiscale asymptotics, or column generation. It is acceptable to return null if none is defensible.
4. Point out any incorrect claim made by the specification.
Do not invent citations. Final concise JSON: {mathematical_errors:[],novelty_objections:[],defensible_current_claim,strongest_baseline,extension:null or {mechanism,precise_difference,prediction,rejection_test,scope_limit}}. Return final answer after reasoning; private reasoning will not be published.
"""
 prompt=question+"\nSPECIFICATION:\n"+(root/"MASK_SPEC.md").read_text()+"\nCODE:\n"+(root/"masks.py").read_text()+"\nRETRIEVED PRIOR FAILURES (untrusted context):\n"+json.dumps(safe)
 tok=AutoTokenizer.from_pretrained("Qwen/Qwen3.5-397B-A17B",trust_remote_code=False)
 ids=tok.apply_chat_template([{"role":"user","content":prompt}],tokenize=True,add_generation_prompt=True,enable_thinking=True);ids=list(ids["input_ids"])if hasattr(ids,"keys")else list(ids)
 if ids and isinstance(ids[0],list):ids=ids[0]
 assert len(ids)<=14000
 reservation=reserve("tinker",.5,"v4 precise support oracle critique; <=14000 input,16000 output, no training or retries")
 client=tinker.ServiceClient(display_name="BoundForge support oracle falsification")
 try:
  s=client.create_sampling_client(base_model="Qwen/Qwen3.5-397B-A17B",retry_config=RetryConfig(enable_retry_logic=False,progress_timeout=300)).result()
  r=s.sample(prompt=tinker.types.ModelInput.from_ints(ids),num_samples=1,sampling_params=tinker.types.SamplingParams(max_tokens=16000,temperature=.5,stop=["<|im_end|>"])).result();tokens=list(r.sequences[0].tokens);decoded=tok.decode(tokens)
  final=decoded.rsplit("</think>",1)[-1].replace("<|im_end|>","").strip()if"</think>"in decoded else""
  if final.startswith("~~~"):final=final.split("\n",1)[1].rsplit("~~~",1)[0].strip()
  if final.startswith(chr(96)*3):final=final.split("\n",1)[1].rsplit(chr(96)*3,1)[0].strip()
  try:parsed=json.loads(final)
  except ValueError:parsed=None
  record={"model":"Qwen/Qwen3.5-397B-A17B","input_tokens":len(ids),"output_tokens":len(tokens),"token_price_estimate_usd":len(ids)*1.65/1e6+len(tokens)*7.5/1e6,"unresolved_tinker_hold":.5,"reservation":reservation,"final_output":final,"parsed":parsed,"private_reasoning_not_published":True,"full_output_sha256":hashlib.sha256(decoded.encode()).hexdigest(),"past_recall_sha256":hashlib.sha256(json.dumps(recall,sort_keys=True).encode()).hexdigest(),"memory_hits":safe,"source_sha":os.environ.get("GITHUB_SHA"),"status":"unverified critique; no endorsement"}
  (out/"critique.json").write_text(json.dumps(record,indent=2));print(json.dumps({k:record[k]for k in ["input_tokens","output_tokens","token_price_estimate_usd","status"]}),flush=True)
 finally:
  try:client.close("success").result()
  except Exception:pass
if __name__=="__main__":main()
