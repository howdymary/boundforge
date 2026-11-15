from fractions import Fraction as Q
import pytest
from .jets import entropy_poly,compile,json_result,check_polynomials
from .finite import certify
def test_binary_birth():
 a,b=entropy_poly([0,1],4);assert a[1]==1 and b[1].zero()
 a,b=entropy_poly([1,-1],4);assert not any(a)and b[1].c==1 and b[2].c==Q(-1,2)
 c=compile([[1,-1],[0,1]],[[0,1]],[[1]],4);assert c["margins"][0]["leading"]["sign"]==1
 assert certify([[1,-1],[0,1]],[[0,1]],[[1]],Q(1,2**80),512)["strict_all_margins"]
def test_regular_quadratic():
 c=compile([[Q(1,2),1],[Q(1,2),-1]],[[0,1]],[[-1]],4);lead=c["margins"][0]["leading"];assert lead["order"]==2 and lead["sign"]==1
def test_natural_quartic_mutual_information():
 polys=[[Q(1,4),0],[Q(1,4),1],[Q(1,4),-1],[Q(1,4),0]]
 maps=[[0,0,1,1],[0,1,0,1],[0,1,2,3]];margins=[[1,1,-1]]
 c=compile(polys,maps,margins,4);lead=c["margins"][0]["leading"];assert lead["order"]==4 and lead["sign"]==1
 assert certify(polys,maps,margins,Q(1,2**30),256)["strict_all_margins"]
def test_global_reparameterization_is_not_new_order_information():
 c=compile([[1,0,-1],[0,0,1]],[[0,1]],[[1]],4);assert c["margins"][0]["A"][2]==2
def test_invalid_mass_programs_rejected():
 with pytest.raises(AssertionError):compile([[1,1],[0,-1]],[[0,1]],[[1]],4)
 with pytest.raises(AssertionError):compile([[1,0],[0,1]],[[0,1]],[[1]],4)
def test_zero_jet_does_not_assert_identical_zero():
 c=compile([[1,0,0,0,0,-1],[0,0,0,0,0,1]],[[0,1]],[[1]],4);assert c["margins"][0]["leading"]["status"].startswith("zero through")
