import numpy as np
import time
import tracemalloc  # For peak memory measurement

from partitioning_utils.greedy import greedy_partitioning
from partitioning_utils.simulated_annealing import simulated_annealing
from partitioning_utils.genetic import genetic_algorithm
from partitioning_utils.grid import grid_search
from partitioning_utils.pso import pso_partitioning
from partitioning_utils.aco import aco_partitioning
from partitioning_utils.branch_bound import branch_and_bound
from partitioning_utils.hill_climbing import hill_climbing
from partitioning_utils.random_search import random_search
from partitioning_utils.tabu import tabu_search

# Define number of devices and layers
num_devices = 5
num_layers = 6

# Randomly generate transfer time matrix T
np.random.seed(42)  # For reproducibility
T = np.random.randint(1, 10, size=(num_devices, num_devices))
np.fill_diagonal(T, 0)  # Set diagonal to zero (no transfer time within the same device)

# Randomly generate full dense computation time matrix C for each layer on each device
C = np.random.randint(1, 10, size=(num_layers, num_devices))

def run_algorithm(algorithm_name, algorithm_func, *args, **kwargs):
    print(f"Running {algorithm_name}...")

    # Start measuring time and memory
    start_time = time.time()
    tracemalloc.start()  # Start tracing memory allocations

    # Run the algorithm
    result = algorithm_func(*args, **kwargs)

    # End measuring time and memory
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()  # Stop tracing memory allocations
    elapsed_time = end_time - start_time
    peak_memory_used = peak / 1024  # Convert peak memory to KB

    # Handle result unpacking
    if len(result) == 2:  # Only best_X and best_cost returned
        best_X, best_cost = result
    elif len(result) == 3:  # best_X, transfer_time, and computation_time returned
        best_X, final_transfer_time, final_computation_time = result
        best_cost = final_transfer_time + final_computation_time
    
    # Print results
    print(f"{algorithm_name} Results:")
    print(f"Best Total Time (Transfer + Computation): {best_cost} units")
    print(f"Elapsed Time: {elapsed_time:.6f} seconds")
    print(f"Peak Memory Used: {peak_memory_used:.2f} KB")
    print("Final Layer-Device Assignment Matrix (X):")
    print(best_X)
    print("-" * 50)
    
    return best_X, best_cost, elapsed_time, peak_memory_used


print("Transfer Time Matrix (T):")
print(T)
print("Computation Time Matrix (C):")
print(C)
print("-" * 50)

# Run all methods and store the final result (X) from each
results = []
results.append(run_algorithm("Greedy Algorithm", greedy_partitioning, num_layers, num_devices, T, C))
results.append(run_algorithm("Simulated Annealing", simulated_annealing, num_layers, num_devices, T, C, initial_temp=1000, cooling_rate=0.995, min_temp=1))
results.append(run_algorithm("Genetic Algorithm", genetic_algorithm, num_layers, num_devices, T, C, population_size=50, num_generations=100, mutation_rate=0.01))
results.append(run_algorithm("Grid Search", grid_search, num_layers, num_devices, T, C))
results.append(run_algorithm("Particle Swarm Optimization (PSO)", pso_partitioning, num_layers, num_devices, T, C, num_particles=30, max_iterations=100, w=0.5, c1=1.5, c2=1.5))
results.append(run_algorithm("Ant Colony Optimization (ACO)", aco_partitioning, num_layers, num_devices, T, C, num_ants=30, max_iterations=100, alpha=1.0, beta=2.0, evaporation_rate=0.5, pheromone_init=1.0))
results.append(run_algorithm("Branch and Bound", branch_and_bound, num_layers, num_devices, T, C))
results.append(run_algorithm("Hill Climbing", hill_climbing, num_layers, num_devices, T, C, max_iterations=1000))
results.append(run_algorithm("Random Search", random_search, num_layers, num_devices, T, C, num_trials=1000))
# results.append(run_algorithm("MILP", milp_partitioning, num_layers, num_devices, T, C))
results.append(run_algorithm("Tabu Search", tabu_search, num_layers, num_devices, T, C, max_iterations=1000, tabu_tenure=10))







import csv

# Define the CSV file path
output_csv = "algorithm_results_summary.csv"

# List of algorithm names corresponding to the order of results
algorithm_names = [
    "Greedy Algorithm",
    "Simulated Annealing",
    "Genetic Algorithm",
    "Grid Search",
    "Particle Swarm Optimization (PSO)",
    "Ant Colony Optimization (ACO)",
    "Branch and Bound",
    "Hill Climbing",
    "Random Search",
    "Tabu Search"
]

# Define the header for the CSV file
header = ["Algorithm", "Best Total Time (Transfer + Computation)", "Elapsed Time (seconds)", "Peak Memory Used (KB)"]

# Write the results to the CSV file
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(header)
    
    # Write each algorithm's results
    for algorithm_name, result in zip(algorithm_names, results):
        best_cost, elapsed_time, peak_memory_used = result[1], result[2], result[3]
        writer.writerow([algorithm_name, best_cost, elapsed_time, peak_memory_used])

print(f"Results have been written to {output_csv}")

