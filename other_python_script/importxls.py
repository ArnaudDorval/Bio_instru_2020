import numpy as np
import matplotlib.pyplot as pyplot
from matplotlib import style
import pandas as pd
from scipy import signal


#selection = input("> Enter Data Name ")
#checker les donnees
data = pd.read_csv("testfkndown" + ".csv", sep=",")
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

t = df_ir[x_data].to_numpy()
x =df_ir[y_data].to_numpy()
baseline = df_baseline[y_data].to_numpy()
bmean = np.mean(baseline)
xn = x
print("moyenne ", bmean)


#Low-pass filter section
bl, al = signal.butter(3, 0.1)
zi = signal.lfilter_zi(bl, al)
z, _ = signal.lfilter(bl, al, xn, zi=zi*xn[0])
z2, _ = signal.lfilter(bl, al, z, zi=zi*z[0])
yl = signal.filtfilt(bl, al, xn)

#High=pass filter section
bh, ah = signal.butter(3, 0.007, btype='high', analog=False)
yh = signal.filtfilt(bh, ah, yl)


pyplot.figure
pyplot.subplot(2, 1, 2)
style.use("ggplot")
#pyplot.scatter(df_baseline[x_data], df_baseline[y_data])
pyplot.scatter(df_ir[x_data], df_ir[y_data])
#pyplot.scatter(df_red[x_data], df_red[y_data])
pyplot.plot(t, yl, 'k')
pyplot.legend(('filtfilt', 'noisy signal'), loc='best')
pyplot.grid(True)
pyplot.xlabel(x_data)
pyplot.ylabel(y_data)

pyplot.subplot(2, 1, 1)
pyplot.plot(t, yh)
pyplot.grid(True)
pyplot.show()

