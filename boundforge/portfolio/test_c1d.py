"""Signed objective controls, including the Arena max-versus-absolute pitfall."""
import random
import numpy as np
from scipy.fft import next_fast_len
from fractions import Fraction
import pytest
from .c1d_exact import score
from .c1d_ntt import check
from .c1d_search import fg
def test_signed_convolution_against_brute_force():
 for v in [[2,-3,4],[3,-2,-4,7],[1,1,1,1]]:
  c={"v_int":v};coef=[sum(v[j]*v[k-j] for j in range(max(0,k-len(v)+1),min(k,len(v)-1)+1)) for k in range(2*len(v)-1)]
  expected=Fraction(2*len(v)*max(map(abs,coef)),sum(v)**2)
  assert Fraction(score(c)["score"])==Fraction(check(c)["score"])==expected
def test_signed_gradient_finite_difference():
 x=np.array([1.1,-.3,.8,1.7,-.2,1.3]);p=9.;L=next_fast_len(2*len(x)-1,real=True);f,g=fg(x,p,L)
 for i in range(len(x)):
  d=np.zeros_like(x);d[i]=1e-6;assert abs((fg(x+d,p,L)[0]-fg(x-d,p,L)[0])/(2e-6)-g[i])<1e-6
def test_zero_integral_rejected():
 for fn in [score,check]:
  with pytest.raises(ValueError):fn({"v_int":[1,-1]})
