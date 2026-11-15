"""Exact absolute signed autoconvolution bound, split-sign Kronecker arithmetic."""
import argparse,json,pathlib
from fractions import Fraction
def score(cert):
 v=cert["v_int"]
 if not isinstance(v,list) or len(v)<2 or any(type(x)is not int for x in v) or not sum(v):raise ValueError("signed vector")
 n=len(v);height=max(map(abs,v));width=((n*height*height).bit_length()+7)//8
 pos=[max(x,0) for x in v];neg=[max(-x,0) for x in v]
 def pack(s):return int.from_bytes(b"".join(x.to_bytes(width,"little") for x in s),"little")
 P=pack(pos);Q=pack(neg);size=(2*n-1)*width
 pp=(P*P).to_bytes(size,"little");pq=(P*Q).to_bytes(size,"little");qq=(Q*Q).to_bytes(size,"little")
 high=-1;arg=0
 for k in range(2*n-1):
  j=k*width;a=int.from_bytes(pp[j:j+width],"little");b=int.from_bytes(pq[j:j+width],"little");c=int.from_bytes(qq[j:j+width],"little");val=abs(a-2*b+c)
  if val>high:high=val;arg=k
 result=Fraction(2*n*high,sum(v)**2)
 if "score_num"in cert and result!=Fraction(int(cert["score_num"]),int(cert["score_den"])):raise ValueError("stated score")
 return {"valid":True,"score":str(result),"n":n,"argmax_abs_knot":arg,"knots":2*n-1,"algorithm":"exact split-sign integer polynomial products","variant":"max(abs(f*f)), not abs(max(f*f))"}
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("certificate");a=ap.parse_args();print(json.dumps(score(json.loads(pathlib.Path(a.certificate).read_text()))))
