#%%
import numpy as np
#from tqdm.auto import tqdm

def prop_list(filename):
    f0 = open(filename,'r').read().split('/')
    return f0

block =prop_list('props_new\\test.GRDECL')

# %%
