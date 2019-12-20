#%%
import glob
import numpy as np
import pandas as pd

# %%
def load_prop_array(propfile):
    # print('Opening file '+propfile)
    file = open(propfile,'r').read().split('/')[1]
    file = file.split('\n')
    # print(str(len(file))+' lines.')
    block=[]
    for line in file[4:]:
        dline = line.replace('  ','')
        if dline[-1] == ' ': dline = dline[:-1]
        dline=dline.split(' ')
        for element in dline:
            if '*' in element:
                rep = int(element.split('*')[0])
                val = float(element.split('*')[1])
            elif ' ' not in element:
                rep = 1
                val = float(element)
            
            n=0
            while n < rep:
                block.append(val)
                n=n+1


    return block


#%%
prop_folder = 'campob\props_new'
props = glob.glob(prop_folder+'\\*.GRDECL')
propnames = [ name.split('\\')[-1].split('.')[0] for name in props]

#%%
data=[]
for prop in (props):
    prop_array = load_prop_array(prop)
    data.append(prop_array)



# %%
dataset = np.array(data)
dataset = pd.DataFrame(dataset.T)
dataset.columns = propnames

# %%
for num,i in enumerate(dataset):
    print(len(i),props[num])
# %%

quis = dataset.loc[ dataset['zones'] == 2 ]
res = quis.loc[ quis['owc'] > 0 ]

#%%
quis.to_csv('campob\\props_new\\quis.csv')
res.to_csv('campob\\props_new\\res.csv')

# %%
