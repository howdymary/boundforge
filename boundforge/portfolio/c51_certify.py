"""Certify a changed exact witness and compare actual previous functions."""
import hashlib,json,os,pathlib,subprocess,sys,time
from fractions import Fraction as F
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"c51certificate";OUT.mkdir(exist_ok=True)
def main():
 start=time.monotonic()
 new={"name":"BoundForge conventional parameter refinement","K":"3.56818544223368269553925743732750636848","alpha":"3.96154311181022808045648786109191322475","lower_bound":"0.58507881967451359","N":12}
 baseline={"name":"Working report w042,2026-07-31","K":"3.568185442233685","alpha":"3.961543111810228","lower_bound":"0.585078819674513546608465623886","N":12,"source":"https://erdosproblemaday.com/report/513"}
 old={"name":"Roehrig PR184","K":"3.5681854310698435","alpha":"3.9615431126097391","lower_bound":"0.585078819674464320841496314106","N":12,"source":"https://github.com/AndreRoehrig/optimization-constants-certificates/tree/ed6387399cf6de02eaa4cf10c43787633496619a"}
 results={}
 for name,data in [("candidate",new),("working-report",baseline),("roehrig",old)]:
  p=OUT/(name+".json");p.write_text(json.dumps(data,indent=2));results[name]={}
  for checker in ["c51_bernstein.py","c51_taylor.py"]:
   r=json.loads(subprocess.check_output([sys.executable,"-I",str(HERE/checker),str(p)],timeout=300));assert r["valid"]
   results[name][checker]=r;(OUT/(name+"-"+checker+".json")).write_text(json.dumps(r,indent=2));print("C51_CERT "+json.dumps({"witness":name,"checker":checker,"nodes":r["nodes"]}),flush=True)
 # A pointwise lower modulus bound gives an upper bound on the ACTUAL old beta,
 # preventing a claim based only on a previous printed truncation.
 from c51_bernstein import witness_upper
 comparison={}
 for label,data,theta in [("working-report",baseline,"0.64554155199259506060314756447091421655"),("roehrig",old,"0.64554155451825961284896142167022979531")]:
  ub=min(witness_upper(data,"0"),witness_upper(data,theta));gain=F(new["lower_bound"])-ub;assert gain>0
  comparison[label]={"actual_previous_beta_upper":str(ub),"certified_gain_over_actual_previous_function":str(gain),"theta_tested":["0",theta]}
 report={"run_id":os.environ["GITHUB_RUN_ID"],"source_sha":os.environ["GITHUB_SHA"],"candidate":new,"candidate_sha256":hashlib.sha256((OUT/"candidate.json").read_bytes()).hexdigest(),"checks":results,"strict_comparisons":comparison,"seconds":time.monotonic()-start,"scope":"Tiny conventional changed-parameter lower-bound refinement; below original1e-9 pilot gate and not a periodic-extension success. No general-method novelty or parameter-global-optimum claim. Literature priority remains scoped to audited public sources."}
 (OUT/"report.json").write_text(json.dumps(report,indent=2));print("C51_CERT_FINAL "+json.dumps({"certified":True,"bound":new["lower_bound"],"seconds":report["seconds"]}),flush=True)
if __name__=="__main__":main()
