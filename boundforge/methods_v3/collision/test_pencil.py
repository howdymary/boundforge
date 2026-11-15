import collections,itertools,random
from fractions import Fraction as Q
from .pencil import event_scan,realize,objective,direction_for,episode,product
from .linear import Problem
from .certify import actual_groups
def test_all_event_products_equal_independent_coordinate_aggregation():
 rng=random.Random(511)
 for m in [4,6,8]:
  p=[(i-i//2,-(i//2))for i in range(m)];v=[(0,0)]+[(rng.randint(-3,3),rng.randint(-3,3))for _ in range(1,m)];controls=[(1,0),(0,1),(1,1),(1,2)]
  scan=event_scan(p,v,controls);assert scan["complete_slice"]
  for record in scan["records"]:
   if record["valid"]:
    actual=realize(p,v,record);assert objective(actual,controls)==tuple(record["key"]);assert len({x-y for x,y in actual})==m
   else:
    t=Q(*record["parameter"]);assert len({(x-y)+t*(a-b)for (x,y),(a,b)in zip(p,v)})<m
def test_nullity_two_projective_maximum_is_parameterization_invariant():
 problem=Problem(5,[(1,0),(0,1),(1,1),(1,2)]);p=problem.initial_points;rng=random.Random(2);found=False
 for release in itertools.combinations(problem.initial.ids,1):
  v,info=direction_for(problem,p,problem.initial,rng,release)
  if v is None or info["nullity"]!=2:continue
  a=event_scan(p,v,problem.controls);p2=[(2*x+3*vx,2*y+3*vy)for (x,y),(vx,vy)in zip(p,v)];v2=[(x+2*vx,y+2*vy)for (x,y),(vx,vy)in zip(p,v)]
  # The base point for the scanner must itself have an injective target.
  if len({x-y for x,y in p2})<problem.m:continue
  b=event_scan(p2,v2,problem.controls);assert a["best_key"]==b["best_key"];found=True;break
 assert found
def test_uniform_integer_objective_matches_entropy_order():
 from .linear import entropy
 examples=[[0,1,2,3],[0,0,1,2],[0,0,1,1],[0,0,0,1],[0,0,0,0]]
 for a,b in itertools.combinations(examples,2):assert (product(a)>product(b))==(entropy(a)<entropy(b))
def test_pencil_policies_generate_verified_points():
 for policy in ["coordinate_event","random_event","kernel_event","memory_event","circuit","batch_repair","coordinate"]:
  r=episode([6,[(1,0),(0,1),(1,1),(1,2)]],policy,22,.1);assert r["check"]["valid"]and r["second_check"]["valid"]

def test_independent_complete_family_checker():
 from .verify_family import check_family
 problem=Problem(5,[(1,0),(0,1),(1,1),(1,2)]);p=problem.initial_points;rng=random.Random(23)
 for row in problem.initial.ids:
  direction,info=direction_for(problem,p,problem.initial,rng,[row])
  if direction is not None and info["nullity"]==2:
   event={"point_before":[list(x)for x in p],"direction":[list(x)for x in direction],"scan":event_scan(p,direction,problem.controls),**info}
   assert check_family(problem.m,problem.controls,event)["valid"]
   return
 raise AssertionError("missing test family")
