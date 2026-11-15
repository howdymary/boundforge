"""Independent direct cell-intersection integration on tiny examples."""
from fractions import Fraction as F
import pytest
from .c1b_translate_exact import check
from .c1b_translate_sweep import check as sweep
def literal(cert):
 n,Q,h=cert["n"],cert["Q"],cert["heights_int"];t=F(*map(int,cert["translation_cells"]))
 # Work in grid-cell coordinates; construct f and g by actual interval intersections.
 fk=sorted({F(0),F(n)}|{t+i for i in range(n+1) if 0<=t+i<=n})
 f=[];g=[]
 for l,r in zip(fk,fk[1:]):
  mid=(l+r)/2;i=(mid-t).__floor__();v=F(h[i],Q) if 0<=i<n else F(0);f.append((l,r,v));g.append((l,r,1-v))
 knots={q-p for l,r,_ in f for p in [l,r] for a,b,_ in g for q in [a,b]}
 best=F(0)
 for x in knots:
  value=F(0)
  for a,b,v in f:
   for c,d,w in g:value+=v*w*max(F(0),min(b,d-x)-max(a,c-x))*F(2,n)
  best=max(best,value)
 return best
def test_translation_both_algorithms_against_cell_intersections():
 for t in [F(-1,3),F(0),F(2,5)]:
  c={"n":8,"Q":10,"heights_int":[0,0,10,10,10,10,0,0],"translation_cells":[str(t.numerator),str(t.denominator)]}
  assert F(check(c)["score"])==F(sweep(c)["score"])==literal(c)
def test_outside_window_rejected():
 c={"n":4,"Q":10,"heights_int":[0,10,10,0],"translation_cells":["2","1"]}
 with pytest.raises(ValueError):check(c)
 with pytest.raises(ValueError):sweep(c)
