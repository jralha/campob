#%%
import os
cwd = os.getcwd()
os.chdir('PyGRDECL')
from GRDECL2VTK import *
os.chdir(cwd)

# %%
Model=GeologyModel(filename='props_new\\test.GRDECL)