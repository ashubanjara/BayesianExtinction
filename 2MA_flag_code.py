# -*- coding: utf-8 -*-

"""
@author: Ashutosh Banjara
"""

from astropy.io import ascii
import matplotlib.pyplot as plt
import numpy as np
from Ext_Law import extinction_law_indeb, extinction_law_ccm_ak

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

def remove_flags(h, j, k, read_flags, blend_flags, cont_flags, string_element):
    """
    Removes any string with string_element (str) present in flag_data 
    (list(str)).
    """
    cleaned_h = []
    cleaned_j = []
    cleaned_k = []
    for i in range(len(read_flags)):
        found_element = False
        for l in read_flags[i]:
            if l == string_element:
                found_element = True
        for m in blend_flags[i]:
            if m == string_element:
                found_element = True
        for n in cont_flags[i]:
            if n == string_element:
                found_element = True

        if found_element == False:
            cleaned_h.append(h[i])
            cleaned_j.append(j[i])
            cleaned_k.append(k[i])
    return np.array(cleaned_h), np.array(cleaned_j), np.array(cleaned_k)


cleaned_h, cleaned_j, cleaned_k = \
remove_flags(h_band, j_band, k_band, rd_flg, bl_flg, cc_flg, '0')

# Color-excess
j_k = cleaned_j - cleaned_k
j_h = cleaned_j - cleaned_h

plt.scatter(j_k, j_h, marker = ".")
plt.title('Color Excess with Extinction Vector (Indebetow)')
plt.xlabel('j - k')
plt.ylabel('j - h')

m = extinction_law_indeb(1.25) - 1

plt.arrow(0, 0.5, 1/2, m/2, head_width = 0.05, head_length = 0.1, 
          label='Extinction Vector')

vector_length = np.sqrt(0.5**2 + (m/2)**2)

plt.figure()

plt.scatter(j_k, j_h, marker = ".")
plt.title('Color Excess with Extinction Vector (CCM)')
plt.xlabel('j - k')
plt.ylabel('j - h')
m = extinction_law_ccm_ak(1.25) - 1

plt.arrow(0, 0.5, 1/2, m/2, head_width = 0.05, head_length = 0.1, 
          label='Extinction Vector')

plt.figure()
plt.scatter(j_k, cleaned_k, marker = ".")
plt.title('Color Magnitude')
plt.xlabel('j - k')
plt.ylabel('k')
plt.ylim(max(k_band), min(k_band))
