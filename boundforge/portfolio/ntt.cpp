// Independent modular convolution backend. No search logic or numerical FFT.
#include <bits/stdc++.h>
using namespace std;using U=uint64_t;
U power(U a,U n,U p){U r=1;for(;n;n>>=1,a=a*a%p)if(n&1)r=r*a%p;return r;}
void transform(vector<U>&a,bool inverse,U p,U primitive){
 int n=a.size();for(int i=1,j=0;i<n;i++){int bit=n>>1;for(;j&bit;bit>>=1)j^=bit;j^=bit;if(i<j)swap(a[i],a[j]);}
 for(int len=2;len<=n;len<<=1){U w=power(primitive,(p-1)/len,p);if(inverse)w=power(w,p-2,p);for(int i=0;i<n;i+=len){U cur=1;for(int j=0;j<len/2;j++){U u=a[i+j],v=a[i+j+len/2]*cur%p;a[i+j]=(u+v)%p;a[i+j+len/2]=(u+p-v)%p;cur=cur*w%p;}}}
 if(inverse){U inv=power(n,p-2,p);for(U&x:a)x=x*inv%p;}
}
int main(int argc,char**argv){bool square=argc>1&&string(argv[1])=="square";int n;cin>>n;if(n<2||n>524288)return 2;vector<string>v(n);for(auto&x:v)cin>>x;int N=1;while(N<2*n-1)N*=2;
 vector<U>primes={998244353,1004535809,469762049,1224736769,167772161,754974721},roots={3,3,3,3,3,11};
 for(int j=0;j<6;j++){U p=primes[j];for(U d=2;d*d<=p;d++)if(p%d==0)return 4;U t=p-1;vector<U>f;for(U d=2;d*d<=t;d++)if(t%d==0){f.push_back(d);while(t%d==0)t/=d;}if(t>1)f.push_back(t);for(U q:f)if(power(roots[j],(p-1)/q,p)==1)return 5;}
 cout<<"{\"primes\":[";for(int i=0;i<6;i++){if(i)cout<<",";cout<<primes[i];}cout<<"],\"coefficients\":[";
 for(int j=0;j<6;j++){U p=primes[j];if((p-1)%N)return 3;vector<U>a(N),b(N);for(int i=0;i<n;i++){U residue=0;bool negative=v[i][0]=='-';for(size_t k=negative?1:0;k<v[i].size();k++){char c=v[i][k];if(c<'0'||c>'9')return 6;residue=(residue*10+c-'0')%p;}if(negative&&residue)residue=p-residue;a[i]=residue;b[square?i:n-1-i]=residue;}transform(a,false,p,roots[j]);transform(b,false,p,roots[j]);for(int i=0;i<N;i++)a[i]=a[i]*b[i]%p;transform(a,true,p,roots[j]);if(j)cout<<",";cout<<"[";for(int i=0;i<2*n-1;i++){if(i)cout<<",";cout<<a[i];}cout<<"]";}
 cout<<"]}\n";
}
