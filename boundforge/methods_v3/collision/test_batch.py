import itertools,random
from .linear import Space,Problem,prime_for,partitions
from .batch import Tables,best_repair,forms_for,groups_for
from .search import propose,episode
def test_generic_grouped_measurements_equal_rebuilds():
 rng=random.Random(702)
 for dimension in [3,5,7]:
  raw=[tuple(rng.randint(-2,2)for _ in range(dimension))for _ in range(20)]
  forms=[[tuple(rng.randint(-3,3)for _ in range(dimension))for _ in range(9)]for _ in range(3)]
  p=prime_for(dimension,max(sum(x*x for x in r)for r in raw+sum(forms,[])));space=Space(dimension,p);kept={}
  for ident,r in enumerate(raw):
   new=space.add(r,ident)
   if new is not None:space=new;kept[ident]=r
   if len(space.ids)==dimension-1:break
  table=Tables(space,forms)
  for size in range(3):
   for deleted in itertools.combinations(space.ids,size):
    rebuilt=Space(dimension,p)
    for ident in space.ids:
     if ident not in deleted:rebuilt=rebuilt.add(kept[ident],ident)
    actual=[partitions([rebuilt.reduce(r)[0]for r in group])for group in forms]
    assert table.all_partitions(deleted)==actual
def test_all_counterfactuals_and_best_match_fresh_rebuilds():
 for m in [4,6,8]:
  problem=Problem(m,[(1,0),(0,1),(1,1),(1,2)]);state=problem.initial;rng=random.Random(m)
  for _ in range(4):state,_=propose(problem,state,"circuit",rng)
  independent=[(i,state.add(r,i))for i,(_,u,v,r)in enumerate(problem.public)if state.add(r,i)is not None]
  for row,trial in independent[:5]:
   a,ae=best_repair(problem,state,row,trial,True);b,be=best_repair(problem,state,row,trial,False)
   assert ae["counterfactual_records"]==be["counterfactual_records"]
   assert a.key()==b.key()
   assert problem.valid(a)
def test_new_policies_verify_integer_artifacts():
 for policy in ["batch_repair","naive_best_repair"]:
  result=episode([6,[(1,0),(0,1),(1,1),(1,2)]],policy,17,.08)
  assert result["check"]["valid"]and result["second_check"]["valid"]
