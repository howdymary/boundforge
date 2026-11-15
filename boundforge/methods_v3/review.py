"""Bounded Exa review. Only immutable source metadata/excerpts retained, no full paper redistribution."""
import base64,datetime as dt,hashlib,json,os,pathlib,subprocess,urllib.request,uuid
ROOT=pathlib.Path(__file__).resolve().parent
REPO="howdymary/boundforge";LEDGER="boundforge/methods_v3/provider-ledger.json"
def gh(path,body=None):
 cmd=["gh","api","repos/"+REPO+"/"+path]
 if body is not None:cmd+=["--method","PUT","--input","-"]
 p=subprocess.run(cmd,input=None if body is None else json.dumps(body).encode(),capture_output=True,check=True)
 return json.loads(p.stdout)
def mutate(fn):
 for _ in range(4):
  d=gh("contents/"+LEDGER);s=json.loads(base64.b64decode(d["content"]));v=fn(s)
  try:gh("contents/"+LEDGER,{"message":"Reserve bounded methods literature review","sha":d["sha"],"branch":"main","content":base64.b64encode((json.dumps(s,indent=2)+"\n").encode()).decode()});return v
  except subprocess.CalledProcessError:continue
 raise RuntimeError("ledger contention")
def reserve(label):
 spec=json.loads((ROOT/"budget.json").read_text());age=(dt.datetime.now(dt.timezone.utc)-dt.datetime.fromisoformat(spec["observed_ui_utc"].replace("Z","+00:00"))).total_seconds()/60
 if not 0<=age<=spec["valid_for_minutes"]:raise RuntimeError("stale balances")
 p=spec["providers"]["exa"];ident=uuid.uuid4().hex
 def f(s):
  used=sum(r["actual"]if r["actual"]is not None else r["amount"]for r in s["reservations"]if r["provider"]=="exa")
  if s["campaign"]!=spec["campaign"]or s["frozen"].get("exa")or not p["enabled"]or used+.05>min(p["campaign_cap"],s["hard_caps"]["exa"])or used+.05+p["old_unresolved_hold"]+p["external_guard"]>p["initial_balance"]:raise RuntimeError("budget refused")
  s["reservations"].append({"id":ident,"provider":"exa","amount":.05,"actual":None,"label":label,"run_id":os.environ.get("GITHUB_RUN_ID")});return ident
 return mutate(f)
def settle(ident,cost):
 def f(s):
  r=next(r for r in s["reservations"]if r["id"]==ident)
  if cost is None or cost<0 or cost>r["amount"]:s["frozen"]["exa"]="missing/excessive cost receipt";return False
  r["actual"]=cost;return True
 if not mutate(f):raise RuntimeError("unknown cost, stop")
def call(endpoint,payload):
 ident=reserve(endpoint+" "+str(payload)[:180])
 req=urllib.request.Request("https://api.exa.ai/"+endpoint,data=json.dumps(payload).encode(),headers={"x-api-key":os.environ["EXA_API_KEY"],"Content-Type":"application/json"})
 with urllib.request.urlopen(req,timeout=35)as r:d=json.load(r)
 settle(ident,d.get("costDollars",{}).get("total"))
 return {"endpoint":endpoint,"payload":payload,"request_id":d.get("requestId"),"cost":d.get("costDollars"),"results":[{"url":x.get("url"),"title":x.get("title"),"publishedDate":x.get("publishedDate"),"text_sha256":hashlib.sha256(x.get("text","").encode()).hexdigest(),"excerpt":x.get("text","")[:4200]}for x in d.get("results",[])]}
QUERIES=[
 "Research papers on adaptive operator selection adaptive large neighborhood search failure diagnostics Fialho Ropke Pisinger algorithm selection",
 "Research papers on exact local optimality certificates reused across search states parametric optimization no-good learning large neighborhood search",
 "Research papers on active algorithm selection probing information gathering value of information algorithm portfolios",
 "Research papers on adaptive representation change combinatorial optimization learned obstruction structure local search",
 "Research papers on joint optimization and rigorous certification interval arithmetic multi fidelity resource allocation",
 "FunSearch AlphaEvolve PatternBoost methods algorithm discovery evaluation ablations official papers",
 "Research papers on scientific agents failure memory counterfactual experiments scientific discovery transferable algorithms",
 "Research papers on proof carrying local search exact exchange neighborhoods symmetry no good reuse multi objective optimization"
]
def main():
 import argparse
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True);records=[]
 for q in QUERIES:
  r=call("search",{"query":q,"type":"auto","numResults":5,"contents":{"text":{"maxCharacters":10000}}});records.append(r)
  (out/"review.json").write_text(json.dumps({"research_date":"2026-11-15","sources_requested":len(records)*5,"records":records},indent=2))
  print(json.dumps({"query":q,"cost":r["cost"],"urls":[x["url"]for x in r["results"]]}),flush=True)
if __name__=="__main__":main()
