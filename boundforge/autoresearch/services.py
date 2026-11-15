"""Optional in-loop Exa frontier gate and bounded Tinker operator selection.
Read-only provider usage; no purchases/reloads/training; uncertain charges stay held.
"""
import csv,datetime as dt,hashlib,io,json,os,pathlib,re,sqlite3,subprocess,sys,time,urllib.request,uuid
from fractions import Fraction as F
HERE=pathlib.Path(__file__).resolve().parent
MODEL="Qwen/Qwen3.5-397B-A17B"
class Disabled(RuntimeError):pass
def http(url,key,payload,timeout=25):
 req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={"x-api-key":key,"Content-Type":"application/json"})
 with urllib.request.urlopen(req,timeout=timeout)as r:return json.load(r)
class Services:
 def __init__(self,out,trace):
  self.out=out;self.trace=trace;self.spec=json.loads((HERE/"provider-budget.json").read_text());self.db=sqlite3.connect(str(out/"provider-budget.sqlite"));self.db.execute("create table if not exists reservations(id text primary key,provider text,amount real,actual real,label text)");self.db.commit();self.used=False;self.cache=None
  stamp=dt.datetime.fromisoformat(self.spec["observed_ui_utc"].replace("Z","+00:00"));age=(dt.datetime.now(dt.timezone.utc)-stamp).total_seconds()/60
  if age<0 or age>self.spec["valid_for_minutes"]:raise Disabled("provider UI snapshot stale; paid calls disabled")
 def reserve(self,p,amount,label):
  s=self.spec["providers"][p]
  if not s["enabled"]:raise Disabled("provider disabled")
  observed=s["initial_cap"]
  if p=="tinker":
   end=(dt.datetime.now(dt.timezone.utc).replace(minute=0,second=0,microsecond=0)+dt.timedelta(hours=1)).isoformat().replace("+00:00","Z")
   raw=subprocess.check_output(["tinker","billing","usage","2026-11-15T00:00:00Z",end,"--csv","-"],timeout=30)
   rows=list(csv.DictReader(io.StringIO(raw.decode())))
   if rows and "estimated_cost_usd"not in rows[0]:raise Disabled("unknown live cost schema")
   observed-=sum(float(r.get("estimated_cost_usd")or 0)for r in rows)
  self.db.execute("begin immediate");used=self.db.execute("select coalesce(sum(coalesce(actual,amount)),0)from reservations where provider=?",(p,)).fetchone()[0]
  if amount<0 or used+amount>s["campaign_cap"]or used+amount+s["old_unresolved_hold"]+s["external_pending_guard"]>observed:self.db.rollback();raise Disabled("credit guard refuses")
  ident=uuid.uuid4().hex;self.db.execute("insert into reservations values(?,?,?,?,?)",(ident,p,amount,None,label));self.db.commit();self.trace.add("provider_reservation",id=ident,provider=p,amount=amount,label=label);return ident
 def settle(self,ident,actual):
  held=self.db.execute("select amount from reservations where id=?",(ident,)).fetchone()[0]
  if actual is None:return
  if not 0<=actual<=held:raise Disabled("unexpected cost, retain hold and stop")
  self.db.execute("update reservations set actual=?where id=?",(actual,ident));self.db.commit()
 def source_entry(self,x):
  text=x.get("text")or"";values=sorted(set(re.findall(r"0\.58[0-9]{4,}",text)))
  return {"url":x.get("url"),"title":x.get("title"),"text_sha256":hashlib.sha256(text.encode()).hexdigest(),"observed_lower_region_numbers":values,"registered_pair_visible":bool(re.search(r"3\.568185442233685",text)and re.search(r"3\.961543111810228",text))}
 def research_and_choose(self,last,default,registry):
  if self.used:return self.cache or{}
  self.used=True
  if not os.environ.get("EXA_API_KEY"):raise Disabled("Exa key missing")
  token=self.reserve("exa",.05,"one in-loop frontier search, at most5results")
  response=http("https://api.exa.ai/search",os.environ["EXA_API_KEY"],{"query":"Erdos problem513 maximum-term constant certified lower bound working report 0.585078819674","type":"lite","numResults":5,"contents":{"text":{"maxCharacters":5000}}})
  cost=response.get("costDollars",{}).get("total");self.settle(token,cost)
  entries=[self.source_entry(x)for x in response.get("results",[])];request_ids=[response.get("requestId")]
  if not any(x["registered_pair_visible"]for x in entries):
   token=self.reserve("exa",.05,"one frontier witness contents lookup")
   more=http("https://api.exa.ai/contents",os.environ["EXA_API_KEY"],{"urls":[registry["incumbent"]["source"]],"text":{"maxCharacters":16000}})
   self.settle(token,more.get("costDollars",{}).get("total"));request_ids.append(more.get("requestId"));entries.extend(self.source_entry(x)for x in more.get("results",[]))
  matched=any(e["registered_pair_visible"]for e in entries)
  source_id=self.trace.add("exa_frontier_gate",source_entries=entries,request_ids=request_ids,registered_witness_confirmed=matched,decision_consequence="permit higher-precision experiment"if matched else"stop; registered frontier not confirmed",scope="source confirmation, not proof that no stronger result exists")
  if not matched:self.cache={"frontier_review_required":True,"source_event":source_id};return self.cache
  advisory={"action":default,"source_event":source_id,"frontier_review_required":False}
  if os.environ.get("TINKER_API_KEY"):
   token=self.reserve("tinker",.05,"single bounded operator-choice inference")
   payload={"diagnosis":last["diagnosis"],"evidence":last["evidence"],"source_entries":entries,"default":default,"operators":["float_local","precision_equioscillation","precision_restart"]}
   # The model is a separate bounded provider process. It cannot edit code.
   p=subprocess.run([sys.executable,"-I",str(HERE/"tinker_choice.py")],input=json.dumps(payload),capture_output=True,text=True,timeout=60,env={k:v for k,v in os.environ.items()if k in ["PATH","TINKER_API_KEY","HF_HOME"]})
   if p.returncode:raise Disabled("inference failed; unresolved hold retained")
   r=json.loads(p.stdout);estimate=r["input_tokens"]*1.65/1e6+r["output_tokens"]*7.5/1e6
   if estimate>.05:raise Disabled("inference exceeds reservation")
   # No itemized receipt: the reservation stays unresolved, estimate is separate.
   eid=self.trace.add("tinker_operator_proposal",model=MODEL,result=r,estimated_usd=estimate,unresolved_hold=.05,source_event=source_id)
   if r["action"]in payload["operators"]:advisory.update(action=r["action"],model_event=eid)
  self.cache=advisory;return advisory
 def summary(self):
  return {p:{"reserved_or_actual":self.db.execute("select coalesce(sum(coalesce(actual,amount)),0)from reservations where provider=?",(p,)).fetchone()[0],"campaign_cap":s["campaign_cap"],"old_hold":s["old_unresolved_hold"],"enabled":s["enabled"]}for p,s in self.spec["providers"].items()}
