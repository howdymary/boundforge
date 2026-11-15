"""One reasoning-enabled proposal after concrete failures. No generated code execution."""
import argparse,hashlib,json,pathlib,re,os
from .ledger import reserve
def strict_pairs(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError("duplicate JSON key")
  d[k]=v
 return d
def main():
 import tinker
 from tinker.lib.retry_handler import RetryConfig
 from transformers import AutoTokenizer
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
 root=pathlib.Path(__file__).parent
 evidence=(root/"RESULTS_SO_FAR.md").read_text();prior=(root/"PRIOR_ART.md").read_text()
 question="""Find ONE genuinely different, implementable methodological hypothesis, or return null if no defensible one emerges. We need a reusable research method for a precisely defined class of exactly checkable mathematical construction search, not a new name or benchmark.
Prior attempts: scalar same-state probes lost; paired signed order credit was algebraically the same as ordinary paired rewards; exact obstruction-guided neutral basis changes lost; shared counterfactual signatures reduced elimination but best-repair lost to random circuit search; exact rational event scans helped, but simple coordinate events often beat kernel/memory controllers.6084 complete projective-family certificates and218 cross-state reuses were independently verified, without a demonstrated memory advantage.
Do not suggest bandits, ALNS, routine subproblem caching, strong-branching imitation, ordinary CEGAR/nogood learning, gradient sensitivity, generic Bayesian information gain, LLM operator synthesis alone, batch evaluation, exact line search alone, or combining them as novelty. These are known.
Closest sources: Fialho adaptive operator selection; Ropke/Pisinger ALNS; FunSearch/AlphaEvolve; PatternBoost; Cuntz2020 arrangement greedy replacement; Avis/Fukuda reverse search; Eppstein parametric matroids; exact subproblem caching; parametric proof reuse; scientific-agent memory/SciMARS. Distinguish problem-specific mathematical reduction from a new general discovery method.
Look for a precise missing capability rather than a story: e.g. a mathematical condition that changes what a failed experiment can imply or what intervention can be guaranteed useful, or a fundamentally different source of search information. You must compare with the strongest simpler mechanism, state an explicit rejection criterion, and propose an inexpensive experiment that could fail. Do not invent citations or claim worldwide novelty. A useful negative theoretical result may be interesting, but it does not satisfy the user's method objective.
Think carefully, then give concise FINAL JSON (not your private reasoning) with: hypothesis (null or {mechanism,task_class,closest_prior_art,material_difference,formal_statement_or_counterexample,prediction,smallest_discriminating_experiment,strongest_baseline,resource_budget,stop_criterion}), why_previous_attempts_failed, novelty_objections. Use URLs only from supplied sources or mark a reference unverified. No generated program will be run automatically.
"""
 tok=AutoTokenizer.from_pretrained("Qwen/Qwen3.5-397B-A17B",trust_remote_code=False);ids=tok.apply_chat_template([{"role":"user","content":question+"\nMEASURED EVIDENCE:\n"+evidence+"\nSOURCED PRIOR ART:\n"+prior}],tokenize=True,add_generation_prompt=True,enable_thinking=True);ids=list(ids["input_ids"])if hasattr(ids,"keys")else list(ids)
 if ids and isinstance(ids[0],list):ids=ids[0]
 assert len(ids)<=18000
 token=reserve("tinker",.5,"one reasoning-enabled hypothesis after failed mechanisms; <=18000 input/20000 output; no training")
 client=tinker.ServiceClient(display_name="BoundForge reasoned alternative after falsification")
 try:
  sampler=client.create_sampling_client(base_model="Qwen/Qwen3.5-397B-A17B",retry_config=RetryConfig(enable_retry_logic=False,progress_timeout=300)).result()
  result=sampler.sample(prompt=tinker.types.ModelInput.from_ints(ids),num_samples=1,sampling_params=tinker.types.SamplingParams(max_tokens=20000,temperature=.6,stop=["<|im_end|>"])).result();tokens=list(result.sequences[0].tokens);decoded=tok.decode(tokens);has_final="</think>"in decoded
  final=decoded.rsplit("</think>",1)[-1]if has_final else "";final=re.sub(r"<\\|[^>]+\\|>","",final).strip()
  if final.startswith("```"):final=final.split("\n",1)[1].rsplit("```",1)[0].strip()
  try:parsed=json.loads(final,object_pairs_hook=strict_pairs)
  except ValueError:parsed=None
  obj={"model":"Qwen/Qwen3.5-397B-A17B","thinking_enabled":True,"input_tokens":len(ids),"output_tokens":len(tokens),"estimate_usd":len(ids)*1.65/1e6+len(tokens)*7.5/1e6,"unresolved_hold_usd":.5,"reservation":token,"private_reasoning_not_published":True,"full_output_sha256":hashlib.sha256(decoded.encode()).hexdigest(),"final_output":final,"parsed":parsed,"status":"unverified hypothesis, no novelty endorsement or generated code execution","source_sha":os.environ.get("GITHUB_SHA")}
  (out/"hypothesis.json").write_text(json.dumps(obj,indent=2));print(json.dumps({k:v for k,v in obj.items()if k not in ["final_output","parsed"]}),flush=True)
 finally:
  try:client.close("success").result()
  except Exception:pass
if __name__=="__main__":main()
