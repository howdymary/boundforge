// Shared bounded ruin/repair engine. Proposal ranking only; no record acceptance here.
#include <bits/stdc++.h>
using namespace std;using U=uint64_t;
int kind,n,param,action,budgetms,N;uint64_t seedv;mt19937_64 rng;
vector<vector<bool>>adj;vector<vector<int>>third;U tried=0,rejected=0,attempts=0,mismatch=0;
clock_t beginCPU;
bool expired(){return 1000.0*(clock()-beginCPU)/CLOCKS_PER_SEC>=budgetms;}
bool legal(int x,vector<int>const&s){
 tried++;
 if(kind==0){
  for(int a:s)if((a&x)==a||(a&x)==x){rejected++;return false;}
  for(size_t i=0;i<s.size();i++)for(size_t j=0;j<i;j++)if((s[i]&s[j])==(s[i]&x)&&(s[i]&s[j])==(s[j]&x)){rejected++;return false;}
 }else if(kind==1){
  for(int a:s)if(adj[x][a]){rejected++;return false;}
 }else{
  vector<bool>has(N);for(int a:s)has[a]=true;
  for(int a:s)if(has[third[x][a]]){rejected++;return false;}
 }
 return true;
}
struct Score{double v;int p,q;array<int,4>c;};
Score score(vector<int>const&s){
 if(kind!=0)return {double(s.size()),0,1,{0,0,0,0}};
 Score best{0,0,1,{0,0,0,0}};
 for(int p=0;p<n;p++)for(int q=p+1;q<n;q++){
  array<int,4>c{};for(int x:s)c[2*((x>>p)&1)+((x>>q)&1)]++;
  if(*min_element(c.begin(),c.end())==0)continue;
  double b=c[1],cc=c[2],rho=(b+cc+sqrt((b-cc)*(b-cc)+4.0*c[0]*c[3]))/2;
  double v=pow(rho,1.0/(n-2));if(v>best.v)best={v,p,q,c};
 }
 return best;
}
vector<int> repair(vector<int>s){
 vector<bool>present(N);for(int x:s)present[x]=true;
 vector<pair<double,int>>order;int center=kind==0?max(1,min(n-1,n/2+int(rng()%3)-1)):0;
 Score ss=score(s);
 for(int x=kind==0?1:0;x<N-(kind==0);x++)if(!present[x]){
  double pr=double(rng()%1000000)/1000000.0;
  if(kind==0)pr-=.6*abs(__builtin_popcount((unsigned)x)-center);
  if(action==5&&kind==0){int cell=2*((x>>ss.p)&1)+((x>>ss.q)&1);pr+=.4/(1+ss.c[cell]);}
  order.push_back({pr,x});
 }
 sort(order.rbegin(),order.rend());
 for(auto[pr,x]:order){if(expired())break;if(legal(x,s)){s.push_back(x);present[x]=true;}}
 return s;
}
vector<int> ruin(vector<int>s){
 int k=action==0?2:action==1?6:action==2?max(12,int(s.size()/3)):action==3?s.size():6;
 shuffle(s.begin(),s.end(),rng);k=min(k,int(s.size()));
 if(action==4&&!s.empty()){
  vector<pair<int,int>>rank;
  for(int a:s){int hit=0;for(int t=0;t<32;t++){int x=rng()%N;if(kind==0)hit+=((a&x)==a||(a&x)==x);else if(kind==1)hit+=adj[a][x];else hit+=find(s.begin(),s.end(),third[a][x])!=s.end();}rank.push_back({hit,a});}
  sort(rank.rbegin(),rank.rend());s.clear();for(auto[h,a]:rank)s.push_back(a);
 }else if(action==5&&!s.empty()){
  Score sc=score(s);
  if(kind==0)stable_sort(s.begin(),s.end(),[&](int a,int b){return sc.c[2*((a>>sc.p)&1)+((a>>sc.q)&1)]>sc.c[2*((b>>sc.p)&1)+((b>>sc.q)&1)];});
  else if(kind==1)stable_sort(s.begin(),s.end(),[&](int a,int b){return count(adj[a].begin(),adj[a].end(),true)>count(adj[b].begin(),adj[b].end(),true);});
 }
 s.erase(s.begin(),s.begin()+k);return s;
}
int main(){try{
 int m;cin>>kind>>n>>param>>m>>seedv>>action>>budgetms;if(!cin||kind<0||kind>2||action<0||action>5||budgetms<1||budgetms>30000)throw runtime_error("invalid protocol");
 rng.seed(seedv);vector<int>s(m);for(int&i:s)cin>>i;
 beginCPU=clock();
 if(kind==0){if(n<3||n>12)throw runtime_error("C49 universe cap");N=1<<n;}
 else if(kind==1){N=n;adj.assign(N,vector<bool>(N));mt19937_64 gr(param);for(int i=0;i<N;i++)for(int j=0;j<i;j++)adj[i][j]=adj[j][i]=(gr()%100)<20;}
 else{N=1;for(int i=0;i<n;i++)N*=3;if(N>243)throw runtime_error("cap-set universe cap");third.assign(N,vector<int>(N));for(int a=0;a<N;a++)for(int b=0;b<N;b++){int aa=a,bb=b,mul=1,c=0;for(int d=0;d<n;d++){c+=((6-aa%3-bb%3)%3)*mul;aa/=3;bb/=3;mul*=3;}third[a][b]=c;}}
 vector<int>sorted=s;sort(sorted.begin(),sorted.end());if(adjacent_find(sorted.begin(),sorted.end())!=sorted.end())throw runtime_error("duplicates");
 for(int x:s)if(x<0||x>=N)throw runtime_error("range");
 Score initial=score(s),best=initial,cur=initial;vector<int>bs=s;
 while(!expired()){
  auto proposal=repair(ruin(s));auto sc=score(proposal);attempts++;
  if(proposal.size()>s.size()&&sc.v+1e-14<cur.v)mismatch++;
  if(sc.v>best.v+1e-14){best=sc;bs=proposal;}
  if(sc.v>=cur.v-1e-14||(rng()%20==0)){s=proposal;cur=sc;}
 }
 auto printvec=[](vector<int>v){sort(v.begin(),v.end());cout<<"[";for(size_t i=0;i<v.size();i++){if(i)cout<<",";cout<<v[i];}cout<<"]";};
 cout<<setprecision(17)<<"{\"score\":"<<cur.v<<",\"best_score\":"<<best.v<<",\"initial_score\":"<<initial.v<<",\"ports\":["<<cur.p<<","<<cur.q<<"],\"best_ports\":["<<best.p<<","<<best.q<<"],\"tested\":"<<tried<<",\"rejected\":"<<rejected<<",\"trials\":"<<attempts<<",\"cardinality_rate_mismatches\":"<<mismatch<<",\"cpu_seconds\":"<<double(clock()-beginCPU)/CLOCKS_PER_SEC<<",\"state\":";
 printvec(s);cout<<",\"best_family\":";printvec(bs);cout<<"}\n";return 0;
 }catch(exception const&e){cerr<<e.what()<<"\n";return 2;}}
