import serial
import serial.tools.list_ports
import time
import csv
import numpy as np
import matplotlib.pyplot as pyplot
from matplotlib import style
import pandas as pd

print("start")

selection = input("> ")
port = "COM4"

bluetooth = serial.Serial(port, 9600)

print("Connected")

bluetooth.flushInput()

print("Get Data")
bluetooth.write(b"init")
input_data = bluetooth.readline()
print(input_data)

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

while data != "END\n":
    input_data = bluetooth.readline()
    data = input_data.decode("utf-8")
    #print(data.rstrip())
    if data != "END\n":
        d = data.rstrip()
        datasplit = d.split(";")
        if len(tagData) != 4249:
            tagData.append(datasplit[0])
            valueData.append(datasplit[1])
            timeData.append(datasplit[2])


dict = {'TAG': tagData, 'Value': valueData, 'Time': timeData}
df = pd.DataFrame(dict)
print(df.head())
#print(df)

df.to_csv(selection + ".csv")

data = pd.read_csv(selection + ".csv", sep=",")
data = data[["TAG", "Value", "Time"]]

baseline_mask = data['TAG'] == "B"
ir_mask = data['TAG'] == "I"
red_mask = data['TAG'] == "R"

df_baseline = data[baseline_mask]
df_ir = data[ir_mask]
df_red = data[red_mask]

print(df_baseline.head())
print(df_ir.head())
print(df_red.head())

y_data = "Value"
x_data = "Time"

style.use("ggplot")
pyplot.scatter(df_baseline[x_data], df_baseline[y_data])
pyplot.scatter(df_ir[x_data], df_ir[y_data])
pyplot.scatter(df_red[x_data], df_red[y_data])
pyplot.xlabel(x_data)
pyplot.ylabel(y_data)
pyplot.show()