# -*- coding: utf-8 -*-

"""
@author: Ashutosh Banjara
"""

from astropy.io import ascii
import matplotlib.pyplot as plt
import numpy as np

data = ascii.read("data/2MA_M31_3600.tbl")

# Coordinates and magnitudes
ra = data['ra']
dec = data['dec']
h_band = data['h_m']
j_band = data['j_m']
k_band = data['k_m']

# Flags
rd_flg = data['rd_flg']
bl_flg = data['bl_flg']
cc_flg = data['cc_flg']

# Color-excess
j_k = j_band - k_band
j_h = j_band - h_band

# Plot of stellar positions in the sky
plt.scatter(ra, dec, marker = '.')
plt.title('Stellar Positions')
plt.xlabel('ra')
plt.ylabel('dec')

# Color-Color
plt.figure()
plt.scatter(j_k, j_h, marker = ".")
plt.title('Color-Color Diagram of Stars Surrounding M31')
plt.xlabel('(j - k)')
plt.ylabel('(j - h)')
plt.plot(np.arange(-3, 5), np.arange(-3, 5))

# Color-Magnitude
plt.figure()
plt.scatter(j_k, k_band, marker = ".")
plt.ylim(max(k_band), min(k_band))
plt.title('Color-Magnitude Diagram of Stars Surrounding M31')
plt.xlabel('color excess (j - k)')
plt.ylabel('k magnitude')


# Filter the data by values
indexes = np.where((j_k > 0.8) & (j_k < 1.2))
rd_flags = list(rd_flg[indexes])
bl_flags = list(bl_flg[indexes])
cc_flags = list(cc_flg[indexes])

print(rd_flags)
print(bl_flags)
print(cc_flags)
                

