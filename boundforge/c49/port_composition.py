"""Free exact port-count/periodic-chain diagnostic; PF/JSR methods are prior art."""
import hashlib,itertools,json,math,os,pathlib,subprocess,time
from fractions import Fraction
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"ports";OUT.mkdir(exist_ok=True)
from tasks import ingredients
from exact import bounds,rate_interval
def mul(A,B):return (A[0]*B[0]+A[1]*B[2],A[0]*B[1]+A[1]*B[3],A[2]*B[0]+A[3]*B[2],A[2]*B[1]+A[3]*B[3])
def score(P,L):return math.log((P[0]+P[3]+math.sqrt((P[0]-P[3])**2+4*P[1]*P[2]))/2)/L
def main():
 start=time.monotonic();p=next((HERE/"artifacts/replay/certificates").glob("best_*.json"));cert=json.loads(p.read_text())
 subprocess.run(["g++","-O3","-std=c++17",str(HERE/"port_counts.cpp"),"-o",str(OUT/"counts")],check=True)
 families=[("PR370",cert["n"],cert["masks"]),("F10",10,ingredients()[0]),("H11",11,ingredients()[1])]
 bank=[];dedup=set();all_ports=[]
 for name,n,fam in families:
  path=OUT/"masks";path.write_text("\n".join(map(str,fam)))
  rows=json.loads(subprocess.check_output([str(OUT/"counts"),str(path),str(n)]))
  all_ports.extend({"family":name,**r} for r in rows)
  for r in rows:
   a,b,c,d=r["counts"];T=(c,d,a,b);key=(T,n-2)
   if key in dedup:continue
   dedup.add(key);bank.append({"family":name,"n":n,**r,"T":T,"L":n-2})
 # Exact common-vector test for all port choices of the same PR370 family.
 a0,b0,c0,d0=(33980,64728,64728,88867)
 def nonpositive(A,B):
  if A==0:return B<=0
  if A>0:return B<0 and A*A*d0<=B*B*a0
  return B<=0 or A*A*d0>=B*B*a0
 inequalities=[]
 for r in all_ports:
  if r["family"]!="PR370":continue
  a,b,c,d=r["counts"];first=nonpositive(c-b0,d-d0);second=nonpositive(a-a0,b-b0)
  inequalities.append({"ports":r["ports"],"counts":r["counts"],"first":first,"second":second})
 common=all(r["first"] and r["second"] for r in inequalities)
 (OUT/"common_vector_certificate.json").write_text(json.dumps({"q_squared":[d0,a0],"rho":"64728+sqrt(3019700660)","all_ports_bounded":common,"inequalities":inequalities,"scope":"If true: arbitrary periodic products of port matrices for the exact same finite PR370 family cannot improve its rate. Standard common-positive-vector PF bound, not global optimality or a new general theorem."},indent=2))
 # All pairs; then bounded beam for periods3..8. No optimality claim beyond the finite all-pairs bank.
 beam=[((1,0,0,1),0,[])];top=[]
 for depth in range(1,9):
  candidates=[]
  for P,L,word in beam:
   for i,B in enumerate(bank):
    Q=mul(P,B["T"]);length=L+B["L"];candidates.append((Q,length,word+[i]))
  candidates.sort(key=lambda x:score(x[0],x[1]),reverse=True)
  top.extend(candidates[:20]);beam=candidates if depth==1 else candidates[:256]
 blo,bhi=bounds([33980,64728,64728,88867],26)
 exact=[]
 for P,L,word in sorted(top,key=lambda x:score(x[0],x[1]),reverse=True)[:40]:
  counts=[P[2],P[3],P[0],P[1]];lo,hi=bounds(counts,L)
  exact.append({"word":word,"matrix":P,"exponent":L,"rate":rate_interval(counts,L),"strict_improvement":lo>bhi})
 report={"source_sha":os.environ["GITHUB_SHA"],"run_id":os.environ["GITHUB_RUN_ID"],"bank":bank,"port_choices":len(all_ports),"unique_matrices":len(bank),"common_vector_all_ports":common,"same_family_inequalities_failed":sum(not(r["first"] and r["second"]) for r in inequalities),"exact_candidates":exact,"new_record":any(x["strict_improvement"] for x in exact),"elapsed_seconds":time.monotonic()-start,"scope":"All matrix pairs plus beam256 for periods3..8; numerical screen followed by exact rational comparisons. Existing valid families and gluing theorem, no new family."}
 (OUT/"report.json").write_text(json.dumps(report,indent=2));print("C49_PORTS_FINAL "+json.dumps({k:v for k,v in report.items() if k not in ["bank","exact_candidates"]}|{"best_exact":exact[0] if exact else None}),flush=True)
if __name__=="__main__":main()
