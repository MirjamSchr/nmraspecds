# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 11:15:58 2022

@author: biede
"""

import nmrglue as ng
import nmrglue.fileio.bruker as bruker

import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from scipy.optimize import minimize, curve_fit

import numpy as np
"""

Various functions for NMR processing

"""
def phaser(data):
    matplotlib.use('Qt5Agg')
    p00,p11 = ng.proc_autophase.manual_ps(data,notebook=False)
    plt.close()
    return p00, p11

def lbcalc(lb,dic): # speziell für NMRGlue 
    ndim = dic['ndim']-1
    sw = dic[ndim]['sw']
    lbc = lb/sw
    return lbc

def chemcalc(dic,td): # Frequenzachse
    ndim = dic['ndim']-1
    sw = dic[ndim]['sw']
    sf1 = dic[ndim]['obs']
    car = dic[ndim]['car']
    freq = np.linspace(-sw/(2*(sf1+car)),sw/(2*(sf1+car)),td)
    return freq

def aqcalc(dic): # Acquisition time
    ndim = dic['ndim']-1
    sw = dic[ndim]['sw']
    td = dic[ndim]['size']
    aq = td/sw
    return aq

def vdlist(exppath):
    vdfile = [f for f in listdir(exppath) if isfile(join(exppath, f)) and f == "vdlist"]
    vdlist = pd.read_table(join(exppath, vdfile[0]), delimiter=" ", header=None).squeeze("columns").to_numpy()
    
    if isinstance(vdlist, np.ndarray):
        vd = np.ones(np.shape(vdlist), dtype=np.float64)
        counter = 0
        for v in vdlist:
            #print(v)
            #print(counter)
            if v.endswith('m'):
                n = float(np.char.replace(v,'m','e-3'))
            elif v.endswith('u'):
                n = float(np.char.replace(v,'u','e-6'))
            vd[counter] = n
            counter += 1
    return vd

"""
Module for calculating the actual sample temperature by using the spin-lattice relaxation of polycrystalline KBr powder 
(mostly separated by the sample of interest with a spacer)

"""
from sympy import symbols, nonlinsolve

def T1_KBr(T1):
    T = symbols('T')
    eq = [0.00145 + 5330.0*T**(-2) + (1.42e7)*T**(-4) + (2.48e9)*T**(-6) - T1]
    sol = nonlinsolve(eq, T)
    return sol

"""
Module for fitting all kind of functions related to NMR
"""
def NMRFit(xdata,ydata,keyword):
    # Function to fit
    def SatRec(x,M0,R):
        return M0*(1-np.exp(-R*x))
    
    def StretchExp(x,M0,R,beta):
        return M0*np.exp((-(R*x)**beta))
    
    # Optimization of initial parameters
    def optimize_init_params(x, y, func):
        # define the error function
        def error_func(params):
            # compute the predicted values using the function and the given parameters
            y_pred = func(x, *params)
              
            # compute the mean squared error between the predicted and observed values
            mse = np.mean((y - y_pred)**2)
          
            return mse
        
        # # initialize the initial parameters with random values
        # init_params = np.random.random(size=func.__code__.co_argcount - 1)
        
        # #initialize the initial parameters with boundaries of the data
        size=func.__code__.co_argcount -1
        if size == 2:
            M0 = max(y)
            R = 100
            init_params=np.array([M0, R])
        elif size == 3:
            M0 = max(y)
            R = 100
            b = 1
            init_params=np.array([M0,R,b])
            
        
        
        # perform global optimization to find the optimal initial parameters
        result = minimize(error_func, init_params, method='L-BFGS-B')
       # return init_params
        return result.x
    
    init_params = optimize_init_params(xdata,ydata,locals()[keyword])
    popt,pcov = curve_fit(locals()[keyword],xdata, ydata, p0=init_params)
    
    perr = np.sqrt(np.diag(pcov))
    
    # Fit statistics / calculating RMSE and Rsquared values of the fit
    modelPredictions = locals()[keyword](xdata,*popt)
    absError = modelPredictions - ydata # absolute error of the fit
    SE = np.square(absError) # squared absolute error
    MSE = np.mean(SE) # mean squared error
    RMSE = np.sqrt(MSE) # root mean squared error
    
    Rsquared = 1.0 - (np.var(absError) / np.var(ydata))
    Rsquared_adj = 1.0 - np.divide(np.multiply(1.0-Rsquared,len(ydata-1)),(len(ydata)+(locals()[keyword].__code__.co_argcount - 1)-1))
    print(Rsquared_adj)
    return popt,pcov,perr,Rsquared_adj, modelPredictions
    
    # if keyword == "SatRec":
    #     init_params = optimize_init_params(xdata,ydata,SatRec)
    #     p,c = curve_fit(SatRec,xdata, ydata, p0=init_params)
    # elif keyword == "StretchExp":
    #     init_params = optimize_init_params(xdata,ydata,StrecthExp)
    #     p,c = curve_fit(StretchExp,xdata, ydata, p0=init_params)
    # return p,c
"""

Module to pick coordinates from plot.
Function xcord picks x coordinates, function ycord retrieves y coordinates.

"""
# xcord function to retrieve x coordiantes from the xy input
def xcord(x,y,npeaks,xlim1,xlim2):
    matplotlib.use('Qt5Agg')
    x_ppm=[]
    x_index=[]
    
    plt.plot(x,y)
    plt.xlim(xlim1,xlim2)
    cords = plt.ginput(npeaks)
    plt.close()
    # print(cords)
    
    for i in range(len(cords)):
        diff = abs(x-cords[i][0])
        # print(diff.min())
        # print(np.where(diff == diff.min()))
        # print(x[np.where(diff == diff.min())])
        c = np.where(diff == diff.min())
        # print(c[0])
        # print(x[c[0]])
        x_ppm.append(x[c[0]])
        x_index.append(c[0])
    return x_ppm, x_index

"""

Module for writing files to disk

"""
### Work in progress, but quick and dirty 
def header(nuclei = ' ', aq= ' ', td=' ', SF1=' ', SW=' ', car=' ', ls_pt=' ', p0=' ', p1=' ', lb=' '):
    header = ''
    nuclei = header + 'Nuclei: ' + nuclei + '\n'
    header = header + '#aq: ' + aq + '\n'
    header = header + '#td: ' + td + '\n'
    header = header + '#SF1: ' +SF1 + '\n'
    header = header + '#SW: '+SW + '\n'
    header = header + '#Points used for left shifting the FID: ' + ls_pt + '\n'
    header = header + '#Zeroth order phase correction: ' + p0 + '\n'
    header = header + '#First order phase correction: ' + p1 + '\n'
    header = header + '#Line broadening for apodization: ' + lb + '\n'
    
    return header

