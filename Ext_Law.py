# -*- coding: utf-8 -*-

"""
@author: Ashutosh Banjara
"""

from astropy.io import ascii
import matplotlib.pyplot as plt
import numpy as np

def extinction_law_ccm(wavelength, Av=1):
    """
    Return the extinction vector, given extinction magnitude (A) and
    wavelength using the Cardelli, Clayton, Mathis extinction law.
    """
    x = 1/wavelength
    Ext = 0.574*(x**(1.61)) - (0.527*(x**(1.61)))/3.1
    return Ext*Av

def extinction_law_indeb(wavelength, Ak=1):
    """
    Return the extinction vector, given extinction magnitude (A) and
    wavelength using the indebetow extinction law.
    """
    log_Ext = 0.61 - 2.22*np.log10(wavelength) + \
        1.21*(np.log10(wavelength)**2)
    return (10**(log_Ext))*Ak

def extinction_law_ccm_ak(wavelength, Ak=1):
    """
    Return the extinction vector, given extinction magnitude (A) and
    wavelength using the Cardelli, Clayton, Mathis extinction law.
    """
    x = 1/wavelength
    Ext = 0.574*(x**(1.61)) - (0.527*(x**(1.61)))/3.1
    return Ext*Ak*(1/extinction_law_ccm(2.164))

if __name__ == "__main__":
    extinction_plot_ccm = extinction_law_ccm_ak(np.arange(1.1, 2.3, 0.01))
    plt.plot(np.arange(1.1, 2.3, 0.01), extinction_plot_ccm, label = 'CCM')
    extinction_plot_indeb = extinction_law_indeb(np.arange(1.1, 2.3, 0.01))
    plt.plot(np.arange(1.1, 2.3, 0.01), extinction_plot_indeb, label = 'Indebetow')
    plt.title('Extinction Laws')
    plt.xlabel('wavelength(um)')
    plt.ylabel('Ax/Ak')
    plt.legend()