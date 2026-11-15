import math,random
from .weighted_events import scan,realize,law_entropies,mix_opt
def test_weighted_event_updates_match_direct_aggregation():
 p=[(0,0),(1,0),(1,-1),(2,-1),(2,-2)];v=[(0,0),(1,0),(-1,2),(0,1),(2,-1)];w=[.1,.2,.3,.15,.25];records,meta=scan(p,v,w)
 assert meta["complete_event_location_scan"]
 for r in records:
  q=realize(p,v,r["parameter"]);hh=law_entropies(q,w);assert max(abs(a-b)for a,b in zip(hh,r["entropies"]))<1e-12
  assert len({x-y for x,y in q})==len(q)
def test_mixture_breakpoints_dominate_dense_grid():
 rng=random.Random(12)
 for _ in range(20):
  a=[rng.uniform(.5,2)for _ in range(4)];b=[rng.uniform(.5,2)for _ in range(4)];ta,tb=rng.uniform(1,2),rng.uniform(1,2);t,best=mix_opt(a,b,ta,tb)
  grid=max((x*ta+(1-x)*tb)/max(x*u+(1-x)*v for u,v in zip(a,b))for x in [i/1000 for i in range(1,1000)])
  assert best>=grid-1e-12
