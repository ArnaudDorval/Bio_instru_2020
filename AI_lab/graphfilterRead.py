import filterLib as lib
import matplotlib.pyplot as pyplot
from matplotlib import style
import pandas as pd
import numpy as np
from scipy import stats
import pickle
import sklearn

selection = input("> file: ")
data = pd.read_csv(selection + ".csv", sep=",")
data = data[["TAG", "Value", "Time"]]

#get data avec bruit
baseline_mask = data['TAG'] == "B"
ir_mask = data['TAG'] == "I"
red_mask = data['TAG'] == "R"
df_baseline = data[baseline_mask]
df_ir = data[ir_mask]
df_r = data[red_mask]


#filter le data
ir_data = lib.filterir(data)
r_data = lib.filterr(data)

irdc = lib.irdc(data);
rdc = lib.rdc(data);

#calcule sao2

x_ir = ir_data["Value"].to_numpy()
x_ir = np.divide(x_ir, irdc)
x_r = r_data["Value"].to_numpy()
x_r = np.divide(x_r, rdc)

iracrms = lib.vrms(ir_data)
racrms = lib.vrms(r_data)

SaO2 = np.divide(x_r,x_ir)
SaO2 = 110-25*SaO2;
rmsSaO2 = 110-25*racrms/iracrms
trimSaO2 = stats.trim_mean(SaO2, 0.05)



#affichage des resultats
#Nom,set,RDC,IRDC,RACrms,IRACrms,SaO2
selection = input("> Name: ")
selectingb = input("> Set: ")
df = pd.DataFrame({'Nom': selection, 'set': selectingb, 'RDC': rdc, 'IRDC': irdc, 'RACrms': racrms, 'IRACrms': iracrms, 'SaO2': trimSaO2, 'rmsSaO2': rmsSaO2}, index=[0])
print(df.head())

#Prediction SaO2
newPoint = np.array(df[["RDC", "IRDC", "RACrms", "IRACrms"]])
newSaO2 = np.array(df[["SaO2"]])
predict = "SaO2"

xprediction = np.array(newPoint)
yprediction = np.array(newSaO2)

pickle_in = open("student-model.pickle", "rb")
linear = pickle.load(pickle_in)

prediction = linear.predict(xprediction)

df = pd.DataFrame({'Nom': selection, 'set': selectingb, 'RDC': rdc, 'IRDC': irdc, 'RACrms': racrms, 'IRACrms': iracrms, 'SaO2': trimSaO2, 'prediction': prediction[0]}, index=[0])
print(df)
strprint = selection + "," + selectingb + "," + str(rdc) + "," + str(irdc) + "," + str(racrms) + "," + str(iracrms) + "," + str(trimSaO2)
print(strprint)

#affichage des graph
y_data = "Value"
x_data = "Time"

pyplot.figure(1)
pyplot.scatter(df_baseline[x_data], df_baseline[y_data])
pyplot.scatter(df_ir[x_data], df_ir[y_data])
pyplot.scatter(df_r[x_data], df_r[y_data])
pyplot.xlabel(x_data)
pyplot.ylabel(y_data)
pyplot.title('Raw Data')
pyplot.legend(('signal baseline', 'signal r', 'signal ir'), loc='best')
pyplot.grid(True)


fig, axs = pyplot.subplots(3, 1, constrained_layout=True)
axs[0].scatter(df_ir[x_data], df_ir[y_data])
axs[0].scatter(df_r[x_data], df_r[y_data])
#axs[0].plot(t1, f(t1), 'o', t2, f(t2), '-')

axs[0].set_xlabel('time (ms)')
axs[0].set_ylabel('Point (bit)')
axs[0].set_title('Raw Data', ha='center')
axs[0].legend(('noisy signal ir', 'noisy signal r'), loc='best')
axs[0].grid(True)
fig.suptitle('Processed Data', fontsize=16, ha='center')

axs[1].plot(ir_data[x_data], ir_data[y_data])
axs[1].plot(r_data[x_data], r_data[y_data])
axs[1].set_xlabel('time (ms)')
axs[1].set_title('Filtered Data')
axs[1].set_ylabel('Volt (V)')
axs[1].legend(('irac', 'rac'), loc='best')
axs[1].grid(True)

axs[2].plot(df_r[x_data], SaO2)
axs[2].set_xlabel('time (ms)')
axs[2].set_title('SaO2 Results')
axs[2].set_ylabel('percent (%)')
axs[2].grid(True)

pyplot.show()