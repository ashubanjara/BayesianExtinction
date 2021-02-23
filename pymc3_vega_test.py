# -*- coding: utf-8 -*-
"""
@author: Ashutosh Banjara
"""

import pymc3 as pm
import numpy as np
import matplotlib.pyplot as plt
import pymc3.distributions.continuous as cont


"""
Extinction Model test on Vega using pymc3
"""

# Define mu of the normal
def mu(abs_mag, distance, extinction):
    return abs_mag + 5*np.log(distance/10) + extinction

Vega_data = [-0.177, -0.029, 0.129] # Vega j-h-k magnitudes from 2MASS.

if __name__ == '__main__':
    
    # Define extinction model
    ext_model = pm.Model()
    
    # Model parameters
    with ext_model:

        # Priors
        abs_mag = cont.Uniform("absolute magnitude")
        distance = cont.Uniform("distance", lower=0.1, upper=32408)
        extinction = cont.Uniform("extinction", lower = 0)    
    

        # Likelihood (how to combine j, h and k?)
        app_mag_j = cont.Normal("apparent magnitude j", 
                              mu = mu(abs_mag, distance, extinction), 
                              observed=Vega_data[0])
        app_mag_h = cont.Normal("apparent magnitude h", 
                              mu = mu(abs_mag, distance, extinction), 
                              observed=Vega_data[1])
        app_mag_k = cont.Normal("apparent magnitude k", 
                              mu = mu(abs_mag, distance, extinction), 
                              observed=Vega_data[2])
        
        # Run the MCMC Algorithm
        trace = pm.sample(3000, cores=2)
        pm.traceplot(trace)
        pm.plot_posterior(trace, var_names = ["distance"])
    
    print("Mean distance to Vega = " + 
          str(np.round(trace["distance"].mean(), 3)) + " pc")
    print("Actual distance to Vega = 7.665 pc")
        
    