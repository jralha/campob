#%% Libraries
import pandas as pd
import numpy as np
np.set_printoptions(suppress=True)

#%% Data load
res = pd.read_csv('csv_correcao\\cluster.csv')

#%%
gmm = res[['RHOB','GR','phie','SW','ILD','GMM']]
kme = res[['RHOB','GR','phie','SW','ILD','KMeans']]

#%%
kme_describe=kme.groupby('KMeans').describe().T
gmm_describe=gmm.groupby('GMM').describe().T

#%% Reorder clusters in order of Porosity


#%%
