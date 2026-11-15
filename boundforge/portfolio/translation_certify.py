"""Fresh independent acceptance of a rational translation; not just its float probe."""
import hashlib,json,os,pathlib,subprocess,sys,time,urllib.request
from fractions import Fraction
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"translation_certification";OUT.mkdir(exist_ok=True)
def run(path,name):return json.loads(subprocess.check_output([sys.executable,"-I",str(HERE/name),str(path)]))
def main():
 start=time.monotonic();url="https://einsteinarena.com/api/solutions/best?problem_id=1&agent_name=Blob&limit=1";raw=urllib.request.urlopen(url).read();entry=json.loads(raw)[0];floats=entry["data"]["values"];h=[Fraction(float(x)) for x in floats];Q=max(x.denominator for x in h);ints=[int(x*Q) for x in h];delta=len(h)*Q//2-sum(ints);repair=delta
 for i,k in enumerate(ints):
  if not delta:break
  change=min(abs(delta),Q-k if delta>0 else k)
  if delta>0:ints[i]+=change;delta-=change
  else:ints[i]-=change;delta+=change
 assert delta==0
 baseline={"n":len(h),"Q":Q,"heights_int":ints,"translation_cells":["0","1"]};candidate=baseline|{"translation_cells":["-86849527570","1000000000000000000"]}
 records={}
 for label,cert in [("baseline",baseline),("candidate",candidate)]:
  path=OUT/(label+".json");path.write_text(json.dumps(cert))
  a=run(path,"c1b_translate_exact.py");b=run(path,"c1b_translate_sweep.py");assert a["score"]==b["score"]
  records[label]={"prefix":a,"jump_sweep":b,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
 old=Fraction(records["baseline"]["prefix"]["score"]);new=Fraction(records["candidate"]["prefix"]["score"]);gain=old-new
 # The project threshold excludes roundoff-scale representation changes.
 report={"source_sha":os.environ["GITHUB_SHA"],"run_id":os.environ["GITHUB_RUN_ID"],"records":records,"strict_improvement":gain>0,"project_record_candidate":gain>Fraction(1,10**12),"gain_exact":str(gain),"gain_display":float(gain),"old_display":float(old),"new_display":float(new),"source":{"url":url,"agent":entry["agentName"],"entry_id":entry["id"],"reported_float_score":str(entry["score"]),"raw_sha256":hashlib.sha256(raw).hexdigest(),"mass_repair":str(Fraction(repair,Q))},"verifier_source_sha256":{p:hashlib.sha256((HERE/p).read_bytes()).hexdigest() for p in ["c1b_translate_exact.py","c1b_translate_sweep.py","ntt.cpp"]},"elapsed_seconds":time.monotonic()-start,"scope":"Small real continuum construction improvement over the strongest publicly retrieved witness, subject to final frontier audit. Almost all bound strength belongs to Blob. Does not meet the Arena1e-7 submission threshold; no method novelty or publication significance claimed."}
 (OUT/"report.json").write_text(json.dumps(report,indent=2));print("TRANSLATION_CERTIFIED "+json.dumps({k:v for k,v in report.items() if k!="records"}),flush=True)
if __name__=="__main__":main()
