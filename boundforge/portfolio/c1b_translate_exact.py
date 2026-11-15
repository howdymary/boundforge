"""Exact continuum overlap for a rationally translated step function.
Method1: carry-free packed height correlation, exact prefix interpolation,
and union of the correlation and translated-boundary knot meshes.
"""
import argparse,json,pathlib
from fractions import Fraction
def check(cert):
 n,Q,h=cert["n"],int(cert["Q"]),cert["heights_int"];T=Fraction(*map(int,cert.get("translation_cells",["0","1"])));P,R=T.numerator,T.denominator
 if type(n)is not int or n<2 or n%2 or len(h)!=n or Q<=0 or any(type(x)is not int or not 0<=x<=Q for x in h) or 2*sum(h)!=n*Q:raise ValueError("admissibility")
 support=[i for i,x in enumerate(h) if x]
 if not -support[0]<=T<=n-1-support[-1]:raise ValueError("translated support escapes window")
 width=((n*Q*Q).bit_length()+7)//8
 a=int.from_bytes(b"".join(x.to_bytes(width,"little") for x in h),"little");b=int.from_bytes(b"".join(x.to_bytes(width,"little") for x in reversed(h)),"little");raw=(a*b).to_bytes((2*n-1)*width,"little")
 corr=[int.from_bytes(raw[(n-1-m)*width:(n-m)*width],"little") for m in range(n)]+[0]
 prefix=[0]
 for x in h:prefix.append(prefix[-1]+x)
 def pre(z):
  if z<=0:return 0
  if z>=n*R:return prefix[-1]*R
  i,r=divmod(z,R);return prefix[i]*R+h[i]*r
 def cor(z):
  i,r=divmod(z,R)
  if i>=n:return 0
  return corr[i]*R+(corr[i+1]-corr[i])*r
 maxima=[]
 for sign in [1,-1]:
  peak=-1;arg=None
  for kind in [0,1]:
   for i in range(n+1):
    z=i*R if kind==0 else n*R-P-i*R if sign==1 else P+i*R
    if not 0<=z<=n*R:continue
    first=pre(n*R-z-P) if sign==1 else prefix[-1]*R-pre(z-P)
    value=Q*first-cor(z)
    if value>peak:peak=value;arg={"sign":sign,"knot_mesh":"autocorrelation" if kind==0 else "window boundary","index":i,"lag_cells":str(Fraction(z,R))}
  maxima.append({"scaled_max":str(peak),"arg":arg})
 maximum=max(int(x["scaled_max"]) for x in maxima);value=Fraction(2*maximum,n*Q*Q*R)
 return {"valid":True,"score":str(value),"n":n,"translation_cells":str(T),"all_real_shifts":True,"method":"packed-height convolution and exact prefix/knot union","positive_and_negative_maxima":maxima,"scaled_denominator":str(n*Q*Q*R),"scope":"Continuum upper bound for the rationally shifted function; no global optimality claim."}
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("certificate");a=ap.parse_args();print(json.dumps(check(json.loads(pathlib.Path(a.certificate).read_text()))))
