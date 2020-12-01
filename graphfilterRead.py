import filterLib as lib
import matplotlib.pyplot as pyplot
from matplotlib import style
import pandas as pd
import numpy as np
from scipy import stats
import pickle
import sklearn

data = pd.read_csv("testfkndown" + ".csv", sep=",")
data = data[["TAG", "Value", "Time"]]

#get data avec bruit
ir_mask = data['TAG'] == "I"
red_mask = data['TAG'] == "R"
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

SaO2 = np.divide(x_r,x_ir)
SaO2 = 110-25*SaO2;
trimSaO2 = stats.trim_mean(SaO2, 0.1)
iracrms = lib.vrms(ir_data)
racrms = lib.vrms(r_data)


#affichage des resultats
#Nom,set,RDC,IRDC,RACrms,IRACrms,SaO2
selection = input("> Name: ")
selectingb = input("> Set: ")
df = pd.DataFrame({'Nom': selection, 'set': selectingb, 'RDC': rdc, 'IRDC': irdc, 'RACrms': racrms, 'IRACrms': iracrms, 'SaO2': trimSaO2}, index=[0])
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



#affichage des graph
y_data = "Value"
x_data = "Time"

pyplot.figure
pyplot.subplot(3, 1, 1)
style.use("ggplot")
pyplot.scatter(df_ir[x_data], df_ir[y_data])
pyplot.scatter(df_r[x_data], df_r[y_data])
pyplot.legend(('noisy signal ir', 'noisy signal ir'), loc='best')
pyplot.xlabel(x_data)
pyplot.ylabel(y_data)
pyplot.grid(True)


pyplot.figure
pyplot.subplot(3, 1, 2)
pyplot.plot(ir_data[x_data], ir_data[y_data])
pyplot.plot(r_data[x_data], r_data[y_data])
pyplot.legend(('irac', 'rac'), loc='best')
pyplot.xlabel(x_data)
pyplot.ylabel(y_data)
pyplot.grid(True)


pyplot.figure
pyplot.subplot(3, 1, 3)
pyplot.plot(df_r[x_data], SaO2)
pyplot.legend(('SaO2'), loc='best')
pyplot.grid(True)
pyplot.show()

