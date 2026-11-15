"""Meaningful rejection controls for the two independent whole-circle checkers."""
import pytest
from boundforge.portfolio import c51_bernstein as poly,c51_taylor as trig
GOOD={"K":"3.56818544223368269553925743732750636848","alpha":"3.96154311181022808045648786109191322475","lower_bound":"0.58507881967451359","N":12}
def test_false_larger_bound_is_refused_by_both():
 bad=dict(GOOD,lower_bound="0.6")
 with pytest.raises(ValueError):poly.check(bad)
 with pytest.raises(ValueError):trig.verify(bad)
def test_invalid_entire_family_is_refused():
 bad=dict(GOOD,K="1")
 with pytest.raises(ValueError):poly.check(bad)
 with pytest.raises(ValueError):trig.verify(bad)
def test_bernstein_polynomial_matches_trig_identity():
 from fractions import Fraction as F
 from mpmath import iv
 K=F(GOOD["K"]);alpha=F(GOOD["alpha"]);q=poly.coefficients(K,alpha,12)
 for ts in ["0","0.2","0.64554155199259563657","1.1"]:
  theta=poly.scalar(F(ts));x=iv.cos(theta)**2
  p=sum((c*x**j for j,c in enumerate(q)),iv.mpf(0))
  re=im=iv.mpf(0)
  for n in range(13):
   T=n*(n+1)//2;c=2*poly.scalar(K)**(-T)*iv.cos((2*n+1)*theta)
   re+=c*iv.cos(poly.scalar(alpha)*T);im+=c*iv.sin(poly.scalar(alpha)*T)
  direct=re*re+im*im;u=poly.ends(p);v=poly.ends(direct)
  assert max(u[0],v[0])<=min(u[1],v[1])
