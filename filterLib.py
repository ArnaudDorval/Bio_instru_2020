import numpy as np
import pandas as pd
from scipy import signal


def filterir(ppandas):
    data = ppandas[["TAG", "Value", "Time"]]

    ir_mask = data['TAG'] == "I"
    baseline_mask = data['TAG'] == "B"

    y_data = "Value"
    x_data = "Time"
    lowpass = 0.08;
    highpass = 0.01;

    df_ir = data[ir_mask]
    df_baseline = data[baseline_mask]


    t = df_ir[x_data].to_numpy()
    xn = df_ir[y_data].to_numpy()

    # convert en voltage
    xn = np.divide((xn * 3.3),(2^16))

    # Low-pass filter section
    bl, al = signal.butter(3, lowpass)
    zi = signal.lfilter_zi(bl, al)
    z, _ = signal.lfilter(bl, al, xn, zi=zi * xn[0])
    z2, _ = signal.lfilter(bl, al, z, zi=zi * z[0])
    yl = signal.filtfilt(bl, al, xn)

    # High=pass filter section
    bh, ah = signal.butter(3, highpass, btype='high', analog=False)
    yh = signal.filtfilt(bh, ah, yl)

    #convert filtered data in pd
    dict = {'TAG': "I", 'Value': yh, 'Time': t}
    df = pd.DataFrame(dict)
    print(df.head())
    return df


def filterr(ppandas):
    data = ppandas[["TAG", "Value", "Time"]]

    r_mask = data['TAG'] == "R"

    y_data = "Value"
    x_data = "Time"
    lowpass = 0.08;
    highpass = 0.01;

    df_r = data[r_mask]

    t = df_r[x_data].to_numpy()
    xn = df_r[y_data].to_numpy()

    #convert en voltage
    xn = np.divide((xn * 3.3),(2^16))

    # Low-pass filter section
    bl, al = signal.butter(3, lowpass)
    zi = signal.lfilter_zi(bl, al)
    z, _ = signal.lfilter(bl, al, xn, zi=zi * xn[0])
    z2, _ = signal.lfilter(bl, al, z, zi=zi * z[0])
    yl = signal.filtfilt(bl, al, xn)

    # High=pass filter section
    bh, ah = signal.butter(3, highpass, btype='high', analog=False)
    yh = signal.filtfilt(bh, ah, yl)

    #convert filtered data in pd
    dict = {'TAG': "R", 'Value': yh, 'Time': t}
    df = pd.DataFrame(dict)
    print(df.head())

    return df


def irdc(ppandas):
    data = ppandas[["TAG", "Value", "Time"]]
    ir_mask = data['TAG'] == "I"
    y_data = "Value"

    df_ir = data[ir_mask]
    xn = df_ir[y_data].to_numpy()

    return np.mean(xn)


def rdc(ppandas):
    data = ppandas[["TAG", "Value", "Time"]]
    r_mask = data['TAG'] == "R"
    y_data = "Value"

    df_r = data[r_mask]
    xn = df_r[y_data].to_numpy()

    return np.mean(xn)


def vrms(ppandas):
    data = ppandas[["TAG", "Value", "Time"]]
    y_data = "Value"
    xn = data[y_data].to_numpy()

    rms = np.sqrt(np.mean(xn ** 2))

    return rms

def trimmean(arr, percent):
    n = len(arr)
    k = int(round(n*(float(percent)/100)/2))
    return np.mean(arr[k+1:n-k])