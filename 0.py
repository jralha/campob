#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'Jupyter\campob'))
	print(os.getcwd())
except:
	pass

#%%



#%%
import pandas as pd
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
sns.set()

#%% [markdown]
# A Function to get various info from the grid index file, returns grid dimensions, origin spatial reference, grid spatial unit and coordinate system.

#%%
def grid_info(gridfile):
    '''Gets grid geometry and coordinate system information from grid.'''
    f = open(gridfile,'r')
    text=[]
    for line in f:
        text.append(line.replace("[","").replace("]","").replace("\n",""). replace(" /",""))
        
    for line in text:
        if "SPECGRID" in line:
            i = text.index(line)
            specgrid = text[i+1]
        elif "MAPUNITS" in line:
            i = text.index(line)
            map_unit = text[i+1]
        elif "MAPAXES" in line:
            i = text.index(line)
            map_axes = text[i+1]
        elif "GRIDUNIT" in line:
            i = text.index(line)
            gridunit = text[i+1]
        elif "COORDSYS" in line:
            i = text.index(line)
            crs = text[i+1]
        
    
    #Specgrid contains the dimensional information
    dims=specgrid.split()
    xdim=int(dims[0])
    ydim=int(dims[1])
    zdim=int(dims[2])
    
    #Map axes contains 3 points, p0 is the origin, p1 is at the first inline and last crossline and p2 at the first crossline and last inline.
    #As such, the vector (p0,p1) represents the crossline direction.
    #The (p0,p2) vector represents the inline direction.
    points=map_axes.split()
    p0=[points[0],points[1]]
    p1=[points[2],points[3]]
    p2=[points[4],points[5]]
    
    #Passes data into a Pandas dataframe for effortless viewing of the data.
    info_dict = {"XDIM":xdim,"YDIM":ydim,"ZDIM":zdim,"Surface Point 0":p0,"Surface Point 1":p1,"Surface Point 2":p2,"Unit":gridunit}
    grid_df = pd.DataFrame(info_dict)

    return grid_df

#%% [markdown]
# Function parsing property files into Numpy arrays.
# 
# Please note the if function. As to reduce filesizes, Petrel groups adjacent cells with similar values together, so this needs to be considered when parsing.
# 
# Example, given 5 consectuve cells with these PhiE values:
# 
# Cell n ---- 0.32      
# Cell n+1 - 0.41      
# Cell n+2 - 0.41     
# Cell n+3 - 0.41      
# Cell n+4 - 0.29      
# 
# Petrel will export those cells as  [ 0.32 , 3*0.41 , 0.29 ]

#%%
def get_prop_array(propfile):
    '''Gets property values for each cell.'''
    f0 = open(propfile,'r').read().split("\n")[0:] #Opens property file and defines an array where each line is an array element.
    f = [] #Empty array to be populated with values.
    for i in tqdm(f0): #For each line
        if "--" not in i and i != "" and i != "/": #Ignore header lines and end of line / symbols.
            temp = i.split() #Temporary value splitting non-header lines into individual cell values.
            for j in temp: # For each cell value.
                if "*" in j and j != "/": #If Petrel grouped up adjacent cells. Also ignore / end of line symbols
                    n = int(j.split("*")[0]) #Get number of grouped up cells
                    N=1 
                    while N <= n: #Start while loop
                        f.append(np.float(j.split("*")[1])) #Pass the grouped cell value N times into the property array.
                        N=N+1
                elif j != "/":    #Ignore / end of line symbols, probably redundant
                    f.append(np.float(j)) #Pass the cell value into property array for non-grouped up cells.
                else:
                    continue #If line is empty or only contains the / end of line symbol, skip line.
    #array = da.from_array(f,chunks=100000)
    return f

#%% [markdown]
# Defining Grid Geometry
# 
# X, Y and Z dims are the number of cells in each direction. Where X is the crossline direction and Y the inline direction.
# 
# Multiplying each dimensions returns the total number of cells in the grid.

#%%
grid='data/campob.GRDECL' #Gridfile
info = grid_info(grid) #Run info function for gridfile
info


#%%
#Get dimensional values from info table.
xdim = info['XDIM'].iloc[0]
ydim = info['YDIM'].iloc[0]
zdim = info['ZDIM'].iloc[0]
p0 = [float(info['Surface Point 0'].iloc[0]),float(info['Surface Point 0'].iloc[1])]

#Calculate gridsize.
gridsize2d = xdim*ydim
gridsize3d = (gridsize2d*zdim)

print("Grid contains "+str(gridsize2d)+" cells in 2D and "+str(gridsize3d)+" cells in 3D.")
print("Grid origin at the "+str(p0[0])+", "+str(p0[1])+" UTM coordinates.")

#%% [markdown]
# Grid Coordinate reference.
# 
# Back in Petrel grid properties related the cell coordinate were generated, they're used as their geospatial reference instead of relying on Petrel's complicated system to define grid geometry.
# 
# Properties are also created for cell size in each direction and index position of the cell in each direction. Where i is the crossline direction, j is the inline direction and k is the depth direction.

#%%
coordsx = get_prop_array('props/campob_PROP_XCOORD.GRDECL')
coordsy = get_prop_array('props/campob_PROP_YCOORD.GRDECL')
coordsz = get_prop_array('props/campob_PROP_ZCOORD.GRDECL')


#%%
celli = get_prop_array('props/campob_PROP_I_INDEX.GRDECL')
cellJ = get_prop_array('props/campob_PROP_J_INDEX.GRDECL')
cellK = get_prop_array('props/campob_PROP_K_INDEX.GRDECL')


#%%
sizex = get_prop_array('props/campob_PROP_CELL_X_DIMENSION.GRDECL')
sizey = get_prop_array('props/campob_PROP_CELL_Y_DIMENSION.GRDECL')
sizez = get_prop_array('props/campob_PROP_CELL_HEIGHT.GRDECL')

#%% [markdown]
# Grid Properties

#%%
sw = get_prop_array('props/campob_PROP_SWMMM195N240.GRDECL')
phie = get_prop_array('props/campob_PROP_PHIE.GRDECL')
cali = get_prop_array('props/campob_PROP_LOCAL_CALI.GRDECL')
ant = get_prop_array('props/campob_PROP_SEISMIC_-_ANT_TRACKING.GRDECL')
gr = get_prop_array('props/campob_PROP_GR.GRDECL')
ild = get_prop_array('props/campob_PROP_ILD.GRDECL')
nphi = get_prop_array('props/campob_PROP_ILD.GRDECL')
acous = get_prop_array('props/campob_PROP_AI.GRDECL')


#%%
region = get_prop_array('props/campob_PROP_REGIONS_ALL_ZONES.GRDECL')


#%%
owc = get_prop_array('props/campob_PROP_OIL_WATER_CONTACT.GRDECL')

#%% [markdown]
# Setting Up data for analysis.
# 
# The region property is based on the physical model generated by the horizons, cells within the Quissamã formation are in region 3.
# 
# Reservoir cells are cells within the Quissamã formation that are above the Oil Water Contact (OWC)

#%%
dictio = {'X':coordsx, 'Y':coordsy, 'Z':coordsz, 'i':celli, 'j':cellJ, 'k':cellK, 'dx':sizex, 'dy':sizey, 'dz':sizez, 'region':region, 'SW':sw, 'phie':phie, 'OWC':owc,'CALI':cali,'Ant Tracking':ant,'GR':gr,'ILD':ild,'NPHI':nphi,'AI':acous}
data = pd.DataFrame(dictio)


#%%



#%%
data_clean = data.loc[data['SW'] > -1 ]
quissama = data_clean.loc[data_clean['region'] == 2]
reservoir = quissama.loc[quissama['OWC'] > 0 ]

#%% [markdown]
# Export to CSV

#%%
quissama.to_csv('quis.csv',index=0)


#%%
reservoir.to_csv('res.csv',index=0)


#%%



