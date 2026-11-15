"""Finish a prior ingestion and recall only our public project findings."""
import argparse,io,json,pathlib,subprocess,time,zipfile,hashlib
from .memory import http
from .ledger import reserve
def main():
 p=argparse.ArgumentParser();p.add_argument("--run",required=True);p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True);repo="howdymary/boundforge"
 arts=json.loads(subprocess.check_output(["gh","api",f"repos/{repo}/actions/runs/{a.run}/artifacts"]))["artifacts"];item=next(x for x in arts if x["name"]=="methods-v3-memory")
 archive=zipfile.ZipFile(io.BytesIO(subprocess.check_output(["gh","api",f"repos/{repo}/actions/artifacts/{item['id']}/zip"])));record=json.loads(archive.read("memory.json"));ing=record["ingest"].get("ingestionId")
 status=http("ingest/"+ing)
 for _ in range(60):
  if status.get("status")in ["completed","failed"]:break
  time.sleep(2);status=http("ingest/"+ing)
 record["completion"]=status
 if status.get("status")=="completed"and"recall"not in record:
  reserve("past",5,"one completed measured-failure recall, unknown cost held")
  answer=http("recall",{"identity":"boundforge-methods-v3-researcher","query":"Find the exact BoundForge methods-v3 measured-failure record source "+record["source_id"]+"; which methods should we avoid repeating and why?","level":"medium"})
  matching=[x for x in answer.get("results",[])if any(s.get("sourceId")==record["source_id"]for s in x.get("sources",[]))]
  record["recall"]={"required_source_found":bool(matching),"matching_documents":matching,"response_sha256":hashlib.sha256(json.dumps(answer,sort_keys=True).encode()).hexdigest(),"decision":"Keep scalar/paired-order directions stopped; continue collision-representation study"if matching else"Source not found; no memory success claim, rely on immutable repository reports"}
 (out/"memory.json").write_text(json.dumps(record,indent=2));print(json.dumps({"status":status.get("status"),"source_id":record["source_id"],"required_source_found":record.get("recall",{}).get("required_source_found")}),flush=True)
if __name__=="__main__":main()
