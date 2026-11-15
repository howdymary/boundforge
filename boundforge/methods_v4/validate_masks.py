import argparse,hashlib,json,pathlib,random,time
from .masks import signatures
from .independent_masks import enumerate_smt
from .partition_pilot import encode
def main():
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True);tasks=[];rng=random.Random(902710)
 for d in [2,3]:
  for i in range(8):
   points=sorted({tuple(rng.randrange(-2,3)for _ in range(d))for _ in range(3)})
   forms=[tuple(rng.randrange(-2,3)for _ in range(d))for _ in range(4)]
   tasks.append({"name":"prospective-d"+str(d)+"-"+str(i),"points":points,"forms":forms})
 base=json.loads(pathlib.Path("boundforge/results/best.json").read_text())
 for i,law in enumerate(base["laws"]):tasks.append({"name":"archived-C3c-law"+str(i),"points":law["points"],"forms":[[1,-1],[1,0],[0,1],[1,1],[1,2]]})
 rows=[]
 for task in tasks:
  geom=signatures(task["points"],task["forms"]);smt=enumerate_smt(task["points"],task["forms"])
  match=set(geom["masks"])==set(smt["masks"])if smt["complete"]else None
  assert match is not False
  row={"task":task,"geometry_cpu":geom["cpu"],"geometry_flats":geom["flats"],"geometry_masks":len(geom["masks"]),"smt":smt,"complete_agreement":match};rows.append(row)
  (out/"validation.json").write_text(json.dumps(encode(rows),indent=2));print(json.dumps({"name":task["name"],"mask_count":len(geom["masks"]),"geometry_cpu":geom["cpu"],"smt_cpu":smt["cpu"],"complete_agreement":match}),flush=True)
 report={"tasks":len(rows),"all_complete_agree":all(r["complete_agreement"]is True for r in rows),"geometry_cpu":sum(r["geometry_cpu"]for r in rows),"smt_cpu":sum(r["smt"]["cpu"]for r in rows),"new_method_claim":False,"scope":"Prospective exact-mask validation on d2/d3 random rational projection fixtures plus two exposed archived C3c supports; not broad transfer or untouched confirmatory discovery.","code_hashes":{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in [pathlib.Path(__file__),pathlib.Path(__file__).with_name("masks.py"),pathlib.Path(__file__).with_name("independent_masks.py")]}}
 (out/"report.json").write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
if __name__=="__main__":main()
