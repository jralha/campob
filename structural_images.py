# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(suppress=True)
pd.set_option('mode.chained_assignment', None)
plt.style.use('ggplot')


# %%
res = pd.read_csv('props_new\\res.csv')


# %%
lats = res['ycoord']
med = np.median(lats)

nor = res.loc[ res['ycoord'] > med]
sou = res.loc[ res['ycoord'] <= med]

fn = nor.loc[ (nor['anttrracking'] > -0.5) & (nor['anttrracking'] < 1) ]
fs = sou.loc[ (sou['anttrracking'] > -0.7) & (sou['anttrracking'] < 1) ]

plt.scatter(fn['xcoord'],fn['ycoord'],s=5,label='Zona Norte - '+str(len(fn))+' pontos com Ant-Tracking > -0.8')
plt.scatter(fs['xcoord'],fs['ycoord'],s=5,label='Zona Sul - '+str(len(fs))+' pontos com Ant-Tracking > -0.8')
plt.ylabel('Latitude')
plt.xlabel('Longitude')
plt.legend(loc='upper left', bbox_to_anchor=(-0.1, -0.15))


# %%
plt.scatter(nor['xcoord'],nor['ycoord'],s=5,label='Zona Norte')
plt.scatter(sou['xcoord'],sou['ycoord'],s=5,label='Zona Sul')
plt.ylabel('Latitude')
plt.xlabel('Longitude')
plt.legend(loc='upper left', bbox_to_anchor=(-0.1, -0.15))


# %%
plt.scatter(nor['xcoord'],nor['anttrracking'],s=5,label='Zona Norte')
plt.scatter(sou['xcoord'],sou['anttrracking'],s=5,label='Zona Sul')
plt.xlabel('Longitude')
plt.ylabel('Ant-Tracking')


# %%



