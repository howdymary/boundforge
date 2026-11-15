"""Archive owned experiment artifacts to GitHub without a local checkout."""
import argparse,base64,gzip,hashlib,io,json,re,subprocess,zipfile
REPO="howdymary/boundforge";PREFIX="boundforge/methods_v4/results/"
def api(path,method="GET",body=None):
 cmd=["gh","api","repos/"+REPO+"/"+path]
 if method!="GET":cmd+=["--method",method,"--input","-"]
 r=subprocess.run(cmd,input=None if body is None else json.dumps(body).encode(),capture_output=True,check=True);return json.loads(r.stdout)
def main():
 p=argparse.ArgumentParser();p.add_argument("--artifact",action="append",required=True,help="Numeric artifact ID:folder");a=p.parse_args();files={};manifest=[]
 for entry in a.artifact:
  ident,folder=entry.split(":");assert ident.isdigit()and re.fullmatch("[a-z0-9-]+",folder)
  meta=api("actions/artifacts/"+ident);assert meta["size_in_bytes"]<90000000
  assert meta["name"]in {"methods-v4-jets","methods-v4-support","methods-v4-oracle","methods-v4-critique","methods-v4-partitions","methods-v4-legacy"},"Only owned experiment artifacts; source excerpts require separate redaction"
  raw=subprocess.check_output(["gh","api",f"repos/{REPO}/actions/artifacts/{ident}/zip"]);z=zipfile.ZipFile(io.BytesIO(raw));assert sum(i.file_size for i in z.infolist())<1500000000
  members={}
  for info in z.infolist():
   data=z.read(info);members[info.filename]={"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}
   if info.filename.endswith(".json") and len(data)<1000000:files[PREFIX+folder+"/"+info.filename]=data
   elif info.filename in ["family-checks.json","memory-chains.json"]:files[PREFIX+folder+"/"+info.filename+".gz"]=gzip.compress(data,mtime=0)
  # Split only large archive transport; concatenation exactly reconstructs the original ZIP.
  parts=[]
  for at in range(0,len(raw),16*1024*1024):
   chunk=raw[at:at+16*1024*1024];name="complete-artifact.zip.part-"+str(len(parts)).zfill(3);files[PREFIX+folder+"/"+name]=chunk;parts.append({"path":name,"bytes":len(chunk),"sha256":hashlib.sha256(chunk).hexdigest()})
  record={"artifact_id":int(ident),"source_run":meta.get("workflow_run"),"zip_sha256":hashlib.sha256(raw).hexdigest(),"zip_bytes":len(raw),"reconstruction":"Concatenate parts in listed order; verify zip_sha256, then open as ZIP.","parts":parts,"members":members};manifest.append(record);files[PREFIX+folder+"/manifest.json"]=json.dumps(record,indent=2).encode()
 entries=[]
 for path,data in files.items():
  blob=api("git/blobs","POST",{"content":base64.b64encode(data).decode(),"encoding":"base64"});entries.append({"path":path,"mode":"100644","type":"blob","sha":blob["sha"]})
 for attempt in range(5):
  h=api("git/ref/heads/main")["object"]["sha"];base=api("git/commits/"+h)["tree"]["sha"];t=api("git/trees","POST",{"base_tree":base,"tree":entries});c=api("git/commits","POST",{"message":"Preserve complete owned research artifacts and independent certificate checks","tree":t["sha"],"parents":[h]})
  try:api("git/refs/heads/main","PATCH",{"sha":c["sha"],"force":False});print(json.dumps({"commit":c["sha"],"files":len(files),"bytes":sum(map(len,files.values())),"artifact_ids":[x["artifact_id"]for x in manifest]}));return
  except subprocess.CalledProcessError:
   if attempt==4:raise
if __name__=="__main__":main()
