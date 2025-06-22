function [accX,accY] = output(pX,pY,iX,iY)

%   iX ou iY = INPUT (11x11)
%            =   [�nergie restante (1x1); 
%                  position relative � l'adversaire (2x1) ; 
%                  position relative aux 4 bords (4x1);
%                  vitesse relative � l'adversaire (2x1);
%                  vitesse relative au r�f�rentiel fixe (2x1)
%            
%     Donne l'acc�l�ration en fonction des inputs iX et iY
%       et des programmes g�n�tiques pX et pY
% 
%     Le prgm g�n�tique est une matrice de taille 24x11
%        de sorte que les matrices carr�es pX(1:11,:), et px(12:22,:)
%        donnent le terme quadratique de l'acc�l�ration et 
%        px(23:24,:) donne le terme lin�aire de l'acc�l�ration.
% 
%     INPUT=vecteur colonne de taille 11x1
%     ACC=vecteur colonne de taille 2x1.
% 
% OUTPUTS (acc�l�ration)
%     -termes quadratiques en les inputs
    qX(1,1)=(iX')*pX(1:11,:)*iX;
    qX(2,1)=(iX')*pX(12:22,:)*iX;
    qY(1,1)=(iY')*pY(1:11,:)*iY;
    qY(2,1)=(iY')*pY(12:22,:)*iY;
%     -termes lin�aires en les inputs
    lX=pX(23:24,:)*iX;
    lY=pX(23:24,:)*iY;

accX= lX+qX;
accY= lY+qY;