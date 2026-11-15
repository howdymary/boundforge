// Exact histograms for a two-coordinate finite alphabet and linear total cost.
#include <bits/stdc++.h>
using namespace std;
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int B,n;while(cin>>B>>n){if(B<1||B>160||n<2||n>(B+1)*(B+1))return 2;vector<pair<int,int>>v(n);for(auto&[a,b]:v)cin>>a>>b;int q=2*B+1;vector<unsigned short>cost(q*q,65535);vector<unsigned char>has(q*q);
for(auto[a,b]:v)for(auto[c,d]:v){has[(a+c)+q*(b+d)]=1;int k=(a-c+B)+q*(b-d+B);unsigned short w=a+b+c+d;if(w<cost[k])cost[k]=w;}
vector<int>minus(4*B+1),plus(4*B+1);int dc=0,sc=0;
for(int y=0;y<q;y++)for(int x=0;x<q;x++){int i=x+q*y;if(cost[i]!=65535){minus[cost[i]]++;dc++;}if(has[i]){plus[x+y]++;sc++;}}
cout<<"{\"minus\":[";for(int i=0;i<=4*B;i++){if(i)cout<<",";cout<<minus[i];}cout<<"],\"plus\":[";for(int i=0;i<=4*B;i++){if(i)cout<<",";cout<<plus[i];}cout<<"],\"differences\":"<<dc<<",\"sums\":"<<sc<<"}\n"<<flush;
}}
