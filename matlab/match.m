function [vainqueur,p_X,p_Y,agg_X,agg_Y,fit_X,fit_Y,F]=match(pX,aggX,pY,aggY,E,T,dt,num_gene,num_combat)
% X et Y sont des matrices colonne de taille Nb_inputs
% X et Y se déplacent dans le carré [-1,1]^2
% E est l'énergie de départ de chaque individu (ne dépend pas du prgm genet)
% le but de chaque individu est de survivre à l'autre, en gérant sa
% quantité dénergie.
% Il y a 2 façons de perdre de l'énergie :
%     -vieillesse
%     -bouger
% Si E tombe à zéro, l'individu meurt. 
% T est la durée de l'affront
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Conditions initiales du match : 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
EX=E;
EY=E;
X=[rand-rand;rand-rand];
Y=[rand-rand;rand-rand];
vX=[0; 0];
vY=[0; 0];
eps=3/10; % portée des tirs
prix_tir=100; % énergie bouffée par un tir
puiss_tir=1; 
gagnant='pas encore';
continuer=1; % indique si la partie doit continuer
G=[];
t=0;
tirX=0; % indique si un tir a été effectué en début de tour ou pas
tirY=0;
FITNESS_X=0;
FITNESS_Y=0;
while (continuer==1)%&&(t<T)
    
    % TIR (précision accrue quand X et Y proches et si vX-vY petit)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if (binornd(1,5*dt*aggX)==1) % si X tire
        if (abs(norm(X-Y)*randn))&&(abs(norm(vX-vY)*randn))<eps % si tir X réussi
            tirX=1;
            FITNESS_X=FITNESS_X+dt;
            FITNESS_Y=max(FITNESS_Y-dt,0);
            EX=EX-prix_tir;
            EY=EY-3*prix_tir;
            if ((X(1,1)-Y(1,1)~=0)||(X(2,1)-Y(2,1)~=0))
                u=(Y-X)/norm(Y-X);
                vY=vY + norm(vY-vX)*u +puiss_tir*u;
            else vY=vY+randn(2,1);
            end; 
        else tirX=0; % si le tir de X est raté
            EX=EX-prix_tir;
        end;
    end;
    if  (binornd(1,5*dt*aggY)==1)
        if (abs(norm(Y-X)*randn))&&(abs(norm(vY-vX)*randn))<eps
            tirY=1;
            FITNESS_Y=FITNESS_Y+dt;
            FITNESS_X=max(FITNESS_X-dt,0);
            EY=EY-prix_tir;
            EX=EX-3*prix_tir;
            if ((X(1,1)-Y(1,1)~=0)||(X(2,1)-Y(2,1)~=0))
                u=(X-Y)/norm(X-Y);
                vX=vX + norm(vX-vY)*u +puiss_tir*u;
            else vX=vX+randn(2,1);
            end;
        else tirY=0;
            EY=EY-prix_tir;
        end;
    end;
    
    % INPUTS de X et Y
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    iX= [EX/E; % énergie restante
        Y(1,1)-X(1,1) ; Y(2,1)-X(2,1) ; % distance relative adv
        X(1,1)-1 ; X(1,1)+1; X(2,1)+1; X(2,1)-1; %distance aux 4 bords
        vY(1,1)-vX(1,1); vY(2,1)-vX(2,1) % vit. relat. adv.
        vX(1,1) ; vX(2,1)]; % vitesse
    iY= [EY/E;
        X(1,1)-Y(1,1) ; X(2,1)-Y(2,1);
        Y(1,1)-1 ; Y(1,1)+1; Y(2,1)+1; Y(2,1)-1;
        vX(1,1)-vY(1,1); vX(2,1)-vY(2,1)
        vY(1,1) ; vY(2,1)];
        
    % OUTPUTS (accélération)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    [aX,aY]=output(pX,pY,iX,iY);
    
    % nouvelles valeurs
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    vX=vX+dt*aX;
    vY=vY+dt*aY;
    X=X+dt*vX;
    Y=Y+dt*vY;
    EX=EX-dt*norm(aX);
    EY=EY-dt*norm(aY);
    % Collision au bord
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if (norm(X,inf)>=1)&&(norm(Y,inf)>=1)
        EX=EX-norm(vX);
        EY=EY-norm(vY);
         X=X/norm(X,inf);
         Y=Y/norm(Y,inf);
         vX= [-vX(1,1)*(abs(X(1,1))>=1)+vX(1,1)*(abs(X(1,1))<1);
             -vX(2,1)*(abs(X(2,1))>=1)+vX(2,1)*(abs(X(2,1))<1)];
         vY= [-vY(1,1)*(abs(Y(1,1))>=1)+vY(1,1)*(abs(Y(1,1))<1);
             -vY(2,1)*(abs(Y(2,1))>=1)+vY(2,1)*(abs(Y(2,1))<1)];
    elseif (norm(X,inf)>=1)&&(norm(Y,inf)<1)
        EX=EX-norm(vX);
        X=X/norm(X,inf);
         vX= [-vX(1,1)*(abs(X(1,1))>=1)+vX(1,1)*(abs(X(1,1))<1);
             -vX(2,1)*(abs(X(2,1))>=1)+vX(2,1)*(abs(X(2,1))<1)];
    elseif (norm(X,inf)<1)&&(norm(Y,inf)>=1)
         EY=EY-norm(vY);
         Y=Y/norm(Y,inf);
         vY= [-vY(1,1)*(abs(Y(1,1))>=1)+vY(1,1)*(abs(Y(1,1))<1);
             -vY(2,1)*(abs(Y(2,1))>=1)+vY(2,1)*(abs(Y(2,1))<1)];
    end;

    % état de la partie (energie)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if (EX<=0)&&(EY<=0)
        if FITNESS_X==FITNESS_Y
            gagnant='aucun';g=0;
        elseif FITNESS_X>FITNESS_Y
            gagnant='individu X';g=1;
        else gagnant='individu Y';g=2;
        end;
        continuer=0;
    elseif (EX>0)&&(EY<=0)
        gagnant='individu X';g=1;
        continuer=0;
    elseif (EX<=0)&&(EY>0)
        gagnant='individu Y';g=2;
        continuer=0;
    end;
        
        
        
    
    if (tirX==1)&&(tirY==1)
        plot(X(1,1),X(2,1),'ob',Y(1,1),Y(2,1),'or',[X(1,1) Y(1,1)],[X(2,1) Y(2,1)],'-g')
        axis([-1.1 1.1 -1.1 1.1])
        title(['Generation ' num2str(num_gene) ', Combat n°' num2str(num_combat) ', t=' num2str(t) ', E(X)=' num2str(floor(EX)) ', E(Y)=' num2str(floor(EY))])
        G=[G getframe];
    elseif (tirX==1)&&(tirY==0)
        plot(X(1,1),X(2,1),'ob',Y(1,1),Y(2,1),'or',[X(1,1) Y(1,1)],[X(2,1) Y(2,1)],'-b')
        axis([-1.1 1.1 -1.1 1.1])
        title(['Generation ' num2str(num_gene) ', Combat n°' num2str(num_combat) ', t=' num2str(t) ', E(X)=' num2str(floor(EX)) ', E(Y)=' num2str(floor(EY))])
        G=[G getframe];
    elseif (tirX==0)&&(tirY==1)
        plot(X(1,1),X(2,1),'ob',Y(1,1),Y(2,1),'or',[X(1,1) Y(1,1)],[X(2,1) Y(2,1)],'-r')
        axis([-1.1 1.1 -1.1 1.1])
        title(['Generation ' num2str(num_gene) ', Combat n°' num2str(num_combat) ', t=' num2str(t) ', E(X)=' num2str(floor(EX)) ', E(Y)=' num2str(floor(EY))])
        G=[G getframe];
    else plot(X(1,1),X(2,1),'ob',Y(1,1),Y(2,1),'or')
        axis([-1.1 1.1 -1.1 1.1])
        title(['Generation ' num2str(num_gene) ', Combat n°' num2str(num_combat) ', t=' num2str(t) ', E(X)=' num2str(floor(EX)) ', E(Y)=' num2str(floor(EY))])
        G=[G getframe];
    end;
    
    t=t+dt;
    if t<20
        FITNESS_X=FITNESS_X+dt;
        FITNESS_Y=FITNESS_Y+dt;
    end;
end;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
vainqueur=gagnant;
p_X=pX;
p_Y=pY;
agg_X=aggX;
agg_Y=aggY;
fit_X=(g==0)*(FITNESS_X+FITNESS_Y)/10 + (g==1)*(FITNESS_X + 2*abs(FITNESS_X-FITNESS_Y));
fit_Y=(g==0)*(FITNESS_X+FITNESS_Y)/10 + (g==2)*(FITNESS_Y + 2*abs(FITNESS_Y-FITNESS_X));
F= G;