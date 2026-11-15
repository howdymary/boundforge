"""Independent exact-theory check and strongest simple symbolic baseline.
No imports from geometry oracle. QF linear real arithmetic is rationally complete here.
"""
import itertools,time
from fractions import Fraction as Q
def enumerate_smt(points,forms,task_seconds=30):
 import z3
 start=time.process_time();d=len(forms[0]);xs=[z3.Real("x"+str(i))for i in range(d)];s=z3.Solver();s.set(timeout=3000);new=[]
 def rational(x):return z3.RealVal(str(Q(x)))
 for j,a in enumerate(forms):
  expr=sum((rational(v)*x for v,x in zip(a,xs)),rational(0));shadow={sum(Q(v)*Q(x)for v,x in zip(a,p))for p in points};b=z3.Bool("new"+str(j));s.add(b==z3.And(*[expr!=rational(v)for v in shadow]));new.append(b)
 found={};checks=[];complete=True
 for mask in itertools.product([0,1],repeat=len(forms)):
  if time.process_time()-start>task_seconds:complete=False;break
  result=s.check(*[b if bit else z3.Not(b)for b,bit in zip(new,mask)])
  checks.append({"mask":mask,"status":str(result)})
  if result==z3.unknown:complete=False;continue
  if result==z3.sat:
   model=s.model();p=[]
   for x in xs:
    v=model.eval(x,model_completion=True);assert z3.is_rational_value(v);p.append(Q(v.numerator_as_long(),v.denominator_as_long()))
   actual=tuple(int(sum(Q(a)*x for a,x in zip(form,p)) not in {sum(Q(a)*Q(x)for a,x in zip(form,old))for old in points})for form in forms)
   assert actual==mask;found[mask]=p
 return {"masks":found,"checks":checks,"complete":complete,"cpu":time.process_time()-start,"solver_version":z3.get_version_string()}
