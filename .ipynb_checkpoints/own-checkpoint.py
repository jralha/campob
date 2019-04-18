#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('reset', '')


# In[ ]:





# Read .gredl initial file and define functions.

# In[4]:


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
    

    return files_df

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
        
    
    
    dims=specgrid.split()
    xdim=int(dims[0])
    ydim=int(dims[1])
    zdim=int(dims[2])
    
    points=map_axes.split()
    p0=[points[0],points[1]]
    p1=[points[2],points[3]]
    p2=[points[4],points[5]]
    
    info_dict = {"XDIM":xdim,"YDIM":ydim,"ZDIM":zdim,"Surface Point 1":p0,"Surface Point 2":p1,"Surface Point 3":p2,"Unit":gridunit}
    grid_df = pd.DataFrame(info_dict)

    return grid_df

def get_prop_array(propfile):
    '''Gets property values for each cell.'''
    f = open(propfile,'r')
    text=[]
    for line in f:
        text.append(line.replace("[","").replace("]","").replace("\n",""). replace(" /",""))
        
    values0=[]
    for line in text:
        if "--" in line or line == "":
            continue
        else:
            values0.append(line)
            
    array=[]
    n0=1
    for i in values0:
        splt = i.split()
        n0= n0+1
        nn0=1
        for j in splt:
            array.append(j)
            nn0= nn0+1
            sys.stdout.write(('\r'+str(propfile)+". Part "+str(n0)+" of "+str(len(values0))+". Part progress: "+str(nn0)+" of "+str(len(splt))+"values."))
            time.sleep(0.003)
            sys.stdout.flush()
            
    values=[]
    n1=1
    for i in array:
        n1 = n1+1
        if "*" in i:
            n = float(i.split("*")[0])
            nn = 1
            while nn < n:
                values.append(i.split("*")[1])
                nn = nn+1
                sys.stdout.write('\r'+str(propfile)+". Token "+str(nn)+" of "+str(n)+" value "+str(n1)+" of "+str(len(array)))
                time.sleep(0.003)
                sys.stdout.flush()
        else:
            values.append(i)
            sys.stdout.write('\r'+str(propfile)+". Value "+str(n1)+" of "+str(len(array)))
            time.sleep(0.003)
            sys.stdout.flush()

    return values

def grid_coords(gridfile):    
    coord_file = files.loc[files['PROPERTY'] == 'COORD']['FILE'].iloc[0].replace("\'","")
    coords = get_prop_array(coord_file)
    xcoords = coords[0::3]
    xcoords = list(OrderedDict.fromkeys(xcoords))
    ycoords = coords[1::3]
    ycoords = list(OrderedDict.fromkeys(ycoords))
    dictio={"X":xcoords,"Y":ycoords}
    return pd.DataFrame(dictio)
    

