"""Check standalone boundaries and immutable verifier sources without paid calls."""
import hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
def main():
 m=json.loads((ROOT/"migration-manifest.json").read_text())
 for p,h in m["protected_sha256"].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 assert not (ROOT/"src/compute_forecast").exists()
 for p in (ROOT/"boundforge").rglob("*.py"):
  if "sources" in p.parts:continue
  s=p.read_text()
  assert "howdymary/compute-forecasting" not in s,p
  assert "compute-observatory" not in s,p
 for p in (ROOT/".github/workflows").glob("*.yml"):
  s=p.read_text()
  assert "compute-observatory" not in s,p
  assert "howdymary/compute-forecasting" not in s,p
  if p.name not in ("boundforge-check.yml","boundforge-v2-check.yml"):
   assert "\n  push:" not in s,p
 print(json.dumps({"standalone":True,"protected_verifiers":len(m["protected_sha256"]),"historical_files":len(m["files"])}))
if __name__=="__main__":main()
