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
feats=['gr','dt','rhob','phie']

res = pd.read_csv('props_new\\res.csv')
res['rhob'] = res['rhob']/1000
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
res_sample=res.sample(10000)
nor = res.loc[ res['Zona'] == 'Norte']
sul = res.loc[ res['Zona'] == 'Sul' ]
nor_s = res_sample.loc[ res_sample['Zona'] == 'Norte']
sul_s = res_sample.loc[ res_sample['Zona'] == 'Sul' ]

combs = list(itertools.combinations(feats,2))

# #%%
# plt.figure()
# n=1
# for feat in feats:
#     plt.subplot(1,len(feats),n)
#     sns.distplot(nor[feat],hist=False,label='Norte')
#     sns.distplot(sul[feat],hist=False,label='Sul')
#     plt.yticks([])
#     n=n+1
# plt.show()
# %%

n=2
for comb in combs:
    plt.figure(figsize=[5,2.5])
    X = comb[0]
    Y = comb[1]
    plt.subplot(1,2,1)
    sns.kdeplot(nor[X],nor[Y], shade=True, shade_lowest=False,cmap='Reds')
    plt.scatter(nor_s[X],nor_s[Y],alpha=0.15,label='Zona Norte',marker='.',s=1,c='black')
    plt.legend(facecolor='white')
    plt.ylabel(Y)
    plt.xlabel(X)
    plt.subplot(1,2,2)
    sns.kdeplot(sul[X],sul[Y], shade=True, shade_lowest=False,cmap='Blues')
    plt.scatter(sul_s[X],sul_s[Y],alpha=0.15,label='Zona Sul',marker='.',s=1,c='black')
    plt.xlabel(X)
    plt.ylabel('')
    plt.yticks([])
    plt.legend(facecolor='white')
    plt.tight_layout()
    # plt.show()
    fname='temp'+str(n)+'.png'
    plt.savefig(fname)
    n=n+1

# %%
# from mpl_toolkits.mplot3d import Axes3D
# combs3 = list(itertools.combinations(feats,3))

# for comb in combs3[0:1]:
#     X=comb[0]
#     Y=comb[1]
#     Z=comb[2]

#     fig = plt.figure()
#     ax = fig.add_subplot(121, projection='3d')
#     ax.scatter(nor_s[X],nor_s[Y],nor_s[Z],marker='.',s=5,alpha=0.2,c='black')
#     ax.set_xlabel(X)
#     ax.set_ylabel(Y)
#     ax.set_zlabel(Z)
#     # plt.zlabel(Z)
#     ax2 = fig.add_subplot(122, projection='3d')
#     ax2.scatter(sul_s[X],sul_s[Y],sul_s[Z],marker='.',s=5,alpha=0.2,c='black')
#     ax2.set_xlabel(X)
#     ax2.set_ylabel(Y)
#     ax2.set_zlabel(Z)
#     # plt.zlabel(Z)
#     plt.show()

# %%
