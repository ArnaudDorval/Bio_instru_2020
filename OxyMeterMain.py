import serial
import serial.tools.list_ports
import time
import csv
import numpy as np
import matplotlib.pyplot as pyplot
from matplotlib import style
import pandas as pd
import filterLib as lib
from scipy import stats
import pickle
import sklearn

print("start")

selection = input("> ")
port = "COM4"
bluetooth = serial.Serial(port, 9600)
print("Connected")

#test de connexion
bluetooth.flushInput()
print("Get Data")
bluetooth.write(b"init")
input_data = bluetooth.readline()
print(input_data)

#commande pour get un data set
selection = input("> Enter Data Name ")
print("Get Data")
bluetooth.write(b"b")
input_data = bluetooth.readline()
print(input_data)

data = "TAG;Value;Time"
dataSet = [data]

timeData = []
tagData = []
valueData = []

counter = 0
#get le data
while data != "END\n":
    input_data = bluetooth.readline()
    data = input_data.decode("utf-8")
    counter = counter + 1
    if data != "END\n":
        if counter > 500:
            d = data.rstrip()
            datasplit = d.split(";")
            if len(tagData) != (4249 - 500):
                tagData.append(datasplit[0])
                valueData.append(datasplit[1])
                timeData.append(datasplit[2])


#sauvegarde to csv
dict = {'TAG': tagData, 'Value': valueData, 'Time': timeData}
df = pd.DataFrame(dict)
print(df.head())
df.to_csv(selection + ".csv")

#ouverture du fichier pour traitement
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



#Nom,set,RDC,IRDC,RACrms,IRACrms,SaO2
selection = input("> Name: ")
selectingb = input("> Set: ")
dict = {'Nom': selection, 'set': selectingb, 'RDC': rdc, 'IRDC': irdc, 'RACrms': racrms, 'IRACrms': iracrms, 'SaO2': trimSaO2, 'rmsSaO2': rmsSaO2}
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

pyplot.figure(2)
pyplot.subplot(3, 1, 1)
style.use("ggplot")
pyplot.scatter(df_ir[x_data], df_ir[y_data])
pyplot.scatter(df_r[x_data], df_r[y_data])
pyplot.legend(('noisy signal ir', 'noisy signal r'), loc='best')
pyplot.xlabel(x_data)
pyplot.ylabel(y_data)
pyplot.title('processed data')
pyplot.grid(True)


pyplot.figure(2)
pyplot.subplot(3, 1, 2)
pyplot.plot(ir_data[x_data], ir_data[y_data])
pyplot.plot(r_data[x_data], r_data[y_data])
pyplot.legend(('irac', 'rac'), loc='best')
pyplot.xlabel(x_data)
pyplot.ylabel(y_data)
pyplot.grid(True)


pyplot.figure(2)
pyplot.subplot(3, 1, 3)
pyplot.plot(df_r[x_data], SaO2)
pyplot.legend(('SaO2'), loc='best')
pyplot.grid(True)
pyplot.show()