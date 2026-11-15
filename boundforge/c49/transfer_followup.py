"""Explicit post-hoc ceiling diagnostic: harder tasks, unchanged frozen controller."""
import hashlib,json,os,pathlib
HERE=pathlib.Path(__file__).resolve().parent
def main():
 import evaluate
 evaluate.OUT=HERE/"transfer_followup";evaluate.OUT.mkdir(exist_ok=True)
 p=HERE/"freeze/freeze.json";original=p.read_bytes();fr=json.loads(original)
 (evaluate.OUT/"parent_freeze.json").write_bytes(original)
 tasks=[{"id":"MIS128-a","kind":1,"n":128,"param":5505,"state":[]},{"id":"MIS128-b","kind":1,"n":128,"param":6606,"state":[]},{"id":"cap5","kind":2,"n":5,"param":0,"state":[]}]
 fr["heldout_tasks"]=[t["id"] for t in tasks];fr["parent_freeze_sha256"]=hashlib.sha256(original).hexdigest()
 fr["scope"]="Post-hoc ceiling diagnostic on3 harder auxiliary instances; frozen controller/operators unchanged, not replacement of the original evaluation."
 p.write_text(json.dumps(fr));(evaluate.OUT/"derived_freeze.json").write_text(json.dumps(fr,indent=2))
 evaluate.heldout_tasks=lambda:tasks
 os.environ["C49_LEDGER_SOURCE"]=str(HERE/"production/budget.sqlite")
 evaluate.main()
if __name__=="__main__":main()
