function [p_,agg_]=crossover(p1,p2,agg1,agg2,mut)
p=zeros(24,11);
for j=1:11
    for i=1:24
        if binornd(1,mut)==1;
            p(i,j)=p(i,j)+randn;
        else qui=binornd(1,0.5);
            p(i,j)=(qui==1)*p1(i,j) + (qui==0)*p2(i,j);
        end;
    end;
end
if binornd(1,mut)==1;
    agg=rand;
else qui=binornd(1,0.5);
    agg=(qui==1)*agg1 + (qui==0)*agg2;
end;
p_=p;
agg_=agg;