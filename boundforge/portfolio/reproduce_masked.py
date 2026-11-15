"""Reproduce the strongest finite C3e certificate with fresh own checkers."""
import base64,hashlib,json,os,pathlib,subprocess,sys,time
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"reproduction";OUT.mkdir(exist_ok=True)
PIN="763fd85126b69b72a8f94fdfceae7b6a36e5b1da";REPO="mizopl/ghr-c3a-odd-base-finite-bound"
def fetch(path):
 raw=subprocess.check_output(["gh","api",f"repos/{REPO}/contents/{path}?ref={PIN}"]);d=json.loads(raw);return base64.b64decode(d["content"])
def main():
 start=time.monotonic();sources={}
 for name in ["c3e_finite_certificate_80_161.json","c3e_finite_certificate_160_321.json","check_c3e.py"]:
  raw=fetch("c3e_finite_certificate/"+name);sources[name]={"url":f"https://github.com/{REPO}/blob/{PIN}/c3e_finite_certificate/{name}","sha256":hashlib.sha256(raw).hexdigest()};(OUT/name).write_bytes(raw)
 # Primary replay in an isolated process. It imports no credentials and performs no network.
 r=subprocess.run([sys.executable,"-I",str(OUT/"check_c3e.py"),str(OUT)],capture_output=True,text=True,check=True);(OUT/"primary-replay.txt").write_text(r.stdout)
 old=json.loads((OUT/"c3e_finite_certificate_160_321.json").read_text());mask=[i for i in range(161) if i not in [1,2,3,6,7,11]]
 cert={"schema":"boundforge-masked-v1","mask":mask,"N":str(old["N"]),"x":[str(old["x_num"]),str(old["x_den"])],"y":[str(old["y_num"]),str(old["y_den"])],"source":sources["c3e_finite_certificate_160_321.json"],"scope":"Prior construction, not a BoundForge result"}
 p=OUT/"baseline.json";p.write_text(json.dumps(cert,indent=2));checks={}
 for name in ["verify_integer.py","verify_decimal.py"]:
  checks[name]=json.loads(subprocess.check_output([sys.executable,"-I",str(HERE/name),str(p)]))
 assert checks["verify_integer.py"]["counts"]==checks["verify_decimal.py"]["counts"]
 from fractions import Fraction
 lo,hi=map(Fraction,checks["verify_integer.py"]["rate_interval"]);dl,dh=map(Fraction,checks["verify_decimal.py"]["rate_interval_decimal"])
 assert max(lo,dl)<min(hi,dh)
 report={"source_sha":os.environ["GITHUB_SHA"],"run_id":os.environ["GITHUB_RUN_ID"],"sources":sources,"primary_replay":r.stdout,"checks":checks,"elapsed_seconds":time.monotonic()-start,"frontier_limit_claim":"1.2725580515... from PR339, not reproduced by a finite checker and not ignored in record acceptance."}
 (OUT/"report.json").write_text(json.dumps(report,indent=2));print("MASK_REPRODUCED "+json.dumps({"valid":True,"integer_interval":[str(lo),str(hi)],"decimal_interval":[str(dl),str(dh)],"elapsed_seconds":report["elapsed_seconds"]}),flush=True)
if __name__=="__main__":main()
