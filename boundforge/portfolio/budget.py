"""Single-controller atomic reservations, live account usage checks, no billing mutations."""
import csv,datetime as dt,io,json,os,pathlib,sqlite3,subprocess,time,urllib.request,uuid
HERE=pathlib.Path(__file__).resolve().parent
def http(url,key,payload=None,header="Authorization"):
 req=urllib.request.Request(url,data=None if payload is None else json.dumps(payload).encode(),headers={header:("Bearer " if header=="Authorization" else "")+key,"Content-Type":"application/json"})
 with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)
class Ledger:
 def __init__(self,out):
  self.snapshot=json.loads((HERE/"campaign-budget.json").read_text());self.db=sqlite3.connect(str(out/"budget.sqlite"));self.db.execute("create table if not exists reservations(id text,provider text,amount real,actual real,label text)")
  for row in [("initial-connector-exa","exa",1.65,None,"unresolved Exa connector research allowance"),("supplemental-exa","exa",.25,None,"additional primary-source check reserved outside active Modal phase")]:
   if not self.db.execute("select 1 from reservations where id=?",(row[0],)).fetchone():self.db.execute("insert into reservations values(?,?,?,?,?)",row)
  self.db.commit()
 def reserve(self,p,amount,label):
  s=self.snapshot["providers"][p];observed=s["initial_cap"]
  if p=="modal":
   r=subprocess.run(["modal","billing","summary","--json"],capture_output=True,text=True,check=True,timeout=45);usage=json.loads(r.stdout)
   observed-=max(0,float(usage["metered_cost"])-s["metered_at_start"])
  elif p=="past":
   r=http("https://api.past.dev/api/v1/usage",os.environ["PAST_API_KEY"])
   if r["month"]["from"]!=s["period"]:raise RuntimeError("past accounting period changed")
   observed=min(r["balance"]["left"],s["initial_cap"]-max(0,r["balance"]["spent"]-s["spent_at_start"]))
  elif p=="tinker":
   end=(dt.datetime.now(dt.timezone.utc).replace(minute=0,second=0,microsecond=0)+dt.timedelta(hours=1)).isoformat().replace("+00:00","Z")
   r=subprocess.run(["tinker","billing","usage","2026-11-14T00:00:00Z",end,"--csv","-"],capture_output=True,text=True,check=True,timeout=45)
   rows=list(csv.DictReader(io.StringIO(r.stdout)))
   if rows and "estimated_cost_usd" not in rows[0]:raise RuntimeError("unverified Tinker usage schema")
   observed-=sum(float(x.get("estimated_cost_usd") or 0) for x in rows)
  self.db.execute("begin immediate")
  total=self.db.execute("select coalesce(sum(coalesce(actual,amount)),0) from reservations where provider=?",(p,)).fetchone()[0]
  if amount<0 or total+amount>s["campaign_cap"] or total+amount+s["old_hold"]+s["external_pending_guard"]>observed:
   self.db.rollback();raise RuntimeError(p+" budget refused")
  ident=str(uuid.uuid4());self.db.execute("insert into reservations values(?,?,?,?,?)",(ident,p,amount,None,label));self.db.commit();return ident
 def settle(self,ident,cost):
  old=self.db.execute("select amount from reservations where id=?",(ident,)).fetchone()[0]
  if cost is None or not 0<=cost<=old:raise RuntimeError("unknown or excessive cost; retain reserve and stop")
  self.db.execute("update reservations set actual=? where id=?",(cost,ident));self.db.commit()
 def summary(self):
  return {p:{"reserved_or_actual":self.db.execute("select coalesce(sum(coalesce(actual,amount)),0) from reservations where provider=?",(p,)).fetchone()[0],"campaign_cap":s["campaign_cap"],"old_hold":s["old_hold"]} for p,s in self.snapshot["providers"].items()}
