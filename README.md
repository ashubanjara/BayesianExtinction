# Code for my AST425 Research Project on mapping extinction in the Milky Way using Bayesian statistics

Uses Markov Chain Monte Carlo (MCMC) and No-U-Turn Sampler (NUTS) to solve for the Stellar-Type, Extinction and Distance towards a star.

Required Python Modules: Numpy, Arviz, Theano, Pymc3, Astropy

How to Run Model:
1. Get the prerequisite python modules (can be done easily through anaconda)
2. Run final_model.py (feel free to change model parameters)
3. The Posteriors will be displayed in console
4. These files/folders should be in the same directory: Ext_Law.py, TwoMA_flag_code.py, Isochrone_code.py, data folder

![Image of Model Diagram](https://github.com/ashubanjara/BayesianExtinction/blob/main/Model_Diagram_2.PNG)

The Bayesian Model representation can be seen in the image above. The methodologies and details behind this
project can be found in my reseach paper: (https://drive.google.com/file/d/10CjTqYPaH3erd1YfR3MEDGbLUEmwtPCx/view?usp=sharing)
