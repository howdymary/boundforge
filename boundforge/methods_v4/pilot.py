"""Small discriminating tests; formal-order advantage is not assumed."""
import argparse,json,math,pathlib,random,time
from fractions import Fraction as Q
from .jets import compile,json_result,proposed_bits
from .finite import certify
MAPS=[[0,0,1,1],[0,1,0,1],[0,1,2,3]]
def cases():
 rows=[]
 for b in [1,10,40,80,160]:
  q=Q(1,2**b);base=[q/2,q/2,(1-q)/2,(1-q)/2];delta=[q-Q(1,2),-q-Q(1,2),Q(3,2)-q,q-Q(1,2)]
  rows.append({"name":"rare-independent-tangent-"+str(b),"class":"mutual_information_quartic","polys":[[p,d]for p,d in zip(base,delta)],"maps":MAPS,"margins":[[1,1,-1]],"expected_order":4})
 for degree in [1,2,3]:
  rows.append({"name":"birth-degree-"+str(degree),"class":"singular_birth","polys":[[1]+[0]*(degree-1)+[-1],[0]*degree+[1]],"maps":[[0,1]],"margins":[[1]],"expected_order":degree,"global_reparameterization":degree>1})
 # Multiobjective support additions: single atom births fail one margin, coupled births succeed.
 maps=[[0,1,2],[0,0,1],[0,1,0]]
 for label,a,b in [("a_only",Q(1),Q(0)),("b_only",Q(0),Q(1)),("coordinated",Q(1,2),Q(1,2))]:
  rows.append({"name":"privacy-"+label,"class":"coordinated_support","polys":[[1,-1],[0,a],[0,b]],"maps":maps,"margins":[[1,Q(-3,2),0],[1,0,Q(-3,2)]],"expected_order":1})
 return rows
def encode(x):
 if isinstance(x,Q):return str(x)
 if isinstance(x,dict):return {k:encode(v)for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [encode(v)for v in x]
 return x
def evaluate(case):
 begin=time.process_time();compiled=compile(case["polys"],case["maps"],case["margins"],4);compilecpu=time.process_time()-begin;prediction=json_result(compiled);signs=[r["leading"]["sign"]for r in compiled["margins"]];positive=all(x==1 for x in signs);b=proposed_bits(compiled);checks=[];grid=[];gridcpu=time.process_time()
 # Strong arbitrary-precision finite baseline uses the same safe domain, no fixed64-bit handicap.
 for precision in [128,256,512,1024,2048,4096]:
  e=Q(1,2**b);v=certify(case["polys"],case["maps"],case["margins"],e,precision);grid.append({"precision":precision,"signs":v["signs"],"positive":v["strict_all_margins"]})
  if v["strict_all_margins"]or all(x==-1 for x in v["signs"]):break
 gridcpu=time.process_time()-gridcpu
 start=time.process_time()
 if positive:
  for extra in [0,16,64]:
   ee=Q(1,2**(b+extra));bits=max(256,8+(b+extra)*max(r["leading"].get("order",1)for r in compiled["margins"])+256)
   if bits>8192:break
   check=certify(case["polys"],case["maps"],case["margins"],ee,bits);checks.append(check)
   if check["strict_all_margins"]:break
 return encode({"case":case,"jet":prediction,"compile_cpu":compilecpu,"predicted_all_positive":positive,"jet_verification_cpu":time.process_time()-start,"finite_checks":checks,"adaptive_finite_baseline":grid,"adaptive_finite_cpu":gridcpu,"known_limit":"Baseline is given the same candidate direction and safe radius. Candidate search and synthesis are not evaluated yet. Global epsilon reparameterizations are not independent transfer cases."})
def main():
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True);rows=[]
 for case in cases():
  r=evaluate(case);rows.append(r);(out/"cases.json").write_text(json.dumps(rows,indent=2))
 report={"stage":"development","cases":len(rows),"predicted_positive":sum(r["predicted_all_positive"]for r in rows),"independently_finite_verified_positive":sum(any(c["strict_all_margins"]for c in r["finite_checks"])for r in rows),"compile_cpu":sum(r["compile_cpu"]for r in rows),"jet_total_cpu":sum(r["compile_cpu"]+r["jet_verification_cpu"]for r in rows),"adaptive_finite_cpu":sum(r["adaptive_finite_cpu"]for r in rows),"cases_summary":[{"name":r["case"]["name"],"orders":[x["leading"].get("order")for x in r["jet"]["margins"]],"signs":[x["leading"]["sign"]for x in r["jet"]["margins"]],"positive":r["predicted_all_positive"]}for r in rows],"new_method_claim":False,"record_claim":False}
 (out/"report.json").write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
if __name__=="__main__":main()
