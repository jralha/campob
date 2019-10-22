#%% Libraries
import pandas as pd
import numpy as np
np.set_printoptions(suppress=True)
pd.set_option('mode.chained_assignment', None)

#%% Data load
res = pd.read_csv('campob\\csv_correcao\\cluster.csv')

#%% Define datasets, reorder clusters in order of Porosity and SW
gmm = res[['RHOB','GR','phie','SW','ILD','GMM']]
kme = res[['RHOB','GR','phie','SW','ILD','KMeans']]

kme_describe=kme.groupby('KMeans').describe()
gmm_describe=gmm.groupby('GMM').describe()

kme_phi = kme_describe[[('phie',  'mean'),('SW','mean')]]
originalOrderK = list(kme_phi.index)
sortedK = kme_phi.sort_values([('phie',  'mean'),('SW','mean')])
newOrderK = list(sortedK.index)
swapK = dict(zip(originalOrderK,newOrderK))

gmm_phi = gmm_describe[[('phie',  'mean'),('SW','mean')]]
originalOrderG = list(gmm_phi.index)
sortedG = gmm_phi.sort_values([('phie',  'mean'),('SW','mean')])
newOrderG = list(sortedG.index)
swapG = dict(zip(originalOrderG,newOrderG))

gmm['GMM'] = gmm['GMM'].map(swapG)
kme['KMeans'] = kme['KMeans'].map(swapK)

res['GMM'] = gmm['GMM']
res['KMeans'] = kme['KMeans']

newNames=[]
oldNames=[]
for i,oldName in enumerate(list(swapG.keys())):
    oldNames.append('cluster '+str(oldName))
    newNames.append('cluster '+str(list(swapG.values())[i]))

swapNames = dict(zip(oldNames,newNames))

res.rename(swapNames)

res.to_csv('campob\\csv_correcao\\cluster_reorder.csv')

#%% Redo cluster stats
kme_describe=kme.groupby('KMeans').describe()
gmm_describe=gmm.groupby('GMM').describe()

kme_describe.to_csv('campob\\csv_correcao\\kme_stats.csv')
gmm_describe.to_csv('campob\\csv_correcao\\gmm_stats.csv')
#%%
