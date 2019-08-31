def get_prop_array(propfile):
    import numpy as np
    from tqdm.auto import tqdm
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