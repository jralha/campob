#!usr/bin/env python3

#%% Libraries

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import seaborn as sns
import numpy as np
import os

#%%Data loading
res = pd.read_csv('csv_outs\\res.csv')
quis = pd.read_csv('csv_outs\\quis.csv')
nres = quis.loc[quis['OWC'] <= 0 ]

#%% North and South Zones
_ys = res['i'].tolist()
ymax = np.max(_ys)
ymin = np.min(_ys)
#y_med = ymin+((ymax-ymin)/2)
y_med = np.median(res['i'])

ns=[]
for y in _ys:
    if y > y_med:
        ns.append(1)
    else:
        ns.append(0)
res['N/S'] = pd.Series(ns)

#%%Sampling for easier plots and rock/fluid separation
resSample = res.sample(n=5000)

features = res[['GR','phie','RHOB','SW','ILD','Ant Tracking','N/S']]
featSample = features.sample(n=5000)
resRock = res[['GR','phie','RHOB','N/S']]
rockSample = resRock.sample(n=5000)
resFluid = res[['SW','ILD','N/S']]
fluidSample = resFluid.sample(n=5000)

#%%
sns.scatterplot(
    x=resSample['phie'],
    y=resSample['GR'],
    s=10,
    hue=resSample['N/S'],
    edgecolors='none'
)
#%%
plt.figure(figsize=[16,12])
n=1
for col in rockSample.columns:
    temp0 = rockSample.loc[rockSample['N/S'] == 0]
    temp1 = rockSample.loc[rockSample['N/S'] == 1]
    #temp0.drop(['N/S'])
    #temp1.drop(['N/S'])
    plt.subplot(2,int(float(len(rockSample.columns))/2)+1,n)
    sns.distplot(temp0[col],hist=False)
    sns.distplot(temp1[col],hist=False)
    n=n+1
plt.show()

#%%
from sklearn.mixture import GaussianMixture
from sklearn.metrics import davies_bouldin_score, silhouette_score
from sklearn.cluster import k_means

kmeans = k_means(3)