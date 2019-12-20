#!usr/bin/env python3

#%% Libraries, settings and data folder

#General libs
import pandas as pd
import os

project_folder = 'D:\\rucksack\\Jupyter Notebooks\\campob'
os.chdir(project_folder)

#Project funs
from pycode.fun import gridTools

#%% Get grid info
main_grid_file = 'data\\campob.GRDECL'

info = gridTools.grid_info(main_grid_file)
xdim = info['XDIM'].iloc[0]
ydim = info['YDIM'].iloc[0]
zdim = info['ZDIM'].iloc[0]
p0 = [float(info['Surface Point 0'].iloc[0]),float(info['Surface Point 0'].iloc[1])]

#Calculate gridsize.
gridsize2d = xdim*ydim
gridsize3d = (gridsize2d*zdim)

print("Grid contains "+str(gridsize2d)+" surface cells and "+str(gridsize3d)+" total cells.")
print("Grid origin at the "+str(p0[0])+", "+str(p0[1])+" UTM coordinates.")

#%% Loading properties
props = [
    'XCOORD',
    'YCOORD',
    "ZCOORD",
    'I_INDEX',
    'J_INDEX',
    'K_INDEX',
    'CELL_X_DIMENSION',
    'CELL_Y_DIMENSION',
    'CELL_HEIGHT',
    'BULK_VOLUME',
    'ELEVATION_GENERAL',
    'GR',
    'ILD', 
    'SWMMM195N240', 
    'PHIE', 
    'RHOB', 
    'SEISMIC_-_ANT_TRACKING',
    'REGIONS_ALL_ZONES',
    'OIL_WATER_CONTACT'
    ]
prop_array = []
n=1
for prop in (props):
    print('Loading proprerty '+prop+' ['+str(n)+'/'+str(len(props))+']')
    prop_array.append(gridTools.get_prop_array('data\\campob_PROP_'+prop+'.GRDECL'))
    n=n+1

#%% Building Dataframe
data = pd.DataFrame(prop_array)
data.columns = props

data_clean = data.loc[data['SW'] > -1 ]
quissama = data_clean.loc[data_clean['region'] == 2]
reservoir = quissama.loc[quissama['OWC'] > 0 ]

#%% Output
quissama.to_csv('csv_outs_new\\quis.csv')
reservoir.to_csv('csv_outs_new\\res.csv')
