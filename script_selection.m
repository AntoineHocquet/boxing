% INITIALISATION
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% % ADAM et EVE
% clear all;
% close all;
% mut=0.03;
% E=10000;
% T=100;
% dt=1/100;
% Npop=100
% Nb_selec=50
% 
% N=1;
% 
% pX1=randn(24,11);
% pX2=randn(24,11);
% pY1=randn(24,11);
% pY2=randn(24,11);
% aggX1=rand;
% aggX2=rand;
% aggY1=rand;
% aggY2=rand;
% 
% REPRISE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear all;
close all;
mut=0.03;
E=10000;
T=100;
dt=1/100;
Npop=100;
Nb_selec=50;

N=200

load(['generation' num2str(N)]);

clear pX1;
clear pX2;
clear aggX1;
clear aggX2;

pX1=randn(24,11);
pX2=randn(24,11);
aggX1=rand;
aggX2=rand;

for g=1:Nb_selec

    for i=1:Npop;
        clear F;
        [PX,AGGX]=crossover(pX1,pX2,aggX1,aggX2,mut);
        [PY,AGGY]=crossover(pY1,pY2,aggY1,aggY2,mut);
%           SANS FILM
%         [vainqueur,pX(:,:,i),pY(:,:,i),agX(i),agY(i),fitX(i),fitY(i)]...
%            =match_muet(PX,AGGX,PY,AGGY,E,T,dt);
%           AVEC FILM
        [vainqueur,pX(:,:,i),pY(:,:,i),agX(i),agY(i),fitX(i),fitY(i),F]...
            =match(PX,AGGX,PY,AGGY,E,T,dt,g+N,i);
        vainqueur
        fitX(i)
        fitY(i)
    end;
    
    generation=N+g
    aggressivite=[aggX1 aggY1]
    fitmax(g,:)=[max(fitX) max(fitY)];
    [fitmax(g,1) fitmax(g,2)]

    % Choix des deux meilleurs dans chaque groupe
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    I1=arg_max(fitX);
    if (I1>=2)&&(I1<=Npop-1)
        I2=arg_max(fitX([1:I1-1 I1+1:end]));
    elseif I1==1
       I2=arg_max(fitX(2:end));
    elseif I1==Npop
      I2=arg_max(fitX(1:end-1));
    end;
    pX1=pX(:,:,I1);
    pX2=pX(:,:,I2);
    aggX1=agX(1,I1);
    aggX2=agX(1,I2);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    I1=arg_max(fitY);
    if (I1>=2)&&(I1<=Npop-1)
        I2=arg_max(fitY([1:I1-1 I1+1:end]));
    elseif I1==1
        I2=arg_max(fitY(2:end));
    elseif I1==Npop
        I2=arg_max(fitY(1:end-1));
    end;
    pY1=pY(:,:,I1);
    pY2=pY(:,:,I2);
    aggY1=agY(1,I1);
    aggY2=agY(1,I2);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
end;

N=N+Nb_selec;
savefile=['generation' num2str(N) '.mat'];
save (savefile,'N','pX1','aggX1','pX2','aggX2','pY1','aggY1','pY2','aggY2','fitmax')