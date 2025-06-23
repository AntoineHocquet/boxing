function [vainqueur,p_X,p_Y,agg_X,agg_Y,fit_X,fit_Y]=match_muet(pX,aggX,pY,aggY,E,T,dt)
% 
% Même chose que match.m , mais sans getframe
% 
EX=E;
EY=E;
X=[rand-rand;rand-rand];
Y=[rand-rand;rand-rand];
vX=[0; 0];
vY=[0; 0];
eps=3/10;
prix_tir=100;
puiss_tir=1; 
gagnant='pas encore';
continuer=1;
G=[];
t=0;
tirX=0;
tirY=0;
FITNESS_X=0;
FITNESS_Y=0;
while (continuer==1)%&&(t<T)
    
    % TIR 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if (binornd(1,5*dt*aggX)==1)
        if (abs(norm(X-Y)*randn))&&(abs(norm(vX-vY)*randn))<eps
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
        else tirX=0; 
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
%     PAS DE FILM
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