"""Run a separately authored checker without edits; isolated env and input JSON."""
import argparse,hashlib,json,os,pathlib,subprocess,sys,urllib.request
HERE=pathlib.Path(__file__).resolve().parent
SOURCE="https://raw.githubusercontent.com/arhancanli/quantavane-replays/ad5a4b17586a8c568ecc10d7fa78082830eefd95/c51/c51_check.py"
HASH="bc59bfbb62d308341666bcee3dfc05b2ec533da3f55f4e433de12b4c2f22e8e8"
DRIVER=r'''
import json,runpy,sys
from fractions import Fraction as F
d=json.load(sys.stdin);api=runpy.run_path(sys.argv[1],run_name="unmodified_published_checker")
lines=[]
e=api["enclose"](F(d["K"]),F(d["alpha"]),out=lambda *a,**k:lines.append(" ".join(map(str,a))),N=d.get("N",12),delta=F(1,10**24))
lo,hi,_=api["beta_text"](e)
print(json.dumps({"valid":bool(e["ok"] and lo>F(d["lower_bound"])),"beta_lower":str(lo),"beta_upper":str(hi),"cover":{"nodes":e["cover"]["nodes"],"leaves":e["cover"]["leaves"],"depth":e["cover"]["deepest"]},"trace":lines,"common_arithmetic":"Python standard-library decimal intervals, not mpmath"}))
'''
def verify(path,out):
 out.mkdir(parents=True,exist_ok=True);raw=urllib.request.urlopen(SOURCE,timeout=40).read()
 if hashlib.sha256(raw).hexdigest()!=HASH:raise ValueError("upstream source hash mismatch")
 source=out/"upstream_c51_check.py";source.write_bytes(raw);driver=out/"invoke_unmodified.py";driver.write_text(DRIVER)
 data=json.loads(path.read_text());p=subprocess.run([sys.executable,"-I",str(driver),str(source)],input=json.dumps(data),capture_output=True,text=True,env={"PATH":os.environ["PATH"]},timeout=150)
 if p.returncode:raise RuntimeError("external checker failed: "+p.stderr[-1500:])
 r=json.loads(p.stdout);r.update(source_url=SOURCE,source_sha256=HASH,certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),license="MIT; Arhan Canli, quantavane-replays; code unmodified")
 (out/"report.json").write_text(json.dumps(r,indent=2));return r
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("certificate",type=pathlib.Path);p.add_argument("--out",type=pathlib.Path,default=HERE/"upstream-output");a=p.parse_args();r=verify(a.certificate,a.out);print(json.dumps(r));raise SystemExit(0 if r["valid"]else 1)
