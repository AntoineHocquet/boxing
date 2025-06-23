function [accX,accY] = output(pX,pY,iX,iY)

%   iX ou iY = INPUT (11x11)
%            =   [énergie restante (1x1); 
%                  position relative à l'adversaire (2x1) ; 
%                  position relative aux 4 bords (4x1);
%                  vitesse relative à l'adversaire (2x1);
%                  vitesse relative au référentiel fixe (2x1)
%            
%     Donne l'accélération en fonction des inputs iX et iY
%       et des programmes génétiques pX et pY
% 
%     Le prgm génétique est une matrice de taille 24x11
%        de sorte que les matrices carrées pX(1:11,:), et px(12:22,:)
%        donnent le terme quadratique de l'accélération et 
%        px(23:24,:) donne le terme linéaire de l'accélération.
% 
%     INPUT=vecteur colonne de taille 11x1
%     ACC=vecteur colonne de taille 2x1.
% 
% OUTPUTS (accélération)
%     -termes quadratiques en les inputs
    qX(1,1)=(iX')*pX(1:11,:)*iX;
    qX(2,1)=(iX')*pX(12:22,:)*iX;
    qY(1,1)=(iY')*pY(1:11,:)*iY;
    qY(2,1)=(iY')*pY(12:22,:)*iY;
%     -termes linéaires en les inputs
    lX=pX(23:24,:)*iX;
    lY=pX(23:24,:)*iY;

accX= lX+qX;
accY= lY+qY;