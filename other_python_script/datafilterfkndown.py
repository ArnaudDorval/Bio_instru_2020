import numpy as np
import matplotlib.pyplot as pyplot
from matplotlib import style
import pandas as pd
from scipy import signal

import csv
data = pd.read_csv("testfkndown" + ".csv", sep=",")
print(data.head())

data = data[["Value", "Time"]]
print(data.head())

index = len(data.index)

test = data.iloc[ 0:20 , : ]
print(test.head())

#baseline_mask = index[4:20:4]
#ir_mask = index[1:20:4]
#red_mask = index[3:20:4]

#df_baseline = data[baseline_mask]
#df_ir = data[ir_mask]
#df_red = data[red_mask]

#print(df_baseline.head())
#print(df_ir.head())
#print(df_red.head())