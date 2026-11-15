"""Exact all-shift arithmetic and numerical gradient tests."""
import pathlib,random,json,subprocess,tempfile
from fractions import Fraction
import numpy as np
import pytest
from .c1b_exact import score
from .c1b_ntt import check
from .c1b_search import soft,quantize
def literal(c):
 n,Q,k=c["n"],c["Q"],c["heights_int"];mx=max(sum(k[i]*(Q-k[i+m]) for i in range(max(0,-m),min(n,n-m))) for m in range(1-n,n))
 return Fraction(2*mx,n*Q*Q)
def test_exact_algorithms_and_brute_force():
 rng=random.Random(613)
 for n in [4,8,16]:
  a=np.array([rng.random() for _ in range(n)]);a=(a+1-a[::-1])/2;c=quantize(a)
  assert Fraction(score(c)["score"])==Fraction(check(c)["score"])==literal(c)
def test_mass_and_invalid_certificate_rejected():
 c={"n":4,"Q":10,"heights_int":[0,5,5,10]}
 assert Fraction(score(c)["score"])==literal(c)
 for bad in [c|{"heights_int":[0,5,6,10]},c|{"heights_int":[-1,5,6,10]}]:
  with pytest.raises(ValueError):score(bad)
  with pytest.raises(ValueError):check(bad)
def test_soft_gradient_against_finite_difference():
 rng=np.random.default_rng(81);a=rng.uniform(.1,.9,size=12);beta=21.;f,g=soft(a,beta,dual=.13,penalty=.6)
 for i in range(len(a)):
  d=np.zeros_like(a);d[i]=1e-6;num=(soft(a+d,beta,.13,.6)[0]-soft(a-d,beta,.13,.6)[0])/(2e-6)
  assert abs(num-g[i])<2e-7
