"""GitHub CAS is the cross-run credit ledger; never call a provider first."""
import base64,json,subprocess
PATH="boundforge/autoresearch/provider-ledger.json";REPO="howdymary/boundforge"
class Refused(RuntimeError):pass
def gh(args,body=None):
 p=subprocess.run(["gh","api",*args],input=None if body is None else json.dumps(body),capture_output=True,text=True)
 if p.returncode:raise Refused("GitHub ledger read/write refused")
 return json.loads(p.stdout)
def mutate(fn,client=gh):
 for attempt in range(3):
  d=client([f"repos/{REPO}/contents/{PATH}"]);state=json.loads(base64.b64decode(d["content"]));result=fn(state)
  body={"message":"Account bounded autonomous provider reservation","sha":d["sha"],"branch":"main","content":base64.b64encode((json.dumps(state,indent=2)+"\n").encode()).decode()}
  try:client([f"repos/{REPO}/contents/{PATH}","--method","PUT","--input","-"],body);return result
  except Refused:
   if attempt==2:raise
 raise Refused("ledger contention")
def reserve(ident,provider,amount,spec,observed,label,run_id,client=gh):
 def change(s):
  if s["campaign"]!="submission-2026-11-15"or s["frozen"].get(provider):raise Refused("campaign/provider frozen")
  if any(r["id"]==ident for r in s["reservations"]):return ident
  total=sum(r["actual"]if r["actual"]is not None else r["amount"]for r in s["reservations"]if r["provider"]==provider)
  cap=min(s["hard_caps"][provider],spec["campaign_cap"]);initial=min(s["initial_caps"][provider],spec["initial_cap"],observed)
  if amount<0 or total+amount>cap or total+amount+spec["old_unresolved_hold"]+spec["external_pending_guard"]>initial:raise Refused("shared credit limit")
  s["reservations"].append({"id":ident,"provider":provider,"amount":amount,"actual":None,"label":label,"run_id":run_id});return ident
 return mutate(change,client)
def settle(ident,cost,client=gh):
 if cost is None:return
 def change(s):
  rows=[r for r in s["reservations"]if r["id"]==ident]
  if len(rows)!=1:raise Refused("unknown reservation")
  r=rows[0]
  if cost<0 or cost>r["amount"]:
   s["frozen"][r["provider"]]="receipt exceeds reservation";return False
  r["actual"]=cost;return True
 if not mutate(change,client):raise Refused("excessive receipt; provider frozen")
