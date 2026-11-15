import itertools
from fractions import Fraction as Q
from .masks import signatures,dot,cone
def actual(points,forms,x):
 return tuple(int(dot(a,x)not in {dot(a,p)for p in points})for a in forms)
def test_geometry_covers_grid():
 for forms,points in [
  ([(1,0),(0,1),(1,1),(2,2),(0,0)],[(0,0),(1,2)]),
  ([(1,0,0),(0,1,0),(0,0,1),(1,1,1)],[(0,0,0),(Q(1,2),1,2)]),
  ([(1,),(2,),(0,)],[(Q(1,3),),(2,)])]:
  out=signatures(points,forms)
  for mask,item in out["masks"].items():assert actual(points,forms,item["point"])==mask
  for x in itertools.product(range(-3,4),repeat=len(forms[0])):assert actual(points,forms,x) in out["masks"]
def test_coordinated_birth_required():
 forms=[(1,1),(1,0),(0,1)];out=signatures([(0,0)],forms,required_new=(0,))
 rows=[[1,Q(-3,2),0],[1,0,Q(-3,2)]]
 result=cone(out["masks"],rows)
 assert result["lower"]==Q(1,4)==result["upper"]
 assert all(min(dot(row,mask)for row in rows)<=0 for mask in out["masks"])
 assert sum(w>0 for w in result["weights"])==2
def test_negative_exact_dual():
 out=signatures([(0,0)],[(1,-1),(1,0),(0,1)],required_new=(0,))
 result=cone(out["masks"],[[1,-2,-2]])
 assert result["upper"]==-1 and result["status"]=="no-positive-leading-ascent"
def test_zero_is_not_global_impossibility():
 out=signatures([(0,0)],[(1,0),(0,1)],required_new=(0,))
 assert cone(out["masks"],[[1,-1],[-1,1]])["upper"]==0
