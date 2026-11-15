"""Free structural diagnostic: continuous translation relative to the domain window.
No exact acceptance. Both positive and negative real shifts include both knot meshes.
"""
import json,os,pathlib,time,urllib.request
import numpy as np
from scipy.signal import fftconvolve
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"translation";OUT.mkdir(exist_ok=True)
def main():
 raw=urllib.request.urlopen("https://einsteinarena.com/api/solutions/best?problem_id=1&agent_name=Blob&limit=1").read();entry=json.loads(raw)[0];a=np.array(entry["data"]["values"],dtype=float);n=len(a);w=2/n
 prefix=np.r_[0,np.cumsum(a)];corr=fftconvolve(a,a[::-1])[n-1:]*w;corr=np.r_[corr,0.]
 pgrid=np.arange(n+1,dtype=float)
 def evaluate(t):
  # Exact event locations in grid-cell units: correlation integers, translated
  # window-prefix breakpoints; interpolation is numerical only.
  pp=np.r_[pgrid,n-t-pgrid];pp=pp[(pp>=0)&(pp<=n)]
  nn=np.r_[pgrid,t+pgrid];nn=nn[(nn>=0)&(nn<=n)]
  positive=w*np.interp(n-pp-t,pgrid,prefix,left=0,right=prefix[-1])-np.interp(pp,pgrid,corr)
  negative=w*(prefix[-1]-np.interp(nn-t,pgrid,prefix,left=0,right=prefix[-1]))-np.interp(nn,pgrid,corr)
  return float(positive.max()),float(negative.max())
 lo=-int(np.flatnonzero(a)[0]);hi=n-1-int(np.flatnonzero(a)[-1]);before=evaluate(0);start=time.monotonic()
 for _ in range(55):
  mid=(lo+hi)/2;p,m=evaluate(mid)
  if p>m:lo=mid
  else:hi=mid
 t=(lo+hi)/2;after=evaluate(t)
 report={"run_id":os.environ["GITHUB_RUN_ID"],"source_sha":os.environ["GITHUB_SHA"],"n":n,"before":before,"after":after,"translation_cells":t,"numerical_gain":max(before)-max(after),"elapsed_seconds":time.monotonic()-start,"scope":"Numerical only. Continuous translation is a different admissible step-function family; no record accepted without all rational event knots verified."}
 (OUT/"report.json").write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=="__main__":main()
