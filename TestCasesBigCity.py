import unittest
from SearchAlgorithm import *
from SubwayMap import *
from utils import *
import os
import random


class TestCases(unittest.TestCase):
    ROOT_FOLDER = 'CityInformation/Lyon_bigCity/'

    def setUp(self):
        map = read_station_information(
            os.path.join(self.ROOT_FOLDER, 'Stations.txt'))
        connections = read_cost_table(
            os.path.join(self.ROOT_FOLDER, 'Time.txt'))
        map.add_connection(connections)

        infoVelocity_clean = read_information(
            os.path.join(self.ROOT_FOLDER, 'InfoVelocity.txt'))
        map.add_velocity(infoVelocity_clean)

        self.map = map


    def test_comparative(self):
        route = uniform_cost_search(1, 90, self.map, 0)
        optimal_path = Astar([213, 506], [644, 680], self.map, 0)
        self.assertEqual(route, optimal_path)

        route = uniform_cost_search(8, 30, self.map, 1)
        optimal_path = Astar([410, 182], [85, 225], self.map, 1)
        self.assertEqual(route, optimal_path)

        route = uniform_cost_search(60, 17, self.map, 2)
        optimal_path = Astar([293, 485], [373, 331], self.map, 2)
        self.assertEqual(route, optimal_path)

        route = uniform_cost_search(40, 124, self.map, 2)
        optimal_path = Astar([510, 560], [115, 450], self.map, 2)
        self.assertEqual(route, optimal_path)


if __name__ == "__main__":
    unittest.main()
