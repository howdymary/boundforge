"""Hosted research memory, one actual agent. No multi-agent-memory benefit claim."""
import datetime as dt,hashlib,json,os,pathlib,time,urllib.request
from .ledger import reserve,settle
def http(path,payload=None):
 req=urllib.request.Request("https://api.past.dev/api/v1/"+path,data=None if payload is None else json.dumps(payload).encode(),headers={"Authorization":"Bearer "+os.environ["PAST_API_KEY"],"Content-Type":"application/json"})
 with urllib.request.urlopen(req,timeout=30)as r:return json.load(r)
def main():
 import argparse
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
 source="boundforge-methods-v3-validated-failures-"+os.environ["GITHUB_RUN_ID"]
 content="BoundForge methods-v3 measured findings. Scalar same-state probing: 324 verified development episodes, no robust advantage over fixed/UCB/shuffled controls; stop scaling this direction. Paired-order pilot: 180 development and140 validation episodes. Signed-contrast credit equals paired absolute reward difference algebraically, so it is not a novel rule. At validation, paired order underperforms stronger controls on graphs and cap sets; useful order predictions did not establish search benefit. Do not re-run or promote these as new methods. Next hypothesis: exact obstruction-guided changes of a projection-collision basis. Circuit/linear algebra components are standard; novelty and usefulness remain unestablished. Source reports: GitHub runs43747190963 and43747638494."
 token=reserve("past",10,"small measured-failure data point; unknown cost held")
 sent=http("ingest",{"id":source,"idempotencyKey":source,"identity":"boundforge-methods-v3-researcher","audience":"project","label":"BoundForge measured failed methods and next hypothesis","timestamp":dt.datetime.now(dt.timezone.utc).isoformat(),"content":content,"metadata":{"project":"boundforge","campaign":"methods-v3","record_type":"measured scoped negative finding"}})
 record={"source_id":source,"ingest":sent,"reserved_credits":10,"cost":"unknown; reservation retained","multi_agent_claim":False}
 (out/"memory.json").write_text(json.dumps(record,indent=2))
 ingestion=sent.get("ingestionId")
 for _ in range(20):
  if sent.get("status")=="completed":break
  if not ingestion:break
  time.sleep(2);sent=http("ingest/"+ingestion)
 record["completion"]=sent
 if sent.get("status")=="completed":
  reserve("past",5,"one scoped recall; unknown cost held")
  answer=http("recall",{"identity":"boundforge-methods-v3-researcher","query":"BoundForge methods-v3 which measured methods should not be repeated? exact source "+source,"level":"medium"})
  matches=[x for x in answer.get("results",[])if any(s.get("sourceId")==source for s in x.get("sources",[]))]
  record["recall"]={"response_sha256":hashlib.sha256(json.dumps(answer,sort_keys=True).encode()).hexdigest(),"required_source_found":bool(matches),"matching_documents":matches,"decision":"Continue collision-representation pilot; do not scale scalar/paired-order mechanisms"if matches else"Hosted recall did not confirm source; rely on immutable repository reports, no memory success claim","reserved_credits":5}
 (out/"memory.json").write_text(json.dumps(record,indent=2));print(json.dumps({k:v for k,v in record.items()if k not in ["recall"]}|{"required_source_found":record.get("recall",{}).get("required_source_found")}),flush=True)
if __name__=="__main__":main()
