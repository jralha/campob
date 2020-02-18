#%%
import pandas as pd
import numpy as np
np.set_printoptions(suppress=True)
pd.set_option('mode.chained_assignment', None)

#%% Data load
feats=['gr','dt','rhob','phie','sw']

res = pd.read_csv('props_new\\res.csv')
lats = res['ycoord']
med = np.median(lats)
nor = res.loc[ res['ycoord'] > med][feats]
sou = res.loc[ res['ycoord'] <= med][feats]
res = res[feats]

quis = pd.read_csv('props_new\\quis.csv')
nres = quis.loc[quis['owc'] <= 0 ][feats]
quis = quis[feats]

#%%
zones = [nor,sou,res,nres,quis]
zone_names=['nor','sou','res','nres','quis']

all_stats=[]
for n,zone in enumerate(zones):
    stats = zone.describe().iloc[1:3,:].T
    stats['std'] = stats['std']/stats['mean']
    stats.columns = ['mean','cv']
    stats = stats.T
    stats['zone'] = zone_names[n]
    all_stats.append(stats)
output=pd.concat(all_stats)

#%%
output.to_excel('dissertacao\\prop_stats.xlsx')



# %%
output

# %%
