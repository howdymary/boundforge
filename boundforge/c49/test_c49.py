"""Remote correctness checks, not tests mirroring a proposed performance claim."""
import itertools,json,os,pathlib,random,subprocess,tempfile
from .tasks import ingredients,isvalid_c49
from .exact import bounds,improves
HERE=pathlib.Path(__file__).resolve().parent
def compile_binary(name,out):
 subprocess.run(["g++","-O2","-std=c++17",str(HERE/name),"-o",str(out)],check=True)
def test_bdd_agrees_with_literal_definition():
 with tempfile.TemporaryDirectory() as td:
  binary=pathlib.Path(td)/"bdd";masks=pathlib.Path(td)/"masks";compile_binary("verify_bdd.cpp",binary)
  rng=random.Random(7788)
  for i in range(100):
   n=rng.randrange(4,8);s=rng.sample(range(1<<n),rng.randrange(1,13));masks.write_text("\n".join(map(str,s)))
   expected=isvalid_c49(s,n) and len({x&3 for x in s})==4
   r=subprocess.run([str(binary),str(masks),str(n),"0","1"],capture_output=True,text=True)
   assert json.loads(r.stdout)["valid"]==expected
  masks.write_text("1\n1\n")
  assert subprocess.run([str(binary),str(masks),"4","0","1"],capture_output=True).returncode!=0
def test_search_returns_literal_valid_families():
 F,H=ingredients();assert isvalid_c49(F,10) and isvalid_c49(H,11)
 with tempfile.TemporaryDirectory() as td:
  binary=pathlib.Path(td)/"search";compile_binary("search.cpp",binary)
  for a in range(6):
   r=subprocess.run([str(binary)],input=f"0 10 0 {len(F)} 101 {a} 15\n"+" ".join(map(str,F)),capture_output=True,text=True,check=True)
   x=json.loads(r.stdout)
   assert isvalid_c49(x["state"],10) and isvalid_c49(x["best_family"],10)
   assert x["best_score"]>=x["initial_score"]-1e-14
def test_exact_frontier_comparison():
 from fractions import Fraction
 lo,hi=bounds([33980,64728,64728,88867],26)
 assert lo<Fraction("1.567864384572806979362033445047061") and hi>Fraction("1.567864384572806979362033445047060")
 assert not improves([33980,64728,64728,88867],26)
 assert improves([33981,64728,64728,88867],26)

def test_box_checker_agrees_with_literal_and_rejects_raised_claim():
 from .verify_boxes import check
 import pytest
 rng=random.Random(991)
 for _ in range(100):
  n=rng.randrange(4,8);s=rng.sample(range(1<<n),rng.randrange(1,13))
  expected=isvalid_c49(s,n) and len({x&3 for x in s})==4
  try:valid=check({"n":n,"ports":[0,1],"masks":s})["valid"]
  except ValueError:valid=False
  assert valid==expected
 F,H=ingredients()
 assert check({"n":10,"ports":[0,1],"masks":F})["valid"]
 with pytest.raises(ValueError):check({"n":10,"ports":[0,1],"masks":F,"claimed_rate_lower":"1.9"})

def test_positive_ports_do_not_hide_a_sunflower():
 from .verify_boxes import check
 import pytest
 family=[3,5,6,9,10,12] # Sperner, all four port cells, but {3,5,9} has core1.
 with pytest.raises(ValueError,match="sunflower"):check({"n":4,"ports":[0,1],"masks":family})
 with tempfile.TemporaryDirectory() as td:
  binary=pathlib.Path(td)/"bdd";path=pathlib.Path(td)/"masks";compile_binary("verify_bdd.cpp",binary)
  path.write_text("\n".join(map(str,family)))
  r=json.loads(subprocess.run([str(binary),str(path),"4","0","1"],capture_output=True,text=True).stdout)
  assert r["ordered_containments"]==6 and r["ordered_equal_intersection_triples"]>6 and not r["valid"]

def test_gluing_small_blocks_and_transfer_counts():
 from .verify_boxes import check
 cycle=[3,6,12,9];kept=[0,2,3,5,6,7]
 glued=[]
 for a in cycle:
  for b in cycle:
   if ((a>>1)&1)==(b&1):continue
   union=a|(b<<4)
   glued.append(sum(((union>>old)&1)<<new for new,old in enumerate(kept)))
 assert isvalid_c49(glued,6) and len(glued)==len(set(glued))==8
 report=check({"n":6,"ports":[0,3],"masks":glued})
 assert report["counts"]==[2,2,2,2] and report["exponent"]==4
