#%%
import pandas as pd
import numpy as np

#%%
def vol_case(frame,phiE,sW,NG): 
    vb = frame['bulkvolume']
    vp = vb*phiE
    oip = vp*sW
    hcpv = oip*NG 
    return np.sum(vb), np.sum(vp), np.sum(oip), np.sum(hcpv)

#%% New columns
data = pd.read_csv('props_new\\cluster_reorder.csv')
data['cluster 1-2'] = 1-data['cluster 0']

#%%
percs=[50,75,90]
perc_ngs=[0]*len(percs)
for i,per in enumerate(percs):
    sws = data['sw']
    phs = data['phie']
    cut_sw = np.percentile(data['sw'],(100-per))
    cut_ph = np.percentile(data['phie'],per)
    bool_sw = sws < cut_sw
    bool_ph = phs > cut_ph
    ng_bool = ((bool_ph == True) & (bool_sw==True))*1
    data['NG perc '+str(per)] = ng_bool

#%%
vols=[]
#Case 0 - Melani et al 2015 NG
vols.append(vol_case(data,data['phie'],data['sw'],data['payflag_melani_nearest']))
#Case 1 - Total volume
vols.append(vol_case(data,data['phie'],data['sw'],1))
#Case 2 - Total Volume - Constant porosity
vols.append(vol_case(data,np.mean(data['phie']),data['sw'],1))
#Case 3 - Total volume - Constant SW
vols.append(vol_case(data,data['phie'],np.mean(data['sw']),1))
#Case 4-6 - 50-75-90 Percentile NGs
vols.append(vol_case(data,data['phie'],data['sw'],data['NG perc 50']))
vols.append(vol_case(data,data['phie'],data['sw'],data['NG perc 75']))
vols.append(vol_case(data,data['phie'],data['sw'],data['NG perc 90']))
#Case 7 - GMM Probability not class 0
vols.append(vol_case(data,data['phie'],data['sw'],1-data['cluster 1-2']))
#Case 8-13 - Vol classes
ks = range(3)
algos = ['KMeans','GMM']
for algo in algos:
    for k in ks:
        slc = data.loc[data[algo] == k]
        vols.append(vol_case(slc,slc['phie'],slc['sw'],1))

#%%
vols = pd.DataFrame(vols)
vols.columns=['Vb','Vp','OIP','HCPV']
cases = ['Melani',
        'Volume Total',
        'Volume Total - Porosidade Constante (Valor médio)',
        'Volume Total - Saturação de Água Constante (Valor médio)',
        'NG 50%',
        'NG 75%',
        'NG 90%',
        'NG = GMM P\'(0)',
        'Kmeans 0',
        'Kmeans 1',
        'Kmeans 2',
        'GMM 0',
        'GMM 1',
        'GMM 2']
vols['Case'] = pd.Series(cases)

#%%
vols.to_csv('props_new\\volume_cases.csv')

# %%
