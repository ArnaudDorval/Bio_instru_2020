%% Traitement de donn�es
clear;
clc;
%% Cr�ation vecteur de data (simulation)
Nbdata = 10000; % Nombre de conn�es dans le dataset
x = linspace(1,Nbdata/4,Nbdata/4);
l = exp(-(x/200)); % ampleur de la croissance/d�croissance exponentielle (amortissement premier ordre)
R = 2.8*ones(1,Nbdata/4); % valeur d'amplitude de rouge
B = zeros(1,Nbdata/4); % valeur d'amplitude baseline
IR = 3.1*ones(1,Nbdata/4); % valeur d'amplitude IR
Indicateur = linspace(0,2,Nbdata)'; %Vecteur indicateur
Timestamp = linspace(0,2,Nbdata)'; %vecteur timestamp
Values = [R-l B+l IR-l B+l]'; % Vecteur de valeurs sans bruit ajout�
Bruit = 0.5*rand(Nbdata,1); % bruit ajout�
ValuesBruitees = Values+Bruit;





RawData = [Indicateur ValuesBruitees Timestamp];
plot(RawData(:,2))
Data = RawData(:,2);

%% Filtrage, on usilise un filtre � moyenne mobile de 1/10 de la largeur des bandes de donn�es
hold on
L = 8; % 1/L est la fraction le la largeur d'une bande, Plus on diminue L, plus le filtre sera intense
M = floor(Nbdata/(4*L)); % 4 parce qu'on a 4 bandes de donn�es par mesure
Filtre1 = 1/M*ones(M,1);
T = conv(Filtre1,Data);
T = T(1:10000);
plot(T)
%%
