#%% Libraries

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import seaborn as sns
import numpy as np
import os
from tqdm.auto import tqdm
from sklearn.mixture import GaussianMixture
from sklearn.metrics import davies_bouldin_score, silhouette_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
np.set_printoptions(suppress=True)
plt.style.use('ggplot')
#%%Data loading
res = pd.read_csv('props_new\\res.csv')
resRock = res[['dt','gr','phie','rhob']]

#%% Clustering
scaler = StandardScaler()

data = scaler.fit_transform(resRock)

#%%
max_k=15
wcss=[]
dbs=[]
sil=[]
k_range = range(2,max_k)
for k in tqdm(k_range):
    kmeans = KMeans(n_clusters=k)
    temp_pred = kmeans.fit_predict(data)
    wcss_k = kmeans.inertia_
    wcss.append(wcss_k)
    dbs.append(davies_bouldin_score(data,temp_pred))
    sil.append(silhouette_score(data,temp_pred))

#%% Plotting DBScores and Silhouette for optimal k
plt.figure(figsize=[8,6])
plt.subplot(2,1,1)
plt.plot(k_range,sil)
plt.ylabel("Silhueta")
plt.subplot(2,1,2)
plt.plot(k_range,dbs)
plt.ylabel("Davis-Bouldin")
plt.xlabel('Número Clusters')



#%% Making both measures into a single one towards finding optimal K
db_std  = scaler.fit_transform(np.array(dbs).reshape(-1, 1))
sil_std = scaler.fit_transform(np.array(sil).reshape(-1, 1))
combined = db_std-sil_std

plt.figure(figsize=[8,3])
plt.plot(k_range,combined)
plt.ylabel("Silhueta - Davies-Bouldin (Escalado)")
plt.xlabel('Número Clusters')

#%% Optimal K
opt_k = k_range[np.where(combined == np.min(combined))[0][0]]

#%% Redo clustering now with optimal K clusters

kmeans = KMeans(n_clusters=opt_k)
gmm = GaussianMixture(n_components=opt_k)

gmm.fit(data)
pred_g = gmm.predict(data)
prob_g = gmm.predict_proba(data)
pred_k = kmeans.fit_predict(data)

#%% Passing predictions to DF
res['KMeans'] = pd.Series(pred_k)
res['GMM'] = pd.Series(pred_g)
for i in range(opt_k):
     col_name = "cluster "+str(i)
     res[col_name] = prob_g.T[i]

res.to_csv('props_new\\cluster.csv')



# %%
