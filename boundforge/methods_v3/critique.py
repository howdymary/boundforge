"""One bounded Tinker critique of mathematical mechanisms, never treated as proof."""
import argparse,json,os,pathlib
from .ledger import reserve
def main():
 import tinker
 from tinker.lib.retry_handler import RetryConfig
 from transformers import AutoTokenizer
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
 text=(pathlib.Path(__file__).parent/"collision/SPECIFICATION.md").read_text()
 prompt="Critically review the following proposed exact construction-search method. Identify actual mathematical counterexamples or missing hypotheses in (1) safe modular rank via Hadamard bounds, (2) generic nullspace embedding preserving collision partitions, (3) exact hitting-set characterization of protected-vector repair, (4) basis-dependent deletion neighborhoods. Then assess the potentially material difference: the controller changes an equivalent basis when a complete small-deletion failure certificate indicates a basis-limited obstruction, to enable a future construction move. Distinguish this from standard Freiman modeling, matroid circuits, matroid interdiction, basis exchange, ALNS and explanation-guided LNS. Do not assert novelty or experimental benefit. Suggest the strongest control or counterexample that would invalidate the mechanism. Return JSON with correctness_objections, prior_art_overlap, decisive_tests, claim_scope.\n\n"+text
 tok=AutoTokenizer.from_pretrained("Qwen/Qwen3.5-397B-A17B",trust_remote_code=False);ids=tok.apply_chat_template([{"role":"user","content":prompt}],tokenize=True,add_generation_prompt=True,enable_thinking=False);ids=list(ids["input_ids"])if hasattr(ids,"keys")else list(ids)
 if ids and isinstance(ids[0],list):ids=ids[0]
 assert len(ids)<=6000
 token=reserve("tinker",.1,"one critique of exact collision representation mechanism; hold retained")
 client=tinker.ServiceClient(display_name="BoundForge exact mechanism critical review")
 try:
  sampler=client.create_sampling_client(base_model="Qwen/Qwen3.5-397B-A17B",retry_config=RetryConfig(enable_retry_logic=False,progress_timeout=45)).result()
  r=sampler.sample(prompt=tinker.types.ModelInput.from_ints(ids),num_samples=1,sampling_params=tinker.types.SamplingParams(max_tokens=1800,temperature=.3,stop=["<|im_end|>"])).result();tokens=list(r.sequences[0].tokens);answer=tok.decode(tokens)
  result={"model":"Qwen/Qwen3.5-397B-A17B","input_tokens":len(ids),"output_tokens":len(tokens),"estimate_usd":len(ids)*1.65/1e6+len(tokens)*7.5/1e6,"unresolved_hold_usd":.1,"reservation":token,"raw_output":answer,"status":"unverified_review_not_independent_human_endorsement"}
  (out/"critique.json").write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items()if k!="raw_output"}),flush=True)
 finally:
  try:client.close("success").result()
  except Exception:pass
if __name__=="__main__":main()
