"""Research-source and cross-role memory calls with explicit reservation receipts."""
import hashlib,json,os,time
from budget import http
def exa(ledger,query,log):
 rid=ledger.reserve("exa",.1,"research loop search")
 r=http("https://api.exa.ai/search",os.environ["EXA_API_KEY"],{"query":query,"type":"auto","numResults":4,"contents":{"text":{"maxCharacters":3500}}},"x-api-key")
 cost=r.get("costDollars",{}).get("total");ledger.settle(rid,cost)
 sources=[{k:x.get(k) for k in ["title","url","text","publishedDate"]} for x in r.get("results",[])]
 log("exa_sources",{"query":query,"request_id":r.get("requestId"),"cost_usd":cost,"sources":[{k:v for k,v in x.items() if k!="text"}|{"text_sha256":hashlib.sha256((x.get("text") or "").encode()).hexdigest()} for x in sources]})
 return sources
def write(ledger,role,content,log):
 sid="boundforge-c49-"+os.environ["GITHUB_RUN_ID"]+"-"+role
 item={"id":sid,"identity":"boundforge-c49-"+role,"audience":"project","label":"BoundForge C49 measured development findings","content":content,"metadata":{"project":"boundforge-c49"}}
 estimate=http("https://api.past.dev/api/v1/ingest/estimate",os.environ["PAST_API_KEY"],{"items":[item]})
 if not estimate.get("fits") or not isinstance(estimate.get("credits"),(int,float)):raise RuntimeError("unverified memory estimate")
 token=ledger.reserve("past",estimate["credits"],"memory ingest")
 r=http("https://api.past.dev/api/v1/ingest",os.environ["PAST_API_KEY"],{**item,"idempotencyKey":sid});ledger.settle(token,estimate["credits"])
 for _ in range(12):
  if r.get("status")=="completed":break
  time.sleep(1);r=http("https://api.past.dev/api/v1/ingest/"+r["ingestionId"],os.environ["PAST_API_KEY"])
 log("memory_write",{"role":role,"source_id":sid,"estimated_credits":estimate["credits"],"ready":r.get("status")=="completed"})
 return sid
def read(ledger,role,source,log):
 token=ledger.reserve("past",1,"memory recall")
 r=http("https://api.past.dev/api/v1/recall",os.environ["PAST_API_KEY"],{"identity":"boundforge-c49-"+role,"query":"BoundForge C49 measured development findings "+source,"limit":8,"maxTokens":1600})
 ledger.settle(token,1)
 ids={s.get("sourceId") for x in r.get("results",[]) for s in x.get("sources",[])}
 present=source in ids
 log("memory_read",{"role":role,"required_source":source,"cross_role_source_present":present,"returned_content_hash":hashlib.sha256(json.dumps(r).encode()).hexdigest()})
 return present
