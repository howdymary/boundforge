"""Remote correctness checks, not tests mirroring a proposed performance claim."""
import itertools,json,os,pathlib,random,subprocess,tempfile
from tasks import ingredients,isvalid_c49
from exact import bounds,improves
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
