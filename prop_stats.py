#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
import seaborn as sns
np.set_printoptions(suppress=True)
pd.set_option('mode.chained_assignment', None)
plt.style.use('ggplot')

#%% Data load
feats=['gr','dt','rhob','phie','sw']

res = pd.read_csv('props_new\\res.csv')
lats = res['ycoord']
med = np.median(lats)
res = res[feats]
nor_bool = (lats > med)*1
zones=[]
for i in nor_bool:
    if i == 1:
        zones.append('Norte')
    else:
        zones.append('Sul')
res['Zona'] = zones
res_sample=res.sample(1000)
nor = res.loc[ res['Zona'] == 'Norte']
sul = res.loc[ res['Zona'] == 'Sul' ]
nor_s = res_sample.loc[ res_sample['Zona'] == 'Norte']
sul_s = res_sample.loc[ res_sample['Zona'] == 'Sul' ]

combs = list(itertools.combinations(feats,2))

#%%
# plt.figure()
# n=1
# for feat in feats:
#     plt.subplot(1,len(feats),n)
#     sns.distplot(nor[feat],hist=False,label='Norte')
#     sns.distplot(sul[feat],hist=False,label='Sul')
#     n=n+1
# plt.show()
# %%
plt.figure()
n=1
for comb in combs:
    X = comb[0]
    Y = comb[1]
    plt.subplot(10,2,n)
    sns.kdeplot(nor[X],nor[Y],cmap="Reds", shade=True, shade_lowest=False)
    n=n+1
    plt.subplot(10,2,n)
    sns.kdeplot(sul[X],sul[Y],cmap="Blues", shade=True, shade_lowest=False)
    n=n+1
plt.show()
# %%
