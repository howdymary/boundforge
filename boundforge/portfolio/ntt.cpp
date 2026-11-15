// Independent modular convolution backend. No search logic or numerical FFT.
#include <bits/stdc++.h>
using namespace std;using U=uint64_t;
U power(U a,U n,U p){U r=1;for(;n;n>>=1,a=a*a%p)if(n&1)r=r*a%p;return r;}
void transform(vector<U>&a,bool inverse,U p){
 int n=a.size();for(int i=1,j=0;i<n;i++){int bit=n>>1;for(;j&bit;bit>>=1)j^=bit;j^=bit;if(i<j)swap(a[i],a[j]);}
 for(int len=2;len<=n;len<<=1){U w=power(3,(p-1)/len,p);if(inverse)w=power(w,p-2,p);for(int i=0;i<n;i+=len){U cur=1;for(int j=0;j<len/2;j++){U u=a[i+j],v=a[i+j+len/2]*cur%p;a[i+j]=(u+v)%p;a[i+j+len/2]=(u+p-v)%p;cur=cur*w%p;}}}
 if(inverse){U inv=power(n,p-2,p);for(U&x:a)x=x*inv%p;}
}
int main(){int n;cin>>n;if(n<2||n>524288)return 2;vector<U>v(n);for(auto&x:v)cin>>x;int N=1;while(N<2*n-1)N*=2;
 vector<U>primes={998244353,1004535809,469762049,1224736769};
 cout<<"{\"primes\":[";for(int i=0;i<4;i++){if(i)cout<<",";cout<<primes[i];}cout<<"],\"coefficients\":[";
 for(int j=0;j<4;j++){U p=primes[j];if((p-1)%N)return 3;vector<U>a(N),b(N);for(int i=0;i<n;i++){a[i]=v[i]%p;b[n-1-i]=v[i]%p;}transform(a,false,p);transform(b,false,p);for(int i=0;i<N;i++)a[i]=a[i]*b[i]%p;transform(a,true,p);if(j)cout<<",";cout<<"[";for(int i=0;i<2*n-1;i++){if(i)cout<<",";cout<<a[i];}cout<<"]";}
 cout<<"]}\n";
}
