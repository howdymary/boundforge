"""Exact active-pair refinement and a scoped all-translations optimum certificate."""
import hashlib,json,os,pathlib,subprocess,sys,time
from fractions import Fraction
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"translation_optimum";OUT.mkdir(exist_ok=True)
def run(path,name):return json.loads(subprocess.check_output([sys.executable,"-I",str(HERE/name),str(path)]))
def ceildec(x,d=24):
 q,r=divmod(x.numerator*10**d,x.denominator);q+=bool(r);s=str(q).rjust(d+1,"0");return s[:-d]+"."+s[-d:]
def main():
 parent=HERE/"translation_certification";base=json.loads((parent/"baseline.json").read_text());previous=json.loads((parent/"report.json").read_text());h=base["heights_int"];n=base["n"];Q=base["Q"];S=sum(h);prefix=[0]
 for a in h:prefix.append(prefix[-1]+a)
 maxima=previous["records"]["candidate"]["prefix"]["positive_and_negative_maxima"];iterations=[]
 for iteration in range(8):
  pos=next(x["arg"] for x in maxima if x["arg"]["sign"]==1);neg=next(x["arg"] for x in maxima if x["arg"]["sign"]==-1)
  if pos["knot_mesh"]!="autocorrelation" or neg["knot_mesh"]!="autocorrelation":raise ValueError("active pair left registered fixed-grid derivation")
  mp=pos["index"];mn=neg["index"]
  cp=sum(h[i]*h[i+mp] for i in range(n-mp));cn=sum(h[i]*h[i+mn] for i in range(n-mn))
  ap=Q*prefix[n-mp]-cp;an=Q*(S-prefix[mn])-cn;sp=-Q*h[n-mp];sn=Q*h[mn]
  if sp==sn:raise ValueError("flat pair")
  t=Fraction(an-ap,sp-sn)
  if not -1<t<0:raise ValueError("active affine formula out of its cell")
  cert=base|{"translation_cells":[str(t.numerator),str(t.denominator)]};p=OUT/"candidate.json";p.write_text(json.dumps(cert));a=run(p,"c1b_translate_exact.py")
  maxima=a["positive_and_negative_maxima"];vp=int(maxima[0]["scaled_max"]);vn=int(maxima[1]["scaled_max"])
  iterations.append({"iteration":iteration,"positive_knot":mp,"negative_knot":mn,"constant_positive":str(ap),"constant_negative":str(an),"slope_positive":str(sp),"slope_negative":str(sn),"translation":str(t),"all_knots_positive_equals_negative":vp==vn})
  if vp==vn:break
 else:raise ValueError("no exactly balanced active pair")
 b=run(p,"c1b_translate_sweep.py");assert a["score"]==b["score"]
 old=Fraction(previous["records"]["baseline"]["prefix"]["score"]);new=Fraction(a["score"]);gain=old-new
 report={"run_id":os.environ["GITHUB_RUN_ID"],"source_sha":os.environ["GITHUB_SHA"],"candidate_sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"prefix_checker":a,"jump_checker":b,"gain_exact":str(gain),"gain_display":float(gain),"upper_bound_24dp":ceildec(new),"baseline_upper_24dp":ceildec(old),"iterations":iterations,"optimal_within_translation_family":True,"optimality_argument":"For positive lag x, overlap=prefix(n-x-t)-corr(x) is nonincreasing in translation t. For negative lag, overlap=mass-prefix(x-t)-corr(x) is nondecreasing. At this exact t, the maxima over all real positive and negative lags are equal. Every smaller t has positive-lag maximum at least this value; every larger t has negative-lag maximum at least this value. Thus this t globally minimizes the maximum over all admissible translations of this exact fixed height profile.","scope":"A standard monotonicity argument gives a witness-specific restricted-family optimum, not global optimality among all functions or a new general research method. Current world-record status still depends on the frontier audit."}
 (OUT/"report.json").write_text(json.dumps(report,indent=2));print("TRANSLATION_OPTIMUM "+json.dumps({k:v for k,v in report.items() if k not in ["prefix_checker","jump_checker"]}),flush=True)
if __name__=="__main__":main()
