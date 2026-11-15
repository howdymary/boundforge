import numpy as np
def test_block_derivative_matches_exact_quadratic():
 rng=np.random.default_rng(4901)
 for n in [17,32]:
  x=rng.normal(size=n);edges=np.linspace(0,n,6,dtype=int);b=rng.normal(size=5)
  h=np.repeat(b,np.diff(edges));idx=np.arange(2*n-1);p=np.r_[0,np.cumsum(x)]
  A=2*(p[np.clip(idx[:,None]-edges[:-1]+1,0,n)]-p[np.clip(idx[:,None]-edges[1:]+1,0,n)])
  assert np.max(np.abs(A@b-2*np.convolve(x,h)))<1e-12
  for alpha in [.001,.1]:
   lhs=np.convolve(x+alpha*h,x+alpha*h)
   rhs=np.convolve(x,x)+alpha*(A@b)+alpha**2*np.convolve(h,h)
   assert np.max(np.abs(lhs-rhs))<1e-12
