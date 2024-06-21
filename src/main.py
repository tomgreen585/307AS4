import utility as utility
import loader as loader
import numpy as np
import warnings
import math

warnings.filterwarnings("ignore")

def main():

    # Paths to the data and solution files.
    vrp_file = "n32-k5.vrp"  # "data/n80-k10.vrp"
    sol_file = "n32-k5.sol"  # "data/n80-k10.sol"
    
    # vrp_file = "n80-k10.vrp"
    # sol_file = "n80-k10.sol"

    # Loading the VRP data file.
    px, py, demand, capacity, depot = loader.load_data(vrp_file)

    # Displaying to console the distance and visualizing the optimal VRP solution.
    vrp_best_sol = loader.load_solution(sol_file)
    best_distance = utility.calculate_total_distance(vrp_best_sol, px, py, depot)
    print("Best VRP Distance:", best_distance)
    utility.visualise_solution(vrp_best_sol, px, py, depot, "Optimal Solution")

    # Executing and visualizing the nearest neighbour VRP heuristic.
    # Uncomment it to do your assignment!

    nnh_solution = nearest_neighbour_heuristic(px, py, demand, capacity, depot)
    nnh_distance = utility.calculate_total_distance(nnh_solution, px, py, depot)
    print("Nearest Neighbour VRP Heuristic Distance:", nnh_distance)
    utility.visualise_solution(nnh_solution, px, py, depot, "Nearest Neighbour Heuristic")

    # Executing and visualizing the saving VRP heuristic.
    # Uncomment it to do your assignment!
    
    sh_solution = savings_heuristic(px, py, demand, capacity, depot)
    sh_distance = utility.calculate_total_distance(sh_solution, px, py, depot)
    print("Saving VRP Heuristic Distance:", sh_distance)
    utility.visualise_solution(sh_solution, px, py, depot, "Savings Heuristic")

def nearest_neighbour_heuristic(px, py, demand, capacity, depot):
    """
    Algorithm for the nearest neighbour heuristic to generate VRP solutions.

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param demand: List of each node's demand.
    :param capacity: Vehicle carrying capacity.
    :param depot: Depot.
    :return: List of vehicle routes (tours).
    """
    
    solution = [] #initialise a solution -> starting from depot
    remaining_routes = list(range(len(px))) #list of routes
    remaining_routes.remove(depot) #with depot removed
    
    while remaining_routes: #while routes remaining
        route = [] #initialise route list
        current_route = depot #starting from depot
        current_capacity = capacity #initalise current_capacity
        
        while True: #while true
            min_distance = float('inf')
            next_route = None
            
            for i in remaining_routes: #for route in remaining_routes
                if demand[i] <= current_capacity: #if demand of route does not exceed capacity
                    distance = utility.calculate_euclidean_distance(px, py, current_route, i) #calculate distance
                    if distance < min_distance: #if distance is less than min_distance
                        min_distance = distance #update min_distance -> loops to find nearest route
                        next_route = i #update next_route
            
            if next_route is None: #if no route found -> break
                break
            
            current_capacity -= demand[next_route] #update current_capacity
            route.append(next_route) #add route to route list
            remaining_routes.remove(next_route) #remove route from remaining_routes
            current_route = next_route #current_route to look at next route

        solution.append(route) #add route to solution
    
    #print routes
    for i, route in enumerate(solution):
        print("ROUTE", i + 1, ": ", route)
    
    return solution

def savings_heuristic(px, py, demand, capacity, depot):
    """
    Algorithm for Implementing the savings heuristic to generate VRP solutions.

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param demand: List of each node's demand.
    :param capacity: Vehicle carrying capacity.
    :param depot: Depot.
    :return: List of vehicle routes (tours).
    """
    
    savings = [] #initialise savings list
    
    routes = [] #initialise routes
    for i in range(len(px)):
        if i != depot:
            routes.append([depot, i, depot]) #(1, vi, 1) for each node vi except depot
            
    remaining_routes = list(range(len(px))) #list of routes
    remaining_routes.remove(depot) #with depot removed

    for i in remaining_routes: #loop through remaining routes
        for j in remaining_routes:
            if i != j: #if route i is not equal to route j -> calculate savings
                L1 = utility.calculate_euclidean_distance(px, py, i, depot) #L(vi, 1)
                L2 = utility.calculate_euclidean_distance(px, py, depot, j) #L(1, vj)
                L3 = utility.calculate_euclidean_distance(px, py, i, j) #L(vi, vj)
                distance = L1 + L2 - L3 #L(vi, 1) + L(1, vj) - L(vi, vj)
                savings.append((i, j, distance)) #savings(vi, vj, distance)
    
    savings = sorted(savings, key=lambda x: x[2], reverse=True) #sort savings descending order
    
    for i, j, distance in savings: #loop through savings
        route1 = None #initialise route 1 and 2
        route2 = None
        for rt in routes:
            if i in rt:
                route1 = rt #if i in route -> route1 = rt
            if j in rt:
                route2 = rt #if j in route -> route2 = rt
            if route1 is not None and route2 is not None: #if both routes are found -> break
                break
       
        if route1 != route2 and route1 is not None and route2 is not None: 
            cost_i = 0 #initialise cost_i and cost_j
            cost_j = 0
            for rt in range(len(route1)): 
                cost_i += demand[route1[rt]] #find cost of route1 -> demand of route1
            for rt in range(len(route2)):
                cost_j += demand[route2[rt]] #find cost of route2 -> demand of route2
            if cost_i + cost_j <= capacity: #if merging route1 and route2 does not exceed capacity
                route = [] #initialise route
                if route1[-2] == i and route2[1] == j: #last val route1 -> i, first val route2 -> j
                    route = route1[:-1] + route2[1:] #merge last non-depot val of route1 and first non-depot val of route2
                elif route2[-2] == j and route1[1] == i: #last val route2 -> j, first val route1 -> i
                    route = route2[:-1] + route1[1:] #merge last non-depot val of route2 and first non-depot val of route1
                if route: #if route is not empty
                    routes.remove(route1) #remove route1 and route2
                    routes.remove(route2)
                    routes.append(route) #add merged route to routes
    
    #print routes
    for i, route in enumerate(routes):
        print("Route", i + 1, ": ", route)
    
    return routes

if __name__ == '__main__':
    main()

