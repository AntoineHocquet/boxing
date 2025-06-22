function n_=arg_max(L)
n=0;
vrai=0;
while (n<=size(L,2))&&(vrai==0)
    n=n+1;
    vrai=L(n)==max(L);
end;
n_=n;