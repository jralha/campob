#%%
import pandas as pd
import numpy as np
from campob.pycode.fun import gridTools

#%%
def vol_case(frame,phiE,sW,NG): 
    dX = frame['dx']
    dY = frame['dy']
    dZ = frame['dz']
    vb = dX*dY*dZ
    vp = vb*phiE
    oip = vp*sW
    hcpv = oip*NG 
    return np.sum(vb), np.sum(vp), np.sum(oip), np.sum(hcpv)

#%%
melani = gridTools.get_prop_array('campob\\props\\campob_PROP_TOT_PAYFLAG.GRDECL')
owc = gridTools.get_prop_array('campob\\props\\campob_PROP_OIL_WATER_CONTACT.GRDECL')
region = gridTools.get_prop_array('campob\\props\\campob_PROP_REGIONS_ALL_ZONES.GRDECL')
dic = {"melani":melani,"owc":owc,"region":region}
temp = pd.DataFrame(dic)
temp = temp.loc[temp['region'] == 2]
temp = temp.loc[temp['owc'] > 0 ]

#%% New columns
data = pd.read_csv('campob\\csv_correcao\\cluster_reorder.csv')
data['ng melani'] = temp['melani'].values

percs=[50,75,90]
perc_ngs=[0]*len(percs)
for i,per in enumerate(percs):
    sws = data['SW']
    phs = data['phie']
    cut_sw = np.percentile(data['SW'],(100-per))
    cut_ph = np.percentile(data['phie'],per)
    bool_sw = sws < cut_sw
    bool_ph = phs > cut_ph
    ng_bool = ((bool_ph == True) & (bool_sw==True))*1
    data['NG perc '+str(per)] = ng_bool

data['cluster 1-2'] = 1-data['cluster 0']

#%%
vols=[]
#Case 0 - Melani et al 2015 NG
vols.append(vol_case(data,data['phie'],data['SW'],data['ng melani']))
#Case 1 - Total volume
vols.append(vol_case(data,data['phie'],data['SW'],1))
#Case 2 - Total Volume - Constant porosity
vols.append(vol_case(data,np.mean(data['phie']),data['SW'],1))
#Case 3 - Total volume - Constant SW
vols.append(vol_case(data,data['phie'],np.mean(data['SW']),1))
#Case 4-6 - 50-75-90 Percentile NGs
vols.append(vol_case(data,data['phie'],data['SW'],data['NG perc 50']))
vols.append(vol_case(data,data['phie'],data['SW'],data['NG perc 75']))
vols.append(vol_case(data,data['phie'],data['SW'],data['NG perc 90']))
#Case 7 - GMM Probability not class 0
vols.append(vol_case(data,data['phie'],data['SW'],1-data['cluster 1-2']))
#Case 8-13 - Vol classes
ks = range(3)
algos = ['KMeans','GMM']
for algo in algos:
    for k in ks:
        slc = data.loc[data[algo] == k]
        vols.append(vol_case(slc,slc['phie'],slc['SW'],1))

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
vols.to_csv('campob\\csv_outs\\volume_cases.csv')

# %%
