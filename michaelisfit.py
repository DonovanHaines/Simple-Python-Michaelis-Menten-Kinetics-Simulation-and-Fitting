# Michaelis Menten fit
# A script 
# adapted by Donovan Haines from http://www.physics.utah.edu/~detar/lessons/python/curve_fit/node1.html
#
# This script will generate Michaelis Menten kinetic data including error/stdev and fit
# using SciPy then make some plots
#
#


import numpy as np
from scipy.optimize import curve_fit

###########################################a                                    
def f(s,Vmax,Km):
    """The model function"""
    return Vmax*s/(Km+s)

###########################################a                                    
def main():

    # Model parameters
    Vmax = 100.0
    Km = 3.0
    stdev = 2.0

    # Create the artificial dataset
    nobs = int(50) # number of observations (data points)
    s_max= float(50) # maximum substrate concentration
    s = np.arange(nobs)*s_max/nobs # generate a range of substrate concentrations
                                   # evenly spaced from 0 to x_max
    v = f(s,Vmax,Km) # calculate velocity for each substrate concentration

    vfluct = stdev*np.random.normal(size=nobs) # calculate error/noise to add to each point
    v = v + vfluct # add the error to each point
    sig = np.zeros(nobs) + stdev  # array sig is the stdev for each point
    
    # Fit the curve
    start = (110, 25) #starting guesses for Vmax and Km
    popt, pcov = curve_fit(f,s, v, sigma = sig, p0 = start, absolute_sigma = True) #actually fit it
    print(popt)
    print(pcov)

    # Compute chi square
    v_exp = f(s, *popt)
    r = v - v_exp
    chisq = np.sum((r/stdev)**2)
    df = nobs - 2
    print("chisq =",chisq,"         df =",df)

    # Plot the data as v versus s with error bars along with the fit result
    import matplotlib.pyplot as plt
    plt.errorbar(s, v, yerr=sig, fmt = 'o', label='"data"')
    plt.plot(s, v_exp, label='fit')
    plt.legend()
    plt.axhline(y=0.0, color='0.75', linestyle='-')
    plt.axvline(x=0.0, color='0.75', linestyle='-')
    plt.show()
    
    # Double reciprocal - later need to enhance to add error bars and extend to x-int
    import matplotlib.pyplot as plt
    newsig=sig/v
    plt.plot(1/s, 1/v,'bo',label='"data"')
    plt.plot(1/s, 1/v_exp, label='fit')
    plt.legend()
    plt.axhline(y=0.0, color='0.75', linestyle='-')
    plt.axvline(x=0.0, color='0.75', linestyle='-')
    plt.show()

###########################################a                                    
main()