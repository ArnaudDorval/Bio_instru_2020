clear;
clc;
hold off
hold on
%% Chargement des données
load('etiennedata1');
load('benjamindata');
load('arnauddata');
load('Dataraw1');


Light = mean(etiennedata1(4:4:4411,2));
IR = (etiennedata1(1:4:4411,2)-Light)*3.3/(2^16);
R = (etiennedata1(3:4:4411,2)-Light)*3.3/(2^16);



%% Composante DC des signaux

RDC = mean(R);
IRDC = mean(IR);
%% filtre PB
% On veut enlever le gros bruit
L = 25; %% Largeur de filtre, Plus L est grand plus le filtrage est intense
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



L2 = 10; %% Largeur de filtre, Plus L est grand plus le filtrage est intense
f2 = 1/L2*ones(L2,1);

RAC= conv(RAC,f2);
IRAC = conv(IRAC,f2);



RAC = RAC(L:length(RAC)-L);
IRAC = IRAC(L:length(IRAC)-L);
% 
% HpkR = findpeaks(RAC,1,'MinPeakDistance',70);
% LpkR = -findpeaks(-RAC,1,'MinPeakDistance',70);
% 
% HpkIR = findpeaks(IRAC,1,'MinPeakDistance',70);
% LpkIR = -findpeaks(-RAC,1,'MinPeakDistance',70);
% 
% RAC = HpkR-LpkR;
% IRAC = HpkIR-LpkIR;

plot(RAC)
plot(IRAC)
legend('R','IR')




%%
SaO2 =110-25*((RAC/RDC)./(IRAC/IRDC));
meanSaO2 = mean(SaO2)