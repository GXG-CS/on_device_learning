import sys
import os

# # Add the parent directory to sys.path
# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# print(f"Parent Directory being added to sys.path: {parent_dir}")
# sys.path.append(parent_dir)

# # Print sys.path to debug
# print("sys.path:", sys.path)

# # Check if the path exists and list the contents
# print(f"Contents of {parent_dir}: {os.listdir(parent_dir)}")

# # Attempt to import partitioning_utils and print its location
# try:
#     import partitioning_utils
#     print(f"partitioning_utils module found at: {partitioning_utils.__file__}")
# except ModuleNotFoundError:
#     print("partitioning_utils module not found")

# Proceed with the imports
from partitioning_utils.greedy import greedy_partitioning
from partitioning_utils.simulated_annealing import simulated_annealing
from partitioning_utils.genetic import genetic_algorithm
from partitioning_utils.grid import grid_search
from partitioning_utils.pso import pso_partitioning
from partitioning_utils.aco import aco_partitioning
from partitioning_utils.branch_bound import branch_and_bound
from partitioning_utils.hill_climbing import hill_climbing
from partitioning_utils.random_search import random_search
from partitioning_utils.milp import milp_partitioning
from partitioning_utils.tabu import tabu_search
