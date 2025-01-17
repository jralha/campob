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

# plt.scatter(fn['xcoord'],fn['ycoord'],s=5,label='Zona Norte - '+str(len(fn))+' pontos com Ant-Tracking > -0.8')
# plt.scatter(fs['xcoord'],fs['ycoord'],s=5,label='Zona Sul - '+str(len(fs))+' pontos com Ant-Tracking > -0.8')
# plt.ylabel('Latitude')
# plt.xlabel('Longitude')
# plt.legend(loc='upper left', bbox_to_anchor=(-0.0, 1.15))
# plt.show()

# exit()

# %%
# plt.scatter(nor['xcoord'],nor['ycoord'],s=5,label='Zona Norte')
# plt.scatter(sou['xcoord'],sou['ycoord'],s=5,label='Zona Sul')
# plt.ylabel('Latitude')
# plt.xlabel('Longitude')
# plt.legend(loc='upper left', bbox_to_anchor=(-0.0, 1.15))
# plt.show()
# exit()

# %%
# plt.scatter(res['ycoord'],res['anttrracking'],s=1,c='black')
# plt.xlabel('Latitude')
# plt.ylabel('Ant-Tracking')
# plt.show()

# %%
# plt.scatter(fs['xcoord'],fs['ycoord'],s=0.5,c=fs['dist_fault'],cmap='magma_r')
# plt.scatter(fn['xcoord'],fn['ycoord'],s=0.5,c=fn['dist_fault'],cmap='magma_r')
# plt.ylabel('Latitude')
# plt.xlabel('Longitude')
# plt.colorbar()
# plt.show()

#%%
rng = range(-10,8)
fracs=[]
fracn=[]
lims=[]
for i in rng:
    limiar = float(i/10)
    lims.append(limiar)
    nn = nor.loc[nor['anttrracking'] > limiar]
    ss = sou.loc[sou['anttrracking'] > limiar]
    ln = len(nn)
    ls = len(ss)
    t = ln+ls
    if t != 0:
        fracs.append(ls/t)
        fracn.append(ln/t)
    else:
        fracs.append(0)
        fracn.append(0)

plt.plot(lims,fracn,label='Zona Norte')
plt.plot(lims,fracs,label='Zona Sul')
plt.legend()
plt.xlabel('Limiar Mínimo de Ant-Tracking')
plt.ylabel('% células Ant-Tracking > Limiar')
plt.show()