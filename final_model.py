# -*- coding: utf-8 -*-
"""
@author: Ashutosh Banjara

Run this file to run the model on a given set of 2MASS
stars with J, H and K magnitudes. It outputs the estimated
distance and the extinction towards that star, also the
likely stellar type.

Required Python Modules: Numpy, Arviz, Theano, Pymc3, Astropy

Required Project Files (should be in the same directory):
Ext_Law.py, TwoMA_flag_code.py, Isochrone_code.py 
"""

import pymc3 as pm
import numpy as np
import pymc3.distributions.continuous as cont
import pymc3.distributions.discrete as disc
from Ext_Law import extinction_law_ccm_ak
from TwoMA_flag_code import remove_flags
from astropy.io import ascii
import arviz as az
import theano


"""
Extinction Model test on Vega using pymc3
"""

isochrone_data = np.loadtxt("data\Isochrone_data_full.dat")
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

sorted_indices = np.lexsort((isochrone_data[:,30][::-1], isochrone_data[:,7][::-1]))

isochrone_data = isochrone_data[sorted_indices]

# Find Specific Columns
Mj = isochrone_data[:,28]
Mh = isochrone_data[:,29]
Mk = isochrone_data[:,30]
temps = isochrone_data[:,7]
Z = isochrone_data[:,25]
Mass = isochrone_data[:,5]

Mj = np.concatenate((Mk, np.zeros(len(Mk/2))))
Mh = np.concatenate((Mk, np.zeros(len(Mk/2))))
Mk = np.concatenate((Mk, np.zeros(len(Mk/2))))

Mj_index = theano.shared(Mj)
Mh_index = theano.shared(Mh)
Mk_index = theano.shared(Mk)

# Define mu of the normal
def mu_j(st_index, distance, extinction):
    return Mj_index[st_index] + 5*np.log(distance/10) + extinction

def mu_h(st_index, distance, extinction):
    return Mh_index[st_index] + 5*np.log(distance/10) + extinction

def mu_k(st_index, distance, extinction):
    return Mk_index[st_index] + 5*np.log(distance/10) + extinction

# Define stellar type function
def stellar_type(abs_mag):
    """
    Returns stellar type given an abs_mag ()
    """
    index_1 = np.where(Mj>=(abs_mag - 0.5))
    index_2 = np.where(Mj < (abs_mag + 0.5))
    indices = np.intersect1d(index_1, index_2)
    
    stellar_type_arr = np.array([10**(temps[indices[0]]), Z[indices[0]], 
                                 Mass[indices[0]]])
                                 
    return stellar_type_arr
    

if __name__ == '__main__':
    
    distances = []
    extinctions = []
    st_indices = []
    
    for i in range(1):
        # Define extinction model
        ext_model = pm.Model()
        
        # Model parameters
        with ext_model:
            
    
            # Priors
            #abs_mag = cont.Uniform("absolute magnitude", lower=-10, upper=10)
            distance = cont.Uniform("distance", lower=0.1, upper=32408)
            extinction = cont.Uniform("extinction", lower = 0, upper=10) 
            stellar_type_index = disc.DiscreteUniform("st_index", lower = 0, 
                                              upper = (len(Mk)/2 - 1)) 
        
    
            # Likelihood (how to combine j, h and k?)
    
            app_mag_j = cont.Normal("apparent magnitude j", 
                                  mu = mu_j(stellar_type_index, distance, extinction
                                          *(1/extinction_law_ccm_ak(1.235))), 
                                  observed=cleaned_j[i])
            app_mag_h = cont.Normal("apparent magnitude h", 
                                  mu = mu_h(stellar_type_index, distance, extinction
                                          *(1/extinction_law_ccm_ak(1.662))), 
                                  observed=cleaned_h[i])
            app_mag_k = cont.Normal("apparent magnitude k", 
                                    mu = mu_k(stellar_type_index, distance, extinction), 
                                    observed=cleaned_k[i])
    
            
            # Using sequential monte carlo, function to be used and its parameters
            # Run the MCMC Algorithm
    
            trace = pm.sample(3000, cores=4)
            az.plot_trace(trace)
            az.plot_posterior(trace, var_names = ["distance"])
            az.plot_pair(trace, var_names = ['distance', 'extinction', 'st_index'],
                kind='kde',
                textsize=18)
            distances.append(trace["distance"])
            az.plot_posterior(trace, var_names = ["extinction"])
            extinctions.append(trace["extinction"])
            st_indices.append(trace["st_index"])
            
        st_pred_index = np.bincount(trace["st_index"]).argmax()
    
        print("Mean distance to Star = " + 
              str(np.round(trace["distance"].mean(), 3)) + " pc")
        
        # Determine the stellar type from most common prediction for st
        stellar_type_array = stellar_type(Mk[st_pred_index])
        
        print("Stellar Type: [temp = " + 
              str(np.round(stellar_type_array[0], 3)) + 
              ", Z = " + str(np.round(stellar_type_array[1], 3)) + ", Mass = " +
              str(np.round(stellar_type_array[2], 3)) + "]")