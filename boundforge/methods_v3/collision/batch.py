"""Shared exact signatures for an entire family of basis deletions."""
import hashlib,itertools,json,math,time
from .linear import partitions,entropy
class Tables:
 def __init__(self,space,measurement_groups):
  self.ids=tuple(space.ids);self.groups=[];self.field=space.p;self.eliminations=0
  for forms in measurement_groups:
   residuals=[];coordinates=[]
   for form in forms:
    residual,c=space.reduce(form,True);residuals.append(residual);coordinates.append(c);self.eliminations+=1
   self.groups.append((partitions(residuals),coordinates))
 def partition(self,index,deleted):
  assert set(deleted)<=set(self.ids)
  labels,coords=self.groups[index]
  return partitions([(label,)+tuple(c.get(d,0)for d in deleted)for label,c in zip(labels,coords)])
 def all_partitions(self,deleted):return [self.partition(i,deleted)for i in range(len(self.groups))]
def forms_for(problem):
 return [[problem.row(a,b,i)for i in range(problem.m)]for a,b in problem.controls+[problem.target]]
def groups_for(problem,space):
 return [partitions([space.reduce(r)[0]for r in forms])for forms in forms_for(problem)]
def score(groups,m):
 hs=[entropy(g)for g in groups[:-1]]
 return {"key":tuple(sorted(hs,reverse=True)),"ratio":math.log(m)/max(hs)}
def best_repair(problem,space,row,trial,shared=True,limit=2):
 start=time.process_time();setup=time.process_time();table=Tables(trial,forms_for(problem))if shared else None;setup=time.process_time()-setup
 best=None;bestscore=None;checked=valid=0;records=[];choices=sorted(space.ids)
 for size in range(limit+1):
  for deleted in itertools.combinations(choices,size):
   checked+=1
   if shared:groups=table.all_partitions(deleted)
   else:
    candidate=problem.rebuild([i for i in trial.ids if i not in deleted]);groups=groups_for(problem,candidate)
   good=len(set(groups[-1]))==problem.m
   if not good:records.append([list(deleted),False]);continue
   valid+=1;s=score(groups,problem.m);records.append([list(deleted),True,s["ratio"]])
   if bestscore is None or s["key"]<bestscore["key"]:best=deleted;bestscore=s
  # No deletion is optimal if already feasible: removing constraints can only refine partitions.
  if size==0 and best is not None:break
 result=problem.rebuild([i for i in trial.ids if i not in best])if best is not None else space
 return result,{"diagnosis":"objective_aware_exact_repair"if best is not None else"no_repair_within_two_basis_deletions","scope":"Complete subsets of the stated trial basis of size at most "+str(limit)+"; not a global optimum","basis_before":list(space.ids),"proposed_row":row,"removed":None if best is None else list(best),"repair_subsets_checked":checked,"feasible_repairs":valid,"counterfactual_records":records,"table_setup_cpu":setup,"counterfactual_total_cpu":time.process_time()-start,"shared_table":shared,"linear_eliminations_in_table":table.eliminations if table else 0}
