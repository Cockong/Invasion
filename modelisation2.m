%% PRV 2D: 

% parametre des equations
beta = 0.1;
D = 2;

% parametres de simulation, espace
s = 10; % taille domaine (carre sxs)
h = 1;
x0 = 0;
x1 = s;
y0 = 0;
y1 = s;
x = x0:h:x1;
y = y0:h:y1;
[X,Y] = meshgrid(x,y);
J = length(x);
J2 = J*J;

% test

% variable dynamiques
P = zeros(J,J); % stocke seulement l'etat au temps t
R = zeros(J,J);
V = zeros(J,J);
newP = zeros(J,J);
newR = zeros(J,J);
newV = zeros(J,J);

% Condition periodiques
L = sparse(1:J2,1:J2,-4); % matrice creuse, compacte en memoire
coinhautgauche = 1;
coinbasgauche = J;
coinhautdroit = J*(J-1)+1;
coinbasdroit = J2;
bordgauche = 2:J-1;
bordhaut = J+1:J:J*(J-2)+1;
bordbas = 2*J:J:J*(J-1);
borddroit = J*(J-1)+2:J2-1;
bord = [coinhautgauche, coinhautdroit, coinbasgauche, coinbasdroit, ...
    bordgauche, bordhaut, bordbas, borddroit];
interieur = setdiff(1:J2, bord);

% interieur
L = L + sparse(interieur,interieur+1,1,J2,J2);
L = L + sparse(interieur,interieur-1,1,J2,J2);
L = L + sparse(interieur,interieur+J,1,J2,J2);
L = L + sparse(interieur,interieur-J,1,J2,J2);

% bords
L = L + sparse(bordhaut,bordhaut+1,1,J2,J2);
L = L + sparse(bordhaut,bordhaut+J-1,1,J2,J2);
L = L + sparse(bordhaut,bordhaut+J,1,J2,J2);
L = L + sparse(bordhaut,bordhaut-J,1,J2,J2);


L = L + sparse(bordgauche,bordgauche+1,1,J2,J2);
L = L + sparse(bordgauche,bordgauche-1,1,J2,J2);
L = L + sparse(bordgauche,bordgauche+J,1,J2,J2);
L = L + sparse(bordgauche,bordgauche+J*(J-1),1,J2,J2);

L = L + sparse(bordbas,bordbas-(J-1),1,J2,J2);
L = L + sparse(bordbas,bordbas-1,1,J2,J2);
L = L + sparse(bordbas,bordbas+J,1,J2,J2);
L = L + sparse(bordbas,bordbas-J,1,J2,J2);

L = L + sparse(borddroit,borddroit+1,1,J2,J2);
L = L + sparse(borddroit,borddroit-1,1,J2,J2);
L = L + sparse(borddroit,borddroit-J*(J-1),1,J2,J2);
L = L + sparse(borddroit,borddroit-J,1,J2,J2);

% coins
L(coinhautgauche,coinhautgauche+1) = 1;
L(coinhautgauche,coinhautgauche+J-1) = 1;
L(coinhautgauche,coinhautgauche+J) = 1;
L(coinhautgauche,coinhautgauche+J*(J-1)) = 1;


L(coinbasgauche,coinbasgauche-(J-1)) = 1;
L(coinbasgauche,coinbasgauche-1) = 1;
L(coinbasgauche,coinbasgauche+J) = 1;
L(coinbasgauche,coinbasgauche+J*(J-1)) = 1;

L(coinhautdroit,coinhautdroit+1) = 1;
L(coinhautdroit,coinhautdroit+J-1) = 1;
L(coinhautdroit,coinhautdroit-J*(J-1)) = 1;
L(coinhautdroit,coinhautdroit-J) = 1;

L(coinbasdroit,coinbasdroit-(J-1)) = 1;
L(coinbasdroit,coinbasdroit-1) = 1;
L(coinbasdroit,coinbasdroit-J*(J-1)) = 1;
L(coinbasdroit,coinbasdroit-J) = 1;

% condition initiales
P(1,5) = 100;
R(7,1) = 100;
V(7,9) = 100;

%P = randi(2,J,J);
%R = randi(2,J,J);
%V = randi(2,J,J);



% parametres de simulation, temps
t0 = 0;
tfinal = 50; 
t = t0;
% k doit etre < a h^2/2/d/D ou dim d = 2
k = min(1,0.2*( h^2/4/max(D)));

 

figure(1); clf;
surf(X,Y,P,'EdgeColor','none'); hold on
surf(X,Y,R,'EdgeColor','none'); hold on
surf(X,Y,V,'EdgeColor','none'); hold off
view(2)
drawnow;
tk = 0;

pause

% BOUCLE PRINCIPALE
while t < tfinal
    drawnow;
    newP = -beta*P.*R+beta*V.*P+reshape((D*k/h^2)*L*reshape(P,J2,1),J,J);
    newR = -beta*R.*V+beta*P.*R+reshape((D*k/h^2)*L*reshape(R,J2,1),J,J);
    newV = -beta*V.*P+beta*R.*V+reshape((D*k/h^2)*L*reshape(V,J2,1),J,J);
    
    P = newP;
    R = newR;
    V = newV;
    if tk > 1 
        t
        P
        surf(X,Y,P,'EdgeColor','none'); hold on
        surf(X,Y,R,'EdgeColor','none'); hold on
        surf(X,Y,V,'EdgeColor','none'); hold off
        view(2)
        drawnow;
        tk = 0;
    end
    t = t + k;
    tk = tk + k;
end