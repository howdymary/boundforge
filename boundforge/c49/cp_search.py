"""Bounded CP-SAT separation for a new small base family; classical prior art."""
import itertools,json,math,resource,time
from fractions import Fraction
def run(spec):
 from ortools.sat.python import cp_model
 start=time.monotonic();cpu0=time.process_time();n=spec["n"];r=Fraction(spec["ratio_num"],spec["ratio_den"]);L=Fraction(spec["lambda_num"],spec["lambda_den"])
 model=cp_model.CpModel();universe=list(range(1,(1<<n)-1));v={x:model.new_bool_var(str(x)) for x in universe}
 # Fixing ports0,1 is WLOG under coordinate permutation. Empty/full cannot occur in a positive-port Sperner family.
 for b in universe:
  a=(b-1)&b
  while a:
   model.add(v[a]+v[b]<=1);a=(a-1)&b
 counts=[sum(v[x] for x in universe if x&3==c) for c in range(4)]
 for c in counts:model.add(c>=1)
 # For u=(r,1)>0, T*u >=L*u certifies rho(T)>=L. This is a search restriction on eigenvector ratio.
 model.add(L.denominator*(counts[2]*r.numerator+counts[3]*r.denominator)>=L.numerator*r.numerator)
 model.add(L.denominator*(counts[0]*r.numerator+counts[1]*r.denominator)>=L.numerator*r.denominator)
 model.maximize(sum(v.values()))
 from tasks import ingredients
 seedfam=ingredients()[n-10] if n in (10,11) else []
 for x in universe:model.add_hint(v[x],int(x in seedfam))
 cuts=set();trace=[];best=None;unknown=0
 for iteration in range(80):
  left=spec["seconds"]-(time.monotonic()-start)
  if left<1:break
  solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=min(8,left);solver.parameters.num_search_workers=2;solver.parameters.random_seed=spec["seed"]+iteration
  status=solver.solve(model);name=solver.status_name(status)
  row={"iteration":iteration,"solver_status":name,"wall_seconds":time.monotonic()-start,"cpu_seconds":time.process_time()-cpu0,"cuts":len(cuts)}
  if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
   chosen=[x for x in universe if solver.value(v[x])];violations=[]
   for a,b,c in itertools.combinations(chosen,3):
    if a&b==a&c==b&c:
     violations.append((a,b,c))
     if len(violations)>=10000:break
   row.update(members=len(chosen),sampled_violations=len(violations),objective_bound=solver.best_objective_bound)
   if not violations:
    best={"n":n,"ports":[0,1],"masks":chosen};trace.append(row);break
   for t in violations:
    if t not in cuts:model.add(sum(v[x] for x in t)<=2);cuts.add(t)
   unknown=0
  elif status==cp_model.INFEASIBLE:
   row["scope"]="solver-reported infeasible for this rational eigenvector-ratio restriction; no independent UNSAT certificate";trace.append(row);break
  elif status==cp_model.MODEL_INVALID:
   row["validation_error"]=model.validate();trace.append(row);break
  else:
   unknown+=1
   if unknown>=6:row["stop"]="six bounded solves without a feasible candidate";trace.append(row);break
  trace.append(row)
 return {"spec":spec,"trace":trace,"candidate":best,"elapsed_seconds":time.monotonic()-start,"cpu_seconds":time.process_time()-cpu0,"rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,"constraints_added":len(cuts),"scope":"Standard CP-SAT constraint separation. UNKNOWN is not infeasibility; absence of a candidate is not a mathematical bound."}
