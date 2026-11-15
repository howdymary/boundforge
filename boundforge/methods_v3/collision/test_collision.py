import itertools,random
from fractions import Fraction
import sympy
from .linear import Problem,Space,prime_for,repairs
from .certify import recover,verify,verify_intervals
from .search import propose
def test_modular_rank_matches_rational_and_embedding():
 for m in [4,6,8]:
  task=Problem(m,[(1,0),(0,1),(1,1),(1,2)]);rng=random.Random(m);space=Space(task.d,task.p);ids=list(range(len(task.public)));rng.shuffle(ids);raw=[]
  for ident in ids[:30]:
   row=task.public[ident][3];added=space.add(row,ident);rank=sympy.Matrix(raw+[list(row)]).rank()
   assert (added is not None)==(rank>len(raw))
   if added is not None:space=added;raw.append(list(row))
  witness=recover(task,task.initial);a=verify(witness);b=verify_intervals(witness);assert a["valid"]and b["valid"]
def test_circuit_hitting_condition_is_necessary_and_sufficient():
 task=Problem(5,[(1,0),(0,1),(1,1),(1,2)]);space=task.initial
 for ident in range(len(task.public)):
  trial=space.add(task.public[ident][3],ident)
  if trial is None:continue
  cores,proof=task.obstruction(trial,ident)
  for k in [0,1,2]:
   for removed in itertools.combinations(space.ids,k):
    prediction=all(set(removed)&c for c in cores)
    actual=task.valid(task.rebuild([i for i in space.ids if i not in removed]+[ident]))
    assert prediction==actual
def test_basis_pivot_changes_repair_scope_without_changing_flat():
 # Generic exact algebra example: basis e1,e2,e3 and new e4.
 # Protected vectors e4+ei require all 3 old rows deleted in old basis.
 # Reencode with e1-e2,e2-e3,e1+e2+e3; deleting the last suffices.
 p=prime_for(4,6)
 old=[(1,0,0,0),(0,1,0,0),(0,0,1,0)];alt=[(1,-1,0,0),(0,1,-1,0),(1,1,1,0)]
 a=Space(4,p);b=Space(4,p)
 for i,r in enumerate(old):a=a.add(r,i)
 for i,r in enumerate(alt):b=b.add(r,i+10)
 assert a.key()==b.key()
 protected=[(1,0,0,1),(0,1,0,1),(0,0,1,1)]
 for base,expected in [(a,3),(b,1)]:
  trial=base.add((0,0,0,1),99);cores=[]
  for r in protected:
   residual,c=trial.reduce(r,True);assert not any(residual)
   cores.append(frozenset(i for i,v in c.items()if i!=99 and v))
  hits,n=repairs(cores,base.ids,3);assert hits and len(hits[0])==expected
def test_all_flat_policies_keep_target_separation():
 for policy in ["random_flat","circuit","random_pivot","guided_pivot","shuffled_core"]:
  task=Problem(6,[(1,0),(0,1),(1,1),(1,2)]);state=task.initial;rng=random.Random(7)
  for _ in range(12):state,e=propose(task,state,policy,rng);assert task.valid(state)
  witness=recover(task,state);assert verify(witness)["valid"]

def test_conditional_rebuild_and_full_library_are_valid():
 from .search import episode
 task=Problem(6,[(1,0),(0,1),(1,1),(1,2)]);state,e=propose(task,task.initial,"conditional_rebuild",random.Random(91));assert task.valid(state)
 for policy in ["library_ucb","library_random"]:
  result=episode([6,[(1,0),(0,1),(1,1),(1,2)]],policy,93,.05)
  assert result["check"]["valid"]and result["second_check"]["valid"]
