clear;
clc;
hold off
hold on
%% Chargement des données
load('EtienneParsedData');
load('BenjaminParsedData');
load('ArnaudParsedData');
load('Dataraw1');


Light = mean(ArnaudSetD(4:4:end,2));
IR = (ArnaudSetD(1:4:end-2,2)-Light)*3.3/(2^16);
R = (ArnaudSetD(3:4:end,2)-Light)*3.3/(2^16);

% plot(R)
% plot(IR)

%% Composante DC des signaux

RDC = mean(R);
IRDC = mean(IR);
%% filtre PB
% On veut enlever le gros bruit
L = 10; %% Largeur de filtre, Plus L est grand plus le filtrage est intense
f = 1/L*ones(L,1);
R = conv(R,f);
IR = conv(IR,f);
R = R(L:length(R)-L);
IR = IR(L:length(IR)-L);


% plot(R)
% plot(IR)

%% Filtre passe haut
% On veut enlever la composante DC
ParaPH = 0.007;
RAC = highpass(R,ParaPH);
IRAC = highpass(IR,ParaPH);

% plot(RAC)
% plot(IRAC)

%% Deuxieme filtre passe bas



L2 = 20; %% Largeur de filtre, Plus L est grand plus le filtrage est intense
f2 = 1/L2*ones(L2,1);

RAC= conv(RAC,f2);
IRAC = conv(IRAC,f2);



RAC = -RAC(L:length(RAC)-L);
IRAC = -IRAC(L:length(IRAC)-L);

RAC = RAC - mean(RAC);
IRAC = IRAC - mean(IRAC);


plot(RAC)
plot(IRAC)
legend('R','IR')




%%
SaO2 =110-25*((rms(RAC)/RDC)./(rms(IRAC)/IRDC));
meanSaO2 = trimmean(SaO2,10) % trouve la moyenne des valeurs excluant les 20% des valeurs
%%les plus loin de la moyenne (données abérantes)