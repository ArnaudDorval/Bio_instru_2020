import serial
import serial.tools.list_ports
import time
import csv
import numpy as np
import matplotlib.pyplot as pyplot
from matplotlib import style
import pandas as pd


#selection = input("> Enter Data Name ")
#checker les donnees
data = pd.read_csv("testb" + ".csv", sep=",")
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