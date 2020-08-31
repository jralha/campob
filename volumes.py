#%%
import pandas as pd
import numpy as np

#%%
def vol_case(frame,phiE,sW,NG): 
    vb = frame['bulkvolume']
    vp = vb*phiE
    oip = vp*(1-sW)
    hcpv = oip*NG 
    return np.sum(vb), np.sum(vp), np.sum(oip), np.sum(hcpv)

#%% New columns
data = pd.read_csv('props_new\\cluster_reorder.csv')
data['cluster 1-2'] = 1-data['cluster 0']

#%%
percs=[50,70,90]
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
#Case 1-3 - 50-75-90 Percentile NGs
vols.append(vol_case(data,data['phie'],data['sw'],data['NG perc 50']))
vols.append(vol_case(data,data['phie'],data['sw'],data['NG perc 70']))
vols.append(vol_case(data,data['phie'],data['sw'],data['NG perc 90']))
#Case 5 - GMM Probability not class 0
vols.append(vol_case(data,data['phie'],data['sw'],1-data['cluster 1-2']))
#Vol classes
ks = range(3)
algos = ['GMM']
for algo in algos:
    for k in ks:
        slc = data.loc[data[algo] == k]
        vols.append(vol_case(slc,slc['phie'],slc['sw'],1))
#Case 4 - Boolean GMM Class not 0
vb4 = vols[-1][0]+vols[-2][0]+vols[-3][0]
vp4 = vols[-1][0]+vols[-2][0]+vols[-3][0]
oip4 = vols[-2][0]+vols[-3][0]
hcpv4 = vols[-2][0]+vols[-3][0]
case4 = (vb4,vp4,oip4,hcpv4)
vols = vols[:4]+[case4]+vols[4:]


#%%
vols = pd.DataFrame(vols)
vols.columns=['Vb','Vp','OIP','HCPV']
cases = ['Melani',
        'NG 50%',
        'NG 75%',
        'NG 90%',
        'GMM 1 ou 2',
        'NG = GMM P\'(0)',
        'GMM 0',
        'GMM 1',
        'GMM 2']

vols['Case'] = pd.Series(cases)

#%%
vols.to_csv('props_new\\volume_cases.csv')

# %%
