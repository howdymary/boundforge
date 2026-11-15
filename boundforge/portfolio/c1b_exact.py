"""Own exact C1b checker using carry-free byte-packed integer multiplication."""
import argparse,hashlib,json,pathlib
from fractions import Fraction
def score(cert):
 n,Q,k=cert["n"],cert["Q"],cert["heights_int"]
 if type(n)is not int or n<2 or n%2 or len(k)!=n or type(Q)is not int or Q<=0:raise ValueError("dimensions")
 if any(type(x)is not int or not 0<=x<=Q for x in k) or 2*sum(k)!=n*Q:raise ValueError("height/mass")
 width=((n*Q*Q).bit_length()+7)//8;A=int.from_bytes(b"".join(x.to_bytes(width,"little") for x in k),"little");B=int.from_bytes(b"".join(x.to_bytes(width,"little") for x in reversed(k)),"little")
 raw=(A*B).to_bytes((2*n-1)*width,"little");prefix=[0]
 for x in k:prefix.append(prefix[-1]+x)
 best=(-1,0)
 for m in range(1-n,n):
  offset=(n-1-m)*width;cross=int.from_bytes(raw[offset:offset+width],"little")
  lo=max(0,-m);hi=min(n,n-m);value=Q*(prefix[hi]-prefix[lo])-cross
  if value>best[0]:best=(value,m)
 val=Fraction(2*best[0],n*Q*Q)
 if "score_num"in cert and val!=Fraction(cert["score_num"],cert["score_den"]):raise ValueError("incorrect stated value")
 return {"valid":True,"n":n,"Q":str(Q),"score":str(val),"argmax_shift":best[1],"all_shifts_checked":2*n-1,"algorithm":"carry-free packed integer convolution; exact integer prefix sums","mass_exact":True}
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("certificate");a=ap.parse_args();p=pathlib.Path(a.certificate);r=score(json.loads(p.read_text()));r["sha256"]=hashlib.sha256(p.read_bytes()).hexdigest();print(json.dumps(r))
