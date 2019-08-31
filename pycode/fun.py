import numpy as np
from tqdm.auto import tqdm
import pandas as pd

def get_prop_array(propfile):
    '''Gets property values for each cell.'''
    f0 = open(propfile,'r').read().split("\n")[0:] #Opens property file and defines an array where each line is an array element.
    f = [] #Empty array to be populated with values.
    for i in tqdm(f0,position=0): #For each line
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

def grid_coords(gridfile):    
    coord_file = files.loc[files['PROPERTY'] == 'COORD']['FILE'].iloc[0].replace("\'","")
    coords = get_prop_array(coord_file)
    xcoords = coords[0::3]
    xcoords = list(OrderedDict.fromkeys(xcoords))
    ycoords = coords[1::3]
    ycoords = list(OrderedDict.fromkeys(ycoords))
    dictio={"X":xcoords,"Y":ycoords}
    return pd.DataFrame(dictio)

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

def grid_files(gridfile):
    '''Get property names and file paths from grid.'''
    f = open(gridfile,'r')
    text=[]
    for line in f:
        text.append(line.replace("[","").replace("]","").replace("\n",""). replace(" /",""))
        
    propfiles=[]
    for line in text:
        if "_PROP_" in line:
            propfiles.append(line)
        elif "_COORD" in line:
            coord_file = line
        elif "_ACTNUM" in line:
            act_file = line
        elif "ZCORN" in line:
            zcorn_file = line
        
    pnames=[]
    for i in propfiles:
        pnames.append(i.split(".")[0].split("_",maxsplit=2)[2:])
        
    pnames.append("COORD")
    pnames.append("ACTNUM")
    pnames.append("ZCORN")
    propfiles.append(coord_file)
    propfiles.append(act_file)
    propfiles.append(zcorn_file)
        
    prop_dict = {"PROPERTY":pnames,"FILE":propfiles}
    files_df = pd.DataFrame(prop_dict)