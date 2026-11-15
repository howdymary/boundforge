import itertools,random
from .tasks import Task,make,independent_check
from .search import greedy,hitting,step,quantum
def test_removal_certificate_matches_exhaustive():
 rng=random.Random(73)
 for _ in range(40):
  blocks=list({rng.randrange(1,1<<6)for j in range(6)});r=hitting(blocks,3)
  expected=[x for x in range(1<<6)if x.bit_count()<=3 and all(x&b for b in blocks)]
  assert (r is None)==(not expected)
  if r is not None:assert r.bit_count()==min(x.bit_count()for x in expected)
def test_all_operators_preserve_exact_validity():
 for task in [make("graph",24,731,.2),make("cap",3,0),make("deletion",6,0)]:
  rng=random.Random(71);s=greedy(task,0,rng,{"tested":0})
  for action in range(6):
   for _ in range(8):
    s=step(task,s,action,rng,{"tested":0});assert task.valid(s);assert independent_check(task,s)["valid"]
def test_bad_constructions_rejected():
 for task in [make("graph",12,4,.5),make("cap",2,0),make("deletion",5,0)]:
  e=task.edges[0];assert not task.valid(e)
  try:independent_check(task,e)
  except AssertionError:pass
  else:raise AssertionError("definition checker accepted forbidden edge")

def test_crossover_reuses_exact_prefixes_and_counts_cost():
 from .order import crossover,batch
 task=make("graph",18,731,.2);s=greedy(task,0,random.Random(4),{"tested":0});seed=19;a,b=0,3
 q=crossover(task,s,a,b,seed)
 sa=batch(task,s,a,seed*1009+a);sb=batch(task,s,b,seed*1009+b)
 ab=batch(task,sa["state"],b,seed*1009+b);ba=batch(task,sb["state"],a,seed*1009+a)
 assert q["ab"]["state"]==ab["state"]and q["ba"]["state"]==ba["state"]
 assert q["primitives"]==16
 assert task.valid(q["best"])
 assert q["contrast"]==max(sa["score"],ab["score"])-max(sb["score"],ba["score"])
