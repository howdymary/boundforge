"""Independent C51a direct trig/Taylor cover, no polynomial or Bernstein code."""
import argparse,json,pathlib
from fractions import Fraction as R
from mpmath import iv
iv.dps=100
def rational(x):
 x=R(x);return iv.mpf(x.numerator)/x.denominator
def bound(x):
 out=[]
 for sign,man,exp,bc in x._mpi_:out.append(R((-1 if sign else 1)*man)*R(2)**exp)
 return out
def verify(d):
 K=R(d["K"]);alpha=R(d["alpha"]);N=d["N"];claim=R(d["lower_bound"])
 if K<=1 or not 0<claim<1 or not 1<=N<=20:raise ValueError("input range")
 k=rational(K);a=rational(alpha);cs=[];S0=S1=S2=iv.mpf(0)
 for n in range(N+1):
  T=n*(n+1)//2;freq=2*n+1;mag=2*k**(-T);arg=a*T;cs.append((freq,mag*iv.cos(arg),mag*iv.sin(arg)));S0+=mag;S1+=mag*freq;S2+=mag*freq*freq
 second=bound(2*(S1*S1+S0*S2)*(iv.pi/2)**2)[1]
 tail=2*K**(-((N+1)*(N+2)//2))/(1-K**(-(N+2)))
 available=1/claim-tail
 if available<=0:raise ValueError("tail exceeds budget")
 target=available*available
 stack=[(0,0)];nodes=leaves=deep=0;highest=R(0)
 while stack:
  index,depth=stack.pop();nodes+=1;mid=R(2*index+1,2**(depth+1));rad=R(1,2**(depth+1));t=iv.pi*rational(mid)/2
  re=im=dr=di=iv.mpf(0)
  for freq,cr,ci in cs:
   c=iv.cos(freq*t);s=-freq*iv.sin(freq*t)*iv.pi/2
   re+=cr*c;im+=ci*c;dr+=cr*s;di+=ci*s
  q=bound(re*re+im*im)[1];der=bound(2*(re*dr+im*di));D=max(abs(v)for v in der)
  up=q+D*rad+second*rad*rad/2
  if up<target:leaves+=1;deep=max(deep,depth);highest=max(highest,up)
  else:
   if depth>=80 or nodes>=100000:raise ValueError("full Taylor cover failed")
   stack.extend([(2*index,depth+1),(2*index+1,depth+1)])
 beta=1/(iv.sqrt(rational(highest))+rational(tail))
 assert bound(beta)[0]>claim
 return {"valid":True,"lower_bound":str(claim),"reciprocal_interval":[str(v)for v in bound(beta)],"N":N,"nodes":nodes,"leaves":leaves,"max_depth":deep,"entire_circle":True,"method":"Direct trigonometric midpoint/derivative evaluations with global Taylor remainder over full dyadic cover","tail":str(tail),"second_derivative_upper":str(second),"analytic_dependency":"He–Tang Theorem2.8, arXiv2602.12217"}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("certificate");a=p.parse_args();print(json.dumps(verify(json.loads(pathlib.Path(a.certificate).read_text()))))
