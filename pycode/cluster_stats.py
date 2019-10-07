#%% Libraries
import pandas as pd
import numpy as np
np.set_printoptions(suppress=True)

#%% Data load
res = pd.read_csv('campob\csv_correcao\cluster.csv')

#%%
gmm = res[['RHOB','GR','phie','SW','ILD','GMM']]
kme = res[['RHOB','GR','phie','SW','ILD','KMeans']]

#%%
kme_describe=[]
for k in np.unique(kme['KMeans']):
    temp = kme.loc[kme['KMeans'] == k]
    temp = temp[['GR','RHOB','phie','ILD','SW']]
    temp = temp.describe()
    temp['Cluster'] = k
    kme_describe.append(temp)

gmm_describe=[]
for g in np.unique(gmm['GMM']):
    temp = gmm.loc[gmm['GMM'] == k]
    temp = temp[['GR','RHOB','phie','ILD','SW']]
    temp = temp.describe()
    temp['Cluster'] = k
    kme_describe.append(temp)

#%%
