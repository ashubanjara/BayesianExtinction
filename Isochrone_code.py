# -*- coding: utf-8 -*-
"""
@author: Ashutosh Banjara
"""

import matplotlib.pyplot as plt
import numpy as np
from Ext_Law import extinction_law_indeb, extinction_law_ccm_ak

data_1e8 = np.loadtxt("data\Isochrone_data_1e8.dat")
data_1e9 = np.loadtxt("data\Isochrone_data_1e9.dat")
data_1e10 = np.loadtxt("data\Isochrone_data_1e10.dat")

"""
Isochrone data using 2Mass + spitzer + WISE, 0 circumstellar dust, All
the ages/metalliticies available. Data gathered from: 
http://stev.oapd.inaf.it/cgi-bin/cmd_3.4
"""

m_bol_1 = data_1e8[:,27]
j_band_1 = data_1e8[:,28]
h_band_1 = data_1e8[:,29]
k_band_1 = data_1e8[:,30]
j_h_1 = j_band_1 - h_band_1

m_bol_2 = data_1e9[:,27]
j_band_2 = data_1e9[:,28]
h_band_2 = data_1e9[:,29]
k_band_2 = data_1e9[:,30]
j_h_2 = j_band_2 - h_band_2

plt.plot(j_h_1, k_band_1, label = 'age = 1e8')
plt.ylim(max(k_band_1), min(k_band_1))
plt.plot(j_h_2, k_band_2, label = 'age = 1e9')
plt.xlabel('Color Excess (J-H)')
plt.ylabel('K band Magnitude (Mk)')
plt.title('Isochrones of Different Length')
plt.legend()

plt.figure()
plt.plot(j_h_1, k_band_1, label = 'age = 1e8')
plt.ylim(max(k_band_1), min(k_band_1))
plt.xlabel('Color Excess (J-H)')
plt.ylabel('K band Magnitude (Mk)')
plt.title('Effect of Extinction on Isochrone')
plt.legend()

m = 1/(extinction_law_indeb(1.235) - extinction_law_indeb(1.662))
plt.annotate("", xy=(m/4 - 0.07, 1/4 - 0.5), xytext=(-0.07, -0.5), 
            arrowprops=dict(arrowstyle="->"))