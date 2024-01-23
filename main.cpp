#include <iostream>
#include <fstream>
#include <time.h>
#include <stdlib.h>
#include <bits/stdc++.h>
#define MAX_NUM 2
using namespace std;
ifstream fin("date.in");
ofstream fout("date.out");
float S,ST;
void randnum(int n,int M[][31])
{
    int random;
    srand(time(NULL));
    for(int i=1;i<=n;i++)
        for(int j=1;j<=n;j++)
        {
            M[i][j]=rand()%MAX_NUM;
            if(M[i][j]==0)
                M[i][j]=rand()%MAX_NUM;
        }
    for(int i=1;i<=n;i++)
        for(int j=1;j<=n;j++)
            if(M[i][j])M[i][j]=2;
}
void simulare(int x,int y,int M[][31],int n)
{
    int C[31][31],secunde=0;
    float p=0;
    for(int i=1;i<=n;i++)
        for(int j=1;j<=n;j++)
            C[i][j]=M[i][j];

    C[x][y]=-1;
    int ok=0;
    while(ok==0)
    {
        if(ok==0)
        {
            /*for(int i=1;i<=n;i++)
            {
                for(int j=1;j<=n;j++)
                    fout<<setw(3)<<C[i][j]<<" ";
                fout<<"\n";

            }
            fout<<"\n";*/
        }
        ok=1;
        secunde++;
        for(int i=1;i<=n;i++)
            for(int j=1;j<=n;j++)
            {
                if(C[i][j]==1)C[i][j]=0,ok=0;
                if(C[i][j]==-1 || C[i][j]==(secunde*(-1)))
                {
                    ok=0;
                    C[i][j]=1;
                    if(C[i+1][j]==2)C[i+1][j]=(secunde+1)*(-1);
                    if(C[i-1][j]==2)C[i-1][j]=(secunde+1)*(-1);
                    if(C[i][j+1]==2)C[i][j+1]=(secunde+1)*(-1);
                    if(C[i][j-1]==2)C[i][j-1]=(secunde+1)*(-1);

                }
            }

    }
    for(int i=1;i<=n;i++)
        for(int j=1;j<=n;j++)
            if(C[i][j])p++;
    p=p/(n*n)*100;
    S+=p;
    ST+=secunde-1;
    ///fout<<"procentaj "<<p<<" secunde:"<<secunde-1<<endl;
    ///fout<<"\n";
}
int n;
float pinit;
int main()
{
    fin>>n;
    int M[31][31];
    /*for(int i=1;i<=n;i++)
        for(int j=1;j<=n;j++)
            fin>>M[i][j];*/
    for(int i=1;i<=100;i++)
    {

        randnum(n,M);
        fout<<"matricea initiala"<<endl;
        for(int i=1;i<=n;i++)
        {
            for(int j=1;j<=n;j++)
            {
                fout<<setw(3)<<M[i][j]<<" ";
                if(M[i][j]==2)
                    pinit++;
            }
            fout<<endl;
        }
        ///fout<<pinit/(n*n)*100<<"% copaci"<<endl;
        int cont=0;
            for(int i=1;i<=n;i++)
                for(int j=1;j<=n;j++)
                    if(M[i][j]==2)
                    {
                        cont++;
                        ///fout<<"simularea "<<cont<<endl;
                        simulare(i,j,M,n);
                    }

        S=(S/pinit);
        ST=(ST/pinit);
        fout<<"CONCLUSION"<<endl;
        fout<<"% initial copaci "<<pinit/(n*n)*100<<endl;
        fout<<"% final copaci "<<S<<endl;
        fout<<" timp "<<ST<<endl;
        pinit=0;
        S=0;
        ST=0;
    }

    return 0;
}