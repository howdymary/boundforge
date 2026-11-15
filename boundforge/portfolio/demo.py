"""Replay actual witness and render a GitHub Actions artifact demo."""
import hashlib,json,os,pathlib,subprocess,sys
from decimal import Decimal,localcontext
from fractions import Fraction
H=pathlib.Path(__file__).resolve().parent;B=H/"results/2026-11-15/c51-certified";data=json.loads((B/"candidate.json").read_text());report=json.loads((B/"report.json").read_text())
results=[json.loads(subprocess.check_output([sys.executable,"-I",str(H/p),str(B/"candidate.json")]))for p in ["c51_bernstein.py","c51_taylor.py"]]
assert all(r["valid"]and Fraction(r["lower_bound"])==Fraction(data["lower_bound"])for r in results)
c=report["strict_comparisons"]["working-report"];gain=Fraction(c["certified_gain_over_actual_previous_function"]);assert gain>Fraction(128,10**19)
with localcontext()as ctx:
 ctx.prec=50;g=Decimal(gain.numerator)/Decimal(gain.denominator);old=Fraction(c["actual_previous_beta_upper"]);old_decimal=Decimal(old.numerator)/Decimal(old.denominator)
body="# Actual-witness replay\n\n**C51a > "+data["lower_bound"]+"**\n\nBoth independent whole-circle algorithms just passed on the saved exact witness; the infinite tail is included.\n\n"
body+="Previous actual-function beta upper bound: approximately "+str(old_decimal)+".\n\nCertified strict gain: at least "+str(g)+".\n\n"
body+="| Checker | Complete cover | Nodes | Maximum depth |\n|---|---|---:|---:|\n"
for name,r in zip(["Exact Bernstein polynomial","Direct trig Taylor"],results):body+="|"+name+"|pass|"+str(r["nodes"])+"|"+str(r["max_depth"])+"|\n"
body+="\nWitness SHA256: "+hashlib.sha256((B/"candidate.json").read_bytes()).hexdigest()+"\n\n"
body+="This is a tiny conventional parameter refinement, below the earlier structural pilot's gate. No new general method or external peer review is claimed. The public-source audit found no stronger applicable prior lower witness; global priority is scoped to that audit.\n\n[Full report](https://github.com/howdymary/boundforge/blob/main/boundforge/portfolio/RESULT.md) · [All120 targets ranked](https://github.com/howdymary/boundforge/blob/main/boundforge/portfolio/TARGET_RANKING.md)\n"
out=H/"demo-output";out.mkdir(exist_ok=True);(out/"README.md").write_text(body);(out/"checker-results.json").write_text(json.dumps(results,indent=2))
if os.environ.get("GITHUB_STEP_SUMMARY"):pathlib.Path(os.environ["GITHUB_STEP_SUMMARY"]).write_text(body)
print(body)
