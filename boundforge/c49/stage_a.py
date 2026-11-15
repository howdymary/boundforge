"""Remote frontier replay and literature discovery; no model or Modal work."""
import datetime as dt,hashlib,json,pathlib,subprocess,os,sys,time,urllib.request
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"artifacts";OUT.mkdir(exist_ok=True)
PIN="a50021b04687719f4a2ea27609029982c980573e";REPO="rpinho/math-certificates"
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"BoundForge"}),timeout=90) as r:return r.read()
def main():
 start=time.monotonic();sources={}
 def fetch(path):
  raw=get(f"https://raw.githubusercontent.com/{REPO}/{PIN}/c49/round1/{path}")
  p=OUT/"replay"/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
  sources[path]={"url":f"https://github.com/{REPO}/blob/{PIN}/c49/round1/{path}","sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw)}
  return p
 # Data and separately implemented primary checkers are transient remote replay inputs.
 cert=fetch("certificates/best_1.5678643845728069793620.json")
 producer=fetch("checker.py");independent=fetch("referee/independent.cpp")
 data=json.loads(cert.read_text());masks=OUT/"replay/candidate.masks";masks.write_text("\n".join(map(str,data["masks"]))+"\n")
 results={}
 for label,cmd in [("primary_box_checker",[sys.executable,str(producer),str(cert)]),("primary_bdd_checker",["bash","-c",'g++ -O3 -std=c++17 "$1" -o "$2" && "$2" "$3"',"replay",str(independent),str(OUT/"replay/independent"),str(masks)])]:
  t=time.monotonic();r=subprocess.run(cmd,capture_output=True,text=True,timeout=1200)
  (OUT/(label+".log")).write_text(r.stdout+"\n"+r.stderr)
  if r.returncode:raise RuntimeError(label+" failed; see artifact")
  results[label]={"output":json.loads(r.stdout),"elapsed_seconds":time.monotonic()-t}
 # Our independently implemented finite-family BDD check and exact rate isolation.
 r=subprocess.run(["g++","-O3","-std=c++17",str(HERE/"verify_bdd.cpp"),"-o",str(OUT/"own_bdd")],capture_output=True,text=True,check=True)
 t=time.monotonic();r=subprocess.run([str(OUT/"own_bdd"),str(cert)],capture_output=True,text=True,timeout=1200)
 # Own checker expects plain masks plus explicit n/ports.
 if r.returncode:
  r=subprocess.run([str(OUT/"own_bdd"),str(masks),"28","0","1"],capture_output=True,text=True,timeout=1200)
 if r.returncode:raise RuntimeError("own exact checker failed: "+r.stderr[:300])
 results["boundforge_bdd"]={"output":json.loads(r.stdout),"elapsed_seconds":time.monotonic()-t}
 from exact import rate_interval
 result=results["boundforge_bdd"]["output"];assert result["valid"] and result["counts"]==[33980,64728,64728,88867]
 results["rate"]=rate_interval(result["counts"],26)
 # Fresh public frontier evidence (includes open and merged updates).
 run=subprocess.run(["gh","api","search/issues","--method","GET","-f","q=repo:teorth/optimizationproblems is:pr sunflower","-f","sort=updated","-f","order=desc","-f","per_page=20"],capture_output=True,text=True,check=True)
 issues=json.loads(run.stdout);(OUT/"frontier.json").write_text(json.dumps({"timestamp":dt.datetime.now(dt.timezone.utc).isoformat(),"query":issues["total_count"],"claims":[{k:x.get(k) for k in ["number","title","html_url","updated_at","state","body"]} for x in issues["items"]]},indent=2))
 # Bounded Exa discovery after verified campaign balance snapshot.
 queries=[
 "adaptive large neighborhood search Ropke Pisinger 2006 adaptive operator selection original paper",
 "algorithm selection Rice 1976 instance features contextual bandit hyper heuristic Fialho adaptive operator selection",
 "learning from failure constraint acquisition nogood learning combinatorial search explanation guided large neighborhood search",
 "FunSearch AlphaEvolve PatternBoost failure memory adaptive search operator selection original papers",
 "sunflower free capacity 1.567864384572806979 49a new construction",
 "counterfactual algorithm selection paired interventions diagnostic feedback combinatorial optimization"
 ]
 events=[];total=0
 for q in queries:
  assert total+.1<=1
  payload={"query":q,"type":"auto","numResults":5,"contents":{"text":{"maxCharacters":6500}}}
  req=urllib.request.Request("https://api.exa.ai/search",data=json.dumps(payload).encode(),headers={"x-api-key":os.environ["EXA_API_KEY"],"Content-Type":"application/json"})
  with urllib.request.urlopen(req,timeout=60) as rr:r=json.load(rr)
  cost=r.get("costDollars",{}).get("total")
  if cost is None or not 0<=cost<=.1:raise RuntimeError("Exa accounting unknown; stop discovery")
  total+=cost
  event={"query":q,"request_id":r.get("requestId"),"cost_usd":cost,"results":[{"title":x.get("title"),"url":x.get("url"),"text":x.get("text",""),"publishedDate":x.get("publishedDate")} for x in r.get("results",[])]}
  events.append(event);print("C49_EXA "+json.dumps(event),flush=True)
  # Full copyrighted text stays transient; publication retains source metadata and hashes.
 (OUT/"exa-working.json").write_text(json.dumps(events))
 public=[{**e,"results":[{k:v for k,v in x.items() if k!="text"}|{"text_sha256":hashlib.sha256(x["text"].encode()).hexdigest()} for x in e["results"]]} for e in events]
 (OUT/"sources.json").write_text(json.dumps(public,indent=2))
 report={"source_sha":os.environ["GITHUB_SHA"],"run_id":os.environ["GITHUB_RUN_ID"],"witness_source_commit":PIN,"sources":sources,"replay":results,"exa_cost_usd":total,"elapsed_seconds":time.monotonic()-start,"new_record":False,"scope":"Reproduction of prior art, not a BoundForge discovery."}
 (OUT/"stage_a_report.json").write_text(json.dumps(report,indent=2));print("C49_STAGE_A "+json.dumps(report),flush=True)
if __name__=="__main__":main()
