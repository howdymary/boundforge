import itertools
from .partitions import compile_partitions,equality_maps
def test_full_maps_cover_grid():
 old=[(0,0)];forms=[(1,0),(0,1),(1,1)]
 result=compile_partitions(old,forms,2)
 assert result["complete"]
 for x in itertools.product(range(-1,2),repeat=4):
  new=[x[:2],x[2:]];assert equality_maps(old,new,forms)in result["partitions"]
 for maps,item in result["partitions"].items():assert equality_maps(old,item["new_points"],forms)==maps
def test_same_novelty_can_have_different_entropy():
 old=[(0,0)];forms=[(1,0),(0,1),(1,1)]
 collided=equality_maps(old,[(1,0),(0,1)],forms)
 separate=equality_maps(old,[(1,0),(0,2)],forms)
 result=compile_partitions(old,forms,2)
 assert collided!=separate
 assert collided in result["partitions"] and separate in result["partitions"]
def test_incomplete_never_claims_coverage():
 result=compile_partitions([(0,0)],[(1,0),(0,1),(1,1)],2,max_flats=2)
 assert not result["complete"]
def test_redundant_old_constraints_are_not_forced_new():
 from .masks import signatures
 result=signatures([(0,0),(1,1)],[(1,0),(0,1),(1,1)])
 assert (0,0,0)in result["masks"]
 assert tuple(result["masks"][(0,0,0)]["point"])in [(0,0),(1,1)]
