# -*- coding: utf-8 -*-
"""
@author: Ashutosh Banjara
"""

import pymc3 as pm
import numpy as np
import matplotlib.pyplot as plt
import pymc3.distributions.continuous as cont
from astropy.io import ascii
from TwoMA_flag_code import remove_flags

if __name__ == '__main__':

    """
    Import and process data
    """
    # Raw Data
    data = ascii.read("data/2MA_M31_3600.tbl")

    # Coordinates and magnitudes
    ra = data['ra']
    dec = data['dec']
    h_band = data['h_m']
    j_band = data['j_m']
    k_band = data['k_m']

    # Flags
    rd_flg = list(data['rd_flg'])
    bl_flg = list(data['bl_flg'])
    cc_flg = list(data['cc_flg'])

    # Flag Data
    cleaned_h, cleaned_j, cleaned_k = \
        remove_flags(h_band, j_band, k_band, rd_flg, bl_flg, cc_flg, '0')


    # Isochrone Data
    data_1e9= np.loadtxt("data\Isochrone_data_1e9.dat")
    m_bol = data_1e9[:,27]


    """
    Extinction Model using pymc3
    """

    # Define mu of the normal
    def mu(abs_mag, distance, extinction):
        return abs_mag + 5*np.log(distance/10) + extinction
    
    distances = []
    extinction = []
    
    for i in range(50):
        
        # Define extinction model
        ext_model = pm.Model()
        with ext_model:

            # Priors
            abs_mag = cont.Uniform("absolute magnitude")
            # Upper Bound = diameter of Milky Way
            distance = cont.Uniform("distance", lower=0.1, upper=32408)
            extinction = cont.Uniform("extinction", lower = 0)    
    

            # Likelihood
            app_mag_j = cont.Normal("apparent magnitude j", 
                                    mu = mu(abs_mag, distance, extinction), 
                                    observed=cleaned_j[i])
            app_mag_h = cont.Normal("apparent magnitude h", 
                                    mu = mu(abs_mag, distance, extinction), 
                                    observed=cleaned_h[i])
            app_mag_k = cont.Normal("apparent magnitude k", 
                                    mu = mu(abs_mag, distance, extinction), 
                                    observed=cleaned_k[i])
        
            # Run the MCMC Algorithm
            trace = pm.sample(3000, cores=2, return_inferencedata=False)
            distances.append(trace["distance"].mean())

    plt.scatter(k_band[0:50], distances)


