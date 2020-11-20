clear;
clc;
% hold off
hold on
%% Chargement des données
load('EtienneParsedData');
load('BenjaminParsedData');
load('ArnaudParsedData');
load('Dataraw1');


% Light = mean(EtienneSetA(4:4:end,2));
% IR = (EtienneSetA(1:4:end-2,2)-Light)*3.3/(2^16);
% R = (EtienneSetA(3:4:end,2)-Light)*3.3/(2^16);

Light = mean(DataSet1fknDown(4:4:end,1));
IR = (DataSet1fknDown(1:4:end-2,1)-Light)*3.3/(2^16);
R = (DataSet1fknDown(3:4:end,1)-Light)*3.3/(2^16);

% Light = mean(ArnaudSetD(4:4:end,2));
% IR = (ArnaudSetD(1:4:end-2,2)-Light)*3.3/(2^16);
% R = (ArnaudSetD(3:4:end,2)-Light)*3.3/(2^16);

% Light = mean(BenjaminSetD(4:4:end,2));
% IR = (BenjaminSetD(1:4:end-2,2)-Light)*3.3/(2^16);
% R = (BenjaminSetD(3:4:end,2)-Light)*3.3/(2^16);
%% Composante DC des signaux
RDC = mean(R);
IRDC = mean(IR);
%% filtre PB
ParaPB = 0.03;
[R,PB1] = lowpass(R,ParaPB);
[IR,PB2] = lowpass(IR,ParaPB);
R = R(length(PB1.Coefficients):length(R)-length(PB1.Coefficients));
IR = IR(length(PB2.Coefficients):length(IR)-length(PB2.Coefficients));
%% Composante AC

RAC = R - mean(R);
IRAC = IR - mean(IR);
%% Filtre passe haut
% On veut enlever la composante DC plus ParaPH est haut, plus la fréquence
% de coupur est haute
ParaPH = 0.01;
[RAC, PH1] = highpass(RAC,ParaPH);
[IRAC, PH2] = highpass(IRAC,ParaPH);
RAC = RAC(length(PH1.Coefficients):length(RAC)-length(PH1.Coefficients));
IRAC = IRAC(length(PH2.Coefficients):length(IRAC)-length(PH2.Coefficients));
plot(RAC)
plot(IRAC)
legend('R','IR')
xlabel('temps [ms]');
ylabel('tension AC [V]');
%%
SaO2 =110-25*(rms((RAC)/RDC)./(rms(IRAC)/IRDC));
meanSaO2 = trimmean(SaO2,5) % trouve la moyenne des valeurs excluant les 20% des valeurs
%%les plus loin de la moyenne (données abérantes)