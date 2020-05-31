#%% Libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use('ggplot')
np.set_printoptions(suppress=True)
pd.set_option('mode.chained_assignment', None)

#%% Data load
res = pd.read_csv('props_new\\cluster.csv')

#%% Define datasets, reorder clusters in order of Porosity
gmm = res[['dt','gr','phie','rhob','GMM']]
kme = res[['dt','gr','phie','rhob','KMeans']]

kme_describe=kme.groupby('KMeans').describe()
gmm_describe=gmm.groupby('GMM').describe()

kme_phi = kme_describe[[('phie',  'mean')]]
originalOrderK = list(kme_phi.index)
sortedK = kme_phi.sort_values(('phie','mean'))
newOrderK = list(sortedK.index)
swapK = dict(zip(newOrderK,originalOrderK))

gmm_phi = gmm_describe[[('phie',  'mean')]]
originalOrderG = list(gmm_phi.index)
sortedG = gmm_phi.sort_values(('phie',  'mean'))
newOrderG = list(sortedG.index)
swapG = dict(zip(newOrderG,originalOrderG))

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

res = res.rename(swapNames)



#%% Redo cluster stats
gmm = res[['dt','gr','phie','rhob','GMM']]
kme = res[['dt','gr','phie','rhob','KMeans']]
kme_describe=kme.groupby('KMeans').describe()
gmm_describe=gmm.groupby('GMM').describe()
for col in kme_describe.columns:
    if 'std' in col:
        kme_describe[(col[0],'CV')] = kme_describe[col] / kme_describe[(col[0],'mean')]
        gmm_describe[(col[0],'CV')] = gmm_describe[col] / gmm_describe[(col[0],'mean')]
    if 'mean' not in col and 'CV' not in col:
        kme_describe = kme_describe.drop(col,axis=1)[['dt','gr','phie','rhob']]
        gmm_describe = gmm_describe.drop(col,axis=1)[['dt','gr','phie','rhob']]


#%% Save files
# res.to_csv('props_new\\cluster_reorder.csv')
# kme_describe.to_csv('props_new\\kme_stats.csv')
# gmm_describe.to_csv('props_new\\gmm_stats.csv')

# %%
props = ['dt','gr','phie','rhob']
cmap = plt.get_cmap('plasma',3).colors
nplot=1
plt.figure(figsize=[8,8])
for prop in props:
    plt.subplot(2,2,nplot)
    sns.boxplot(
        data=gmm,
        y=prop,
        x='GMM',
        showfliers=False,
        showmeans=True,
        palette=cmap,
        meanprops=dict(marker="o",markerfacecolor='white', markersize=5,markeredgecolor='black'),     
        )
    plt.xlabel('Cluster')
    if prop == 'dt':
        plt.ylabel('DT (us/ft)')
        plt.title('DT - GMM')
    elif prop == 'gr':
        plt.ylabel('GR (gAPI)')
        plt.title('GR - GMM')
    elif prop == 'phie':
        plt.ylabel('PHIE (v/v)')
        plt.title('PHIE - GMM')
    elif prop == 'rhob':
        plt.ylabel('RHOB (g/cm³)')
        plt.title('RHOB - GMM')
    nplot+=1
plt.tight_layout()

# %%
nplot=1
plt.figure(figsize=[8,8])
for prop in props:
    plt.subplot(2,2,nplot)
    sns.boxplot(
        data=kme,
        y=prop,
        x='KMeans',
        showfliers=False,
        showmeans=True,
        palette=cmap,
        meanprops=dict(marker="o",markerfacecolor='white', markersize=5,markeredgecolor='black'),     
        )
    plt.xlabel('Cluster')
    if prop == 'dt':
        plt.ylabel('DT (us/ft)')
        plt.title('DT - KMeans')
    elif prop == 'gr':
        plt.ylabel('GR (gAPI)')
        plt.title('GR - KMeans')
    elif prop == 'phie':
        plt.ylabel('PHIE (v/v)')
        plt.title('PHIE - KMeans')
    elif prop == 'rhob':
        plt.ylabel('RHOB (g/cm³)')
        plt.title('RHOB - KMeans')
    nplot+=1
plt.tight_layout()


# %%
