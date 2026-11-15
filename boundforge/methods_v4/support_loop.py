"""Prospective analytic support-extension loop; no claim of methodological novelty."""
import argparse,copy,hashlib,itertools,json,math,os,pathlib,time
from fractions import Fraction as Q
from .jets import compile,proposed_bits,json_result
from .adaptive_log import certificate_bounds
FORMS=[(1,-1),(1,0),(0,1),(1,1),(1,2)]
def holes(law):
 pts=[tuple(p)for p in law["points"]];shadows=[{a*x+b*y for x,y in pts}for a,b in FORMS];seen=set();out=[]
 for i,j in itertools.combinations(range(1,5),2):
  a,b=FORMS[i];d,e=FORMS[j];det=a*e-b*d
  for u,v in itertools.product(shadows[i],shadows[j]):
   x,y=Q(e*u-b*v,det),Q(a*v-d*u,det)
   if (x,y)in seen or x-y in shadows[0]:continue
   seen.add((x,y))
   if all(aa*x+bb*y in shadows[k]for k,(aa,bb)in enumerate(FORMS[1:],1)):out.append((x,y))
 return sorted(out)
def proposal(law,point):
 weights=[Q(*w)for w in law["weights"]];points=[tuple(p)for p in law["points"]]+[point]
 polys=[[p,-p]for p in weights]+[[Q(0),Q(1)]]
 maps=[[str(a*x+b*y)for x,y in points]for a,b in FORMS];R=Q(1674894211307116228764565173,10**27)
 margins=[[Q(1)]+[-R if j==k else Q(0)for j in range(4)]for k in range(4)]
 compiled=compile(polys,maps,margins,1);assert all(m["leading"]["sign"]==1 for m in compiled["margins"])
 bits=proposed_bits(compiled)
 # Avoid relying on an unbounded Taylor neighborhood: make the trial mass small relative to all old affected images.
 for mapping in maps[1:]:
  label=mapping[-1];mass=sum(p for p,k in zip(weights,mapping[:-1])if k==label);assert mass>0;bits=max(bits,mass.denominator.bit_length()-mass.numerator.bit_length()+8)
 return bits,compiled
def candidate(base,lawid,point,b):
 c=copy.deepcopy(base);law=c["laws"][lawid];eps=Q(1,2**b);weights=[(1-eps)*Q(*w)for w in law["weights"]]+[eps];points=[tuple(p)for p in law["points"]]+[point];den=math.lcm(*(Q(z).denominator for p in points for z in p));law["points"]=[[int(Q(x)*den),int(Q(y)*den)]for x,y in points];law["weights"]=[[p.numerator,p.denominator]for p in weights];c["base"]=1+2*max(abs(a*x+b*y)for law in c["laws"]for x,y in law["points"]for a,b in FORMS);c["claimed_lower_bound"]=[0,1];return c
def ball_bounds(c,bits):
 from boundforge.verify import measure
 a,b,_=measure(c,bits=bits);return a,b
def main():
 from flint import arb,fmpq
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True);raw=pathlib.Path("boundforge/results/best.json").read_bytes();baseline=json.loads(raw);start=time.process_time();options=[];trace=[]
 for lawid,law in enumerate(baseline["laws"]):
  for point in holes(law):
   b,compiled=proposal(law,point);options.append((b,lawid,point,json_result(compiled)))
 assert options,"No zero-new-control-image support extension found"
 options.sort(key=lambda x:(x[0],x[1],x[2]));retained=None
 for number,(b,lawid,point,jet)in enumerate(options[:4]):
  for attempt in range(4):
   trialbits=b+32*attempt;precision=max(1024,4*trialbits+512)
   if precision>8192:continue
   c=candidate(baseline,lawid,point,trialbits);alo,ahi=ball_bounds(c,precision);blo,bhi=ball_bounds(baseline,precision);ql,qh=certificate_bounds(c,precision);bl,bh=certificate_bounds(baseline,precision)
   strict_arb=bool(alo>bhi);strict_q=ql>bh;assert strict_arb==strict_q
   entry={"turn":len(trace),"operator":"new support atom with no new control image","law":lawid,"point":list(map(str,point)),"epsilon_bits":trialbits,"precision_bits":precision,"formal_prediction":jet,"strict_arb":strict_arb,"strict_independent_rational":strict_q,"candidate_interval":[str(ql),str(qh)],"baseline_interval":[str(bl),str(bh)],"improvement_interval":[str(ql-bh),str(qh-bl)],"cpu":time.process_time()-start,"next_decision":"retain and stop"if strict_q else"shrink epsilon and recheck"};trace.append(entry);(out/"decisions.json").write_text(json.dumps(trace,indent=2))
   if strict_q:
    S=1<<(precision//2);claim=Q(ql.numerator*S//ql.denominator,S);c["claimed_lower_bound"]=[claim.numerator,claim.denominator];c["proof_bits"]=precision
    assert bool(alo>=arb(fmpq(claim.numerator,claim.denominator)))
    retained=c;(out/"candidate.json").write_text(json.dumps(c,indent=2));break
  if retained is not None:break
 report={"run_id":os.environ.get("GITHUB_RUN_ID"),"source_sha":os.environ.get("GITHUB_SHA"),"baseline_sha256":hashlib.sha256(raw).hexdigest(),"zero_shadow_candidates":len(options),"attempts":len(trace),"strict_improvement_over_archived":retained is not None,"cpu":time.process_time()-start,"new_method_claim":False,"world_record_claim":False,"frontier_audit_required":True,"chronology":"The prior diagnostic exposed existence of holes before this standalone run. The run enumerates/selects its own atom, scale and finite certificate. This is prospective development, not an untouched generalization test."}
 (out/"report.json").write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
if __name__=="__main__":main()
