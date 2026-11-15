#include <bits/stdc++.h>
int main(int argc,char**argv){int n=std::stoi(argv[1]);std::mt19937_64 r(std::stoull(argv[2]));bool first=true;std::cout<<"[";for(int i=0;i<n;i++)for(int j=0;j<i;j++)if(r()%100<20){if(!first)std::cout<<",";first=false;std::cout<<"["<<i<<","<<j<<"]";}std::cout<<"]\n";}
