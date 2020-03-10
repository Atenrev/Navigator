# This file contains all the required routines to make an A* search algorithm.
#
__authors__ = '1533031'
__group__ = 'DM.12'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Grau en Enginyeria Informatica
# Curs 2016- 2017
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import os
import math
import copy


class CoolerPath(Path):
    def __init__(self, route):
        self.transfers = 0
        self.g = 0
        self.h = 0
        self.f = 0

        if type(route) is list:
            self.route = route
        elif type(route) is CoolerPath:
            self.route = route.route.copy()
            self.transfers = route.transfers
            self.g = route.g
            self.h = route.h
            self.f = route.f
        elif type(route) is Path:
            self.route = route.route.copy()
            self.g = route.g
            self.h = route.h
            self.f = route.f
        else:
            self.route = [route]

        self.head = self.route[0]
        self.last = self.route[-1]

        if len(self.route) >= 2:
            self.penultimate = self.route[-2]

    def update_transfers(self, v):
        self.transfers += v


def get_cost(x): return x.g


def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """

    expanded = []

    for i in map.connections[path.last]:
        new_path = CoolerPath(path)
        new_path.add_route(i)

        if map.stations[new_path.last]["name"] == map.stations[new_path.penultimate]["name"]:
            new_path.update_transfers(1)

        expanded.append(new_path)

    return expanded


def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """

    uncycled = []

    for path in path_list:
        route = path.route
        if len(route) == len(set(route)):
            uncycled.append(path)

    return uncycled


def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """

    return list(expand_paths + list_of_path)


def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """

    paths = [CoolerPath(origin_id)]

    while paths and paths[0].last != destination_id:
        expanded = expand(paths[0], map)
        uncycled = remove_cycles(expanded)
        paths.pop(0)
        paths = insert_depth_first_search(uncycled, paths)

    if paths:
        return paths[0]
    else:
        return []


def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """

    return list(list_of_path + expand_paths)


def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """

    paths = [CoolerPath(origin_id)]

    while paths and paths[0].last != destination_id:
        expanded = expand(paths[0], map)
        uncycled = remove_cycles(expanded)
        paths.pop(0)
        paths = insert_breadth_first_search(uncycled, paths)

    if paths:
        return paths[0]
    else:
        return []


def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """

    if type_preference == 0:
        # El cost es calcula en canviar d'estació o sense comptar transbordaments.
        for path in expand_paths:
            path.update_g(1)

    elif type_preference == 1:
        for path in expand_paths:
            g = map.connections[path.penultimate][path.last]
            path.update_g(g)

    elif type_preference == 2:
        for path in expand_paths:
            if map.stations[path.last]["name"] == map.stations[path.penultimate]["name"]:
                velocity = 0
            else:
                velocity = map.stations[path.last]["velocity"]
            seconds = map.connections[path.penultimate][path.last]
            g = velocity * seconds
            path.update_g(g)

    elif type_preference == 3:
        for path in expand_paths:
            path.g = path.transfers
            # if map.stations[path.last]["name"] == map.stations[path.penultimate]["name"]:
            #     path.update_g(1)

    return expand_paths


def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """

    with_cost = list(expand_paths + list_of_path)
    with_cost.sort(key=get_cost)
    return with_cost


def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """

    paths = [CoolerPath(origin_id)]

    while paths and paths[0].last != destination_id:
        expanded = expand(paths[0], map)
        uncycled = remove_cycles(expanded)
        paths.pop(0)
        with_cost = calculate_cost(uncycled, map, type_preference)
        paths = insert_cost(with_cost, paths)

    if paths:
        return paths[0]
    else:
        return []


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    if type_preference == 0:
        # Què coi és l'adjacència?
        for path in expand_paths:
            path.update_h(uniform_cost_search(
                path.last, destination_id, map, type_preference).g)

    elif type_preference == 1:
        # En funció de què la calculem?
        for path in expand_paths:
            path.update_h(uniform_cost_search(
                path.last, destination_id, map, type_preference).g)

    elif type_preference == 2:
        # L'única que sé que és correcta
        for path in expand_paths:
            last_station = map.stations[path.last]
            destination = map.stations[destination_id]
            coord_last = [last_station["x"], last_station["y"]]
            coord_destination = [
                destination["x"], destination["y"]]

            h = euclidean_dist(coord_destination, coord_last)
            path.update_h(h)

    elif type_preference == 3:
        for path in expand_paths:
            # Which criteria shall we follow?
            path.update_h(uniform_cost_search(
                path.last, destination_id, map, 1).transfers)

    return expand_paths


def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    pass


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g in this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
    """
    pass


def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    pass


def coord2station(coord, map):
    """
        From coordinates, it searches the closest station.
        Format of the parameter is:
        Args:
            coord (list):  Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            possible_origins (list): List of the Indexes of stations, which corresponds to the closest station
    """

    close_stations = []
    min_dist = INF

    for id, station in map.stations.items():
        station_xy = [station["x"], station["y"]]
        dist = euclidean_dist(station_xy, coord)

        if dist < min_dist:
            close_stations = [id]
            min_dist = dist
        elif dist == min_dist:
            close_stations.append(id)

    return close_stations


def Astar(origin_coor, dest_coor, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (list): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    pass
