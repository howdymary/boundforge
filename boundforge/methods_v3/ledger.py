"""Shared CAS reservations. Per user instruction, no balance/usage/dashboard probes."""
import base64,json,os,pathlib,subprocess,uuid
ROOT=pathlib.Path(__file__).resolve().parent
REPO="howdymary/boundforge";PATH="boundforge/methods_v3/provider-ledger.json"
def api(path,body=None):
 cmd=["gh","api","repos/"+REPO+"/"+path]
 if body is not None:cmd+=["--method","PUT","--input","-"]
 p=subprocess.run(cmd,input=None if body is None else json.dumps(body).encode(),capture_output=True,check=True)
 return json.loads(p.stdout)
def mutate(fn):
 for _ in range(4):
  d=api("contents/"+PATH);s=json.loads(base64.b64decode(d["content"]));v=fn(s)
  try:api("contents/"+PATH,{"message":"Account bounded methods campaign provider use","sha":d["sha"],"branch":"main","content":base64.b64encode((json.dumps(s,indent=2)+"\n").encode()).decode()});return v
  except subprocess.CalledProcessError:continue
 raise RuntimeError("ledger contention; no provider call authorized")
def reserve(provider,amount,label):
 spec=json.loads((ROOT/"budget.json").read_text());p=spec["providers"][provider];ident=uuid.uuid4().hex
 def change(s):
  used=sum(r["actual"]if r["actual"]is not None else r["amount"]for r in s["reservations"]if r["provider"]==provider)
  if not p["enabled"]or s["campaign"]!=spec["campaign"]or s["frozen"].get(provider)or amount<0 or used+amount>min(p["campaign_cap"],s["hard_caps"][provider])or used+amount+p["old_unresolved_hold"]+p.get("external_guard",0)>p["initial_balance"]:raise RuntimeError("reservation refused")
  s["reservations"].append({"id":ident,"provider":provider,"amount":amount,"actual":None,"label":label,"run_id":os.environ.get("GITHUB_RUN_ID")});return ident
 return mutate(change)
def settle(ident,cost):
 if cost is None:return
 def change(s):
  r=next(x for x in s["reservations"]if x["id"]==ident)
  if cost<0 or cost>r["amount"]:s["frozen"][r["provider"]]="receipt exceeds reservation";return False
  r["actual"]=cost;return True
 if not mutate(change):raise RuntimeError("unexpected cost; hold retained and provider frozen")
