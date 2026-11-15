// BoundForge exact verifier. Algorithmic BDD tuple counting is prior art.
// Independently implemented here; not claimed clean-room after reading prior checkers.
#include <bits/stdc++.h>
using namespace std;
using U=uint64_t;
struct Node{int z,o;};
struct Key{int a,b,c;bool operator==(Key const&x)const{return a==x.a&&b==x.b&&c==x.c;}};
struct KH{size_t operator()(Key const&x)const{return (size_t(x.a)*1000003+x.b)*1000003+x.c;}};
vector<U> masks;vector<Node>nodes(2);map<pair<int,int>,int>canon;
unordered_map<U,U>memo2;unordered_map<Key,U,KH>memo3;
int build(size_t l,size_t r,int bit){
 if(l==r)return 0;if(bit<0)return 1;
 size_t s=l;while(s<r&&!(masks[s]&(U(1)<<bit)))++s;
 int z=build(l,s,bit-1),o=build(s,r,bit-1);
 pair<int,int> key={z,o};auto it=canon.find(key);if(it!=canon.end())return it->second;
 int id=nodes.size();nodes.push_back({z,o});canon[key]=id;return id;
}
U pairs(int a,int b){
 if(!a||!b)return 0;if(a==1&&b==1)return 1;
 U key=(U(a)<<32)|U(b);auto it=memo2.find(key);if(it!=memo2.end())return it->second;
 Node x=nodes[a],y=nodes[b];U v=pairs(x.z,y.z)+pairs(x.z,y.o)+pairs(x.o,y.o);memo2[key]=v;return v;
}
U triples(int a,int b,int c){
 if(!a||!b||!c)return 0;if(a==1&&b==1&&c==1)return 1;
 array<int,3>s={a,b,c};sort(s.begin(),s.end());Key key{s[0],s[1],s[2]};
 auto it=memo3.find(key);if(it!=memo3.end())return it->second;
 if(memo3.size()>15000000)throw runtime_error("tuple-state budget");
 Node x=nodes[a],y=nodes[b],z=nodes[c];
 U v=triples(x.z,y.z,z.z)+triples(x.o,y.z,z.z)+triples(x.z,y.o,z.z)+triples(x.z,y.z,z.o)+triples(x.o,y.o,z.o);
 memo3[key]=v;return v;
}
int main(int argc,char**argv){try{
 if(argc!=5)throw runtime_error("usage: verifier masks n p q");
 int n=stoi(argv[2]),p=stoi(argv[3]),q=stoi(argv[4]);if(n<3||n>32||p<0||q<0||p>=n||q>=n||p==q)throw runtime_error("invalid ground set/ports");
 ifstream in(argv[1]);if(!in)throw runtime_error("input missing");
 string tok;while(in>>tok){if(tok.empty()||tok.find_first_not_of("0123456789")!=string::npos)throw runtime_error("invalid mask");U x=stoull(tok);if(x>=(U(1)<<n))throw runtime_error("mask outside universe");masks.push_back(x);}
 if(masks.empty()||masks.size()>300000)throw runtime_error("family size budget");
 sort(masks.begin(),masks.end());if(adjacent_find(masks.begin(),masks.end())!=masks.end())throw runtime_error("duplicate");
 // At most 300000^3 ordered triples fits uint64; every DP tuple count is bounded by this.
 int root=build(0,masks.size(),n-1);U m=masks.size(),P=pairs(root,root),Q=triples(root,root,root);
 array<U,4>counts{};for(U x:masks)counts[2*((x>>p)&1)+((x>>q)&1)]++;
 bool valid=P==m&&Q==m&&*min_element(counts.begin(),counts.end())>0;
 cout<<"{\"valid\":"<<(valid?"true":"false")<<",\"members\":"<<m<<",\"ordered_containments\":"<<P<<",\"ordered_equal_intersection_triples\":"<<Q<<",\"nodes\":"<<nodes.size()<<",\"counts\":["<<counts[0]<<","<<counts[1]<<","<<counts[2]<<","<<counts[3]<<"]}\n";
 return valid?0:1;
 }catch(exception const&e){cerr<<e.what()<<"\n";return 2;}}
