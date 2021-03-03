# -*- coding: utf-8 -*-
"""
@author: Ashutosh Banjara
"""

import pymc3 as pm
import numpy as np
import matplotlib.pyplot as plt
import pymc3.distributions.continuous as cont
import pymc3.distributions.discrete as disc
from Ext_Law import extinction_law_ccm_ak


"""
Extinction Model test on Vega using pymc3
"""

isochrone_data_1e9 = np.loadtxt("data\Isochrone_data_1e9.dat")
Vega_data = [-0.177, -0.029, 0.129] # Vega j-h-k magnitudes from 2MASS.

# Find Specific Columns
Mj = isochrone_data_1e9[:,28]
Mh = isochrone_data_1e9[:,29]
Mk = isochrone_data_1e9[:,30]
temps = isochrone_data_1e9[:,7]
Z = isochrone_data_1e9[:,25]
Mass = isochrone_data_1e9[:,5]

# Define mu of the normal
"""
def mu(abs_mag, distance, extinction):
    return abs_mag + 5*np.log(distance/10) + extinction
"""

def mu_j(st_index, distance, extinction):
    return stellar_type + 5*np.log(distance/10) + extinction

def mu_h(st_index, distance, extinction):
    return stellar_type + 5*np.log(distance/10) + extinction

def mu_k(st_index, distance, extinction):
    return Mk[st_index] + 5*np.log(distance/10) + extinction


# Define stellar type function
def stellar_type(abs_mag, band):
    """
    Returns stellar type given an abs_mag ()
    """
    if band == 'j':
        index_1 = np.where(Mj>=(abs_mag - 0.5))
        index_2 = np.where(Mj < (abs_mag + 0.5))
        indices = np.intersect1d(index_1, index_2)
        
    elif band == 'h':
        index_1 = np.where(Mh>=(abs_mag - 0.5))
        index_2 = np.where(Mh < (abs_mag + 0.5))
        indices = np.intersect1d(index_1, index_2)
        
    if band == 'k':
        index_1 = np.where(Mk>=(abs_mag - 0.5))
        index_2 = np.where(Mk < (abs_mag + 0.5))
        indices = np.intersect1d(index_1, index_2)
    
    stellar_type_arr = np.array([10**(temps[indices[0]]), Z[indices[0]], 
                                 Mass[indices[0]]])
                                 
    return stellar_type_arr

def mj_func(i):
    return Mj[i]

def mh_func(i):
    return Mh[i]

def mk_func(i):
    return Mk[i]

# Print values to test function
ST_k = stellar_type(-8, 'k')
print("Temperature = " + str(ST_k[0]))
print("Metallicity = " + str(ST_k[1]))
print("Age = " + str(ST_k[2]))


if __name__ == '__main__':
    
    # Define extinction model
    ext_model = pm.Model()
    
    # Model parameters
    with ext_model:

        # Priors
        # abs_mag = cont.Uniform("absolute magnitude", lower=-10, upper=10)
        distance = cont.Uniform("distance", lower=0.1, upper=32408)
        extinction = cont.Uniform("extinction", lower = 0, upper=10) 
        stellar_type_index = disc.DiscreteUniform("st_index", lower = 0, 
                                          upper = len(Mk) - 1)
    

        # Likelihood (how to combine j, h and k?)
        """
        app_mag_j = cont.Normal("apparent magnitude j", 
                              mu = mu(mj_func(stellar_type_index), distance, extinction
                                      *(1/extinction_law_ccm_ak(1.235))), 
                              observed=Vega_data[0])
        app_mag_h = cont.Normal("apparent magnitude h", 
                              mu = mu(mh_func(stellar_type_index), distance, extinction
                                      *(1/extinction_law_ccm_ak(1.662))), 
                              observed=Vega_data[1])
        app_mag_k = cont.Normal("apparent magnitude k", 
                              mu = mu(mk_func(stellar_type_index), distance, extinction), 
                              observed=Vega_data[2])
        """
        
        # Using sequential monte carlo, function to be used and its parameters
        sim_k = pm.Simulator("sim", mu_k, 
                           params = (stellar_type_index, distance, extinction),
                           observed = np.array(Vega_data[0]))
        
        # Run the MCMC Algorithm
        """
        trace = pm.sample(3000, cores=2)
        pm.traceplot(trace)
        pm.plot_posterior(trace, var_names = ["distance"])
        """
        
        trace_lv = pm.sample_smc(kernel="ABC", parallel=True)
        
    """
    print("Mean distance to Vega = " + 
          str(np.round(trace["distance"].mean(), 3)) + " pc")
    print("Actual distance to Vega = 7.665 pc")
    """
    