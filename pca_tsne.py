#%% Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import dbscan
from MulticoreTSNE import MulticoreTSNE as TSNE
from sklearn.decomposition import PCA
from mapping import plot_map
import seaborn as sns
np.set_printoptions(suppress=True)
plt.style.use('ggplot')

#%% Load Data                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   #%% Data load
res = pd.read_csv('props_new\\cluster_reorder.csv')

#%%Defining good constants to plot.
med_i = np.median(res['celli'])
med_j = np.median(res['cellj'])
med_k = np.median(res['cellk'])

res['cluster 1 ou 2'] = 1-res['cluster 0']



#%%TSNE and PCA
pca = TSNE(n_components=2,verbose=1,n_jobs=-1,).fit_transform(res[['dt','gr','phie','rhob']])
# pca = PCA(n_components=2).fit_transform(res[['dt','gr','phie','rhob']])


# %%

indices = np.random.choice(pca.shape[0], 400000, replace=False)


sns.kdeplot(pca[indices].T[0],pca[indices].T[1], shade=True, shade_lowest=False,cmap='Reds')
# plt.scatter(pca[indices].T[0],pca[indices].T[1],s=1,alpha=0.2,color='black')
# %%
