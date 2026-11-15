"""Fresh-process independent certification and exact incumbent comparison."""
import argparse,hashlib,json,pathlib,subprocess,sys,tempfile
from fractions import Fraction
HERE=pathlib.Path(__file__).resolve().parent
def certify(certificate,baseline):
 cert=json.loads(pathlib.Path(certificate).read_text());bar=json.loads(pathlib.Path(baseline).read_text())
 def box(path):return json.loads(subprocess.check_output([sys.executable,"-I",str(HERE/"verify_boxes.py"),str(path)]))
 x=box(certificate);b=box(baseline)
 with tempfile.TemporaryDirectory() as td:
  td=pathlib.Path(td);binary=td/"verify"
  subprocess.run(["g++","-O3","-std=c++17",str(HERE/"verify_bdd.cpp"),"-o",str(binary)],check=True)
  reports=[]
  for data in [cert,bar]:
   p=td/"masks";p.write_text("\n".join(map(str,data["masks"])))
   reports.append(json.loads(subprocess.check_output([str(binary),str(p),str(data["n"]),*map(str,data["ports"])])))
 assert x["counts"]==reports[0]["counts"] and b["counts"]==reports[1]["counts"]
 lo,hi=map(Fraction,x["rate_interval_rational"]);bl,bh=map(Fraction,b["rate_interval_rational"])
 return {"valid":True,"strict_improvement":lo>bh,"comparison":"equal certificate" if cert["masks"]==bar["masks"] and cert["ports"]==bar["ports"] else "strict improvement" if lo>bh else "not proved better","box":x,"bdd":reports[0],"baseline_box":b,"baseline_bdd":reports[1],"certificate_sha256":hashlib.sha256(pathlib.Path(certificate).read_bytes()).hexdigest(),"verifier_sha256":{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ["verify_boxes.py","verify_bdd.cpp"]}}
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("certificate");ap.add_argument("baseline");a=ap.parse_args();print(json.dumps(certify(a.certificate,a.baseline)))
