"""Adversarial mathematical checks; no paid APIs or search campaign."""
import itertools,random
from decimal import Decimal,Context
from fractions import Fraction
import pytest
from .verify_integer import lograt,reconstruct,ONE
from .verify_decimal import check
def toy():
 return {"mask":[0,1],"N":"4","x":["1","2"],"y":["1","2"]}
def test_log_enclosures_against_independent_decimal():
 ctx=Context(prec=130);rng=random.Random(502)
 for _ in range(20):
  n=rng.randrange(1,10**20);d=rng.randrange(1,10**20);lo,hi=lograt(Fraction(n,d))
  value=Fraction(ctx.subtract(ctx.ln(Decimal(n)),ctx.ln(Decimal(d))))
  assert Fraction(lo,ONE)<=value<=Fraction(hi,ONE)
def test_two_checkers_overlap_and_explicit_word_model():
 cert=toy();a=reconstruct(cert);b=check(cert)
 lo,hi=map(Fraction,a["rate_interval"]);dl,dh=map(Fraction,b["rate_interval_decimal"])
 assert max(lo,dl)<min(hi,dh)
 N=4;Q=3;L=int(a["L"]);words=[w for w in itertools.product([0,1],repeat=N) if sum(w)<=L]
 S={tuple(x+y for x,y in zip(u,v)) for u in words for v in words};D={tuple(x-y for x,y in zip(u,v)) for u in words for v in words}
 A={sum(x*Q**i for i,x in enumerate(w)) for w in words}
 assert len(S)==len({x+y for x in A for y in A}) and len(D)==len({x-y for x in A for y in A})
 assert len(D)>=12 and len(S)<=Fraction(7,4)**N*4
def test_bad_counts_and_raised_claim_are_rejected():
 for cert in [toy()|{"counts":{"1":"2"}},toy()|{"claim":"2"},toy()|{"mask":[0,1,1]}]:
  with pytest.raises(ValueError):reconstruct(cert)
  with pytest.raises(ValueError):check(cert)
def test_weighted_objective_gradient_away_from_ties():
 import numpy as np
 from .weighted_search import Problem
 p=Problem([0,1,3,4,9]);z=np.array([-.25,-.19,1.13,3.41,3.87,9.37]);value,g=p.fun(z)
 for k in range(len(z)):
  dz=np.zeros_like(z);dz[k]=1e-6
  numerical=(p.fun(z+dz)[0]-p.fun(z-dz)[0])/(2e-6)
  assert abs(numerical-g[k])<2e-5
