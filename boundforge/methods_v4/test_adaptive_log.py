from fractions import Fraction as Q
from .adaptive_log import logarithm,entropy
def test_exact_log_enclosures_against_independent_ball_backend():
 from flint import arb,fmpq,ctx
 ctx.prec=2048
 for q in [Q(1),Q(2),Q(1,2),Q(1,3),Q(103,17),Q(1,2**1200),Q(10**150+1,10**150)]:
  a,b=logarithm(q,1024);v=arb(fmpq(q.numerator,q.denominator)).log()
  assert bool(arb(fmpq(a.numerator,a.denominator))<=v)and bool(v<=arb(fmpq(b.numerator,b.denominator)))
  assert b-a<Q(1,2**1000)
def test_binary_entropy_enclosure():
 lo,hi=entropy([Q(1,2),Q(1,2)],512);a,b=logarithm(Q(2),512);assert max(lo,a)<=min(hi,b)
def test_extremely_small_birth_is_positive():
 p=Q(1,2**2000);a,b=entropy([1-p,p],4096);assert a>0 and b-a<Q(1,2**4000)
