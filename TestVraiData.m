clear;
clc;
%%
L = 10; %% Largeur de filtre, Plus L est grand plus le filtrage est intense
load('Dataraw1');
Light = mean(DataSet1fknDown(4:4:end,1));
IR = DataSet1fknDown(1:4:end,1)-Light;
R = DataSet1fknDown(3:4:end,1)-Light;


%% filtre PB
f = 1/L*ones(L,1);
R = conv(R,f);
IR = conv(IR,f);

%%
R = R(L:length(R)-L);
IR = IR(L:length(IR)-L);

RDC = mean(R);
IRDC = mean(IR);
RAC = R-min(R)+1;
IRAC = IR-min(IR)+1;



plot(IRAC);
hold on
plot(RAC)

SaO2 = 110 -25*((RAC/RDC)./(IRAC/IRDC));



