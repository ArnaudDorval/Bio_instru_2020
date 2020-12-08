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

tr = df_red[x_data].to_numpy()
xr =df_red[y_data].to_numpy()

lowvar = 0.07
highvar = 0.004

#Low-pass filter section
bl, al = signal.butter(3, lowvar)
zi = signal.lfilter_zi(bl, al)
z, _ = signal.lfilter(bl, al, xn, zi=zi*xn[0])
z2, _ = signal.lfilter(bl, al, z, zi=zi*z[0])
yl = signal.filtfilt(bl, al, xn)

#High=pass filter section
bh, ah = signal.butter(3, highvar, btype='high', analog=False)
yh = signal.filtfilt(bh, ah, yl)

#Low-pass filter section
blr, alr = signal.butter(3, lowvar) #vers le haut cest moins intense
zi = signal.lfilter_zi(blr, alr)
z, _ = signal.lfilter(blr, alr, xr, zi=zi*xn[0])
z2, _ = signal.lfilter(blr, alr, z, zi=zi*z[0])
ylr = signal.filtfilt(blr, alr, xr)

#High=pass filter section
bhr, ahr = signal.butter(3, highvar, btype='high', analog=False)
yhr = signal.filtfilt(bhr, ahr, ylr)



######################################################################################################
fig, axs = pyplot.subplots(2, 1, constrained_layout=True)
axs[0].scatter(df_ir[x_data], df_ir[y_data])
axs[0].plot(t, yl, 'k')
axs[0].set_xlabel('time (ms)')
axs[0].set_ylabel('Point (bit)')
axs[0].set_title('Low Pass Filter & Interpolation', ha='center')
axs[0].legend(('filtered', 'raw signal'), loc='best')
axs[0].grid(True)
fig.suptitle('Data Filtering IR Signal', fontsize=16, ha='center')

axs[1].plot(t, yh)
axs[1].set_xlabel('time (ms)')
axs[1].set_title('High Pass Filter')
axs[1].set_ylabel('Point (bit)')
axs[1].grid(True)


######################################################################################################
fig, axs = pyplot.subplots(2, 1, constrained_layout=True)
axs[0].scatter(df_red[x_data], df_red[y_data], color='red')
axs[0].plot(tr, ylr, 'k')
axs[0].set_xlabel('time (ms)')
axs[0].set_ylabel('Point (bit)')
axs[0].set_title('Low Pass Filter & Interpolation', ha='center')
axs[0].legend(('filtered', 'raw signal'), loc='best')
axs[0].grid(True)
fig.suptitle('Data Filtering RED Signal', fontsize=16, ha='center')

axs[1].plot(tr, yhr, color='red')
axs[1].set_xlabel('time (ms)')
axs[1].set_title('High Pass Filter')
axs[1].set_ylabel('Point (bit)')
axs[1].grid(True)


pyplot.show()