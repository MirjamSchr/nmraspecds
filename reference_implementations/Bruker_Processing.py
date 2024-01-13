# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 13:50:35 2023

@author: biede
"""
import os
import nmrutils as nu

import nmrglue as ng
import nmrglue.fileio.bruker as bruker

import matplotlib
import matplotlib.pyplot as plt

import numpy as np
from scipy.fft import fft, ifft, fftshift
from scipy.integrate import simpson, trapezoid, cumulative_trapezoid

path = r"N:\EtOH_d3\20230119_EtOH_D3_KBr_in_1p3mm_with_10mM_AMUPol_100K"
expno = "13"
exppath = os.path.join(path, expno)


# import FID from Bruker file system by using NMRglue
dic, data = bruker.read(exppath, cplex=True)
udic = bruker.guess_udic(dic, data)
print(udic)
data = bruker.remove_digital_filter(dic, data)
time = np.linspace(0, nu.aqcalc(udic), len(data[0, :]))

# plot all imported fids
for i in range(len(data)):
    plt.plot(time, data.real[i, :])
    plt.plot(time, data.imag[i, :])
plt.show()
plt.close()

freq = nu.chemcalc(udic, 8192)
point = 1.0
data_copy = data
lb = float(input("Enter the line broadening for apodization of the FID. "))
while point != 0.0:
    ### process the fid:
    # Leftshift
    data = data_copy
    data = ng.proc_base.ls(data, pts=point)
    # Zerofill
    data = ng.proc_base.zf_size(data, 8192)
    # Apodization
    data = ng.proc_base.em(data, lb=nu.lbcalc(lb, udic))
    # FFT
    data = ng.proc_base.fft(data)
    plt.plot(freq, data.real[0, :])
    plt.show()
    # Final point value for report
    pt = point
    point = float(
        input("Enter the points for leftshift (as float). If good, enter 0")
    )

del data_copy
plt.close()

# Phase the processed spectra
p0start = float(input("Enter starting PHC0 value."))
data = ng.proc_base.ps(data, p0=p0start)
p00, p11 = nu.phaser(data[0, :])
data = ng.proc_base.ps(data, p0=p00, p1=p11)
# Final p0 and p1 value for report
final_p00 = p0start + p00


### Output for saving; NMRglue has a Bruke writing function, which Topspin doesn't recognize as Bruker files
data_T = data.transpose()
# doing it manually because i don't understand the other stuff
out = np.zeros(shape=(len(data[0, :]), 17))
for i in range(17):
    if i == 0:
        out[:, i] = freq
    else:
        out[:, i] = data_T[:, i - 1]

ndim = udic["ndim"] - 1
np.savetxt(
    path + "T1X.dat",
    out,
    header=nu.header(
        "2H",
        str(nu.aqcalc(udic)),
        str(len(data[0, :])),
        str(udic[ndim]["obs"]),
        str(udic[ndim]["sw"]),
        str(udic[ndim]["car"]),
        str(pt),
        str(final_p00),
        str(p11),
        str(lb),
    ),
)
