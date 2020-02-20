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
res['nor_bool'] = nor_bool

sns.pairplot(res,hue='nor_bool', plot_kws=dict(edgecolor="none",marker='.',s=0.05) ) 
plt.show()

# %%
