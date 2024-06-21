import numpy as np


def load_data(file):

    """
    Read a VRP instance from a .vrp file, and returns the px, py, demand, capacity, depot.

    :param file: the .vrp file.
    :return: px, py, demand, capacity, depot
    """

    print("Loading VRP data file:", file)

    f = open(file, "r") #open file and read

    capacity = 0 #set vehicle capacity to 0
    # Skip the first information rows until "NODE_COORD_SECTION" is seen
    line = f.readline() #read first line in file
    while not line.__contains__("NODE_COORD_SECTION"): #while line does not have "NODE_COORD_SECTION"
        if line.__contains__("CAPACITY"): #if line contains "CAPACITY"
            capacity = float(line.split()[-1]) #set capacity to last element in the line
        line = f.readline() #read next line

    # Read the coordinate section
    id, px, py = [], [], [] #set id, plot x and plot y to empty lists

    line = f.readline() #read next line
    while not line.__contains__("DEMAND_SECTION"): #while line does not have "DEMAND_SECTION"
        line_elements = line.split() #split line into elements
        id.append(int(line_elements[0])) #append first element to id
        px.append(float(line_elements[1])) #append second element to px
        py.append(float(line_elements[2])) #append third element to py
        line = f.readline() #read next line

    # Read the demand section
    demand = np.zeros(len(id)) #create array of zeros with length of id
    line = f.readline() #read next line
    while not line.__contains__("DEPOT_SECTION"): #while line does not have "DEPOT_SECTION"
        line_elements = line.split() #split line into elements
        pos = id.index(int(line_elements[0])) #set pos to index of first element in id
        demand[pos] = float(line_elements[1]) #set demand at pos to second element
        line = f.readline() #read next line

    # Read the single depot
    line = f.readline().rstrip("\n") #read next line and remove newline character
    depot = id.index(int(line)) #set depot to index of first element in id

    f.close() #close file

    return np.array(px), np.array(py), demand, capacity, depot #return px, py, demand, capacity, depot


def load_solution(file):

    """
    Read a VRP solution from a .sol file.

    :param file: the .sol file.
    :return: The VRP solution, which is an array of arrays (excluding the depot).
    """

    f = open(file, "r") #open file and read

    routes = [] #set routes to empty list
    line = f.readline() #read first line in file
    while line.__contains__("Route"): #while line contains "Route"
        a_route_str = line.split(":")[1].lstrip().rstrip() #set a_route_str to line split at ":" and remove leading and trailing whitespace
        a_route = np.array(a_route_str.split()).astype(int) #set a_route to a_route_str split and converted to int

        routes.append(a_route) #append a_route to routes
        line = f.readline() #read next line

    f.close() #close file

    return np.array(routes, dtype=object) #return routes as object
