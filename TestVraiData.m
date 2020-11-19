clear;
clc;
hold off
hold on
%% Chargement des données

load('Dataraw1');
Light = mean(DataSet1fknDown(4:4:end,1));
IR = (DataSet1fknDown(1:4:end,1)-Light)*3.3/(2^16);
R = (DataSet1fknDown(3:4:end,1)-Light)*3.3/(2^16);


%% Composante DC des signaux

RDC = mean(R);
IRDC = mean(IR);
%% filtre PB
% On veut enlever le gros bruit
L = 20; %% Largeur de filtre, Plus L est grand plus le filtrage est intense
f = 1/L*ones(L,1);
R = conv(R,f);
IR = conv(IR,f);
R = R(L:length(R)-L);
IR = IR(L:length(IR)-L);
%% Filtre passe haut
% On veut enlever la composante DC
ParaPH = 0.007;
RAC = highpass(R,ParaPH);
IRAC = highpass(IR,ParaPH);

%% Deuxieme filtre passe bas

L2 = 5; %% Largeur de filtre, Plus L est grand plus le filtrage est intense
f2 = 1/L2*ones(L2,1);

RAC= conv(RAC,f2);
IRAC = conv(IRAC,f2);

%% plot signal AC


RAC = RAC(L:length(RAC)-L);
IRAC = IRAC(L:length(IRAC)-L);


plot(RAC)
plot(IRAC);
legend('R','IR')




%%
SaO2 =110-25*((RAC/RDC)./(IRAC/IRDC));
meanSaO2 = mean(SaO2)