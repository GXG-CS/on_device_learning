import numpy as np
import time
import tracemalloc
from partitioning_utils import greedy_partitioning, simulated_annealing, genetic_algorithm, grid_search, pso_partitioning, aco_partitioning, branch_and_bound, hill_climbing, random_search, milp_partitioning, tabu_search

# Define number of devices and layers
num_devices = 10
num_layers = 10  # For grid search, use a small number of layers due to exponential complexity

# Randomly generate transfer time matrix T
np.random.seed(42)  # For reproducibility
T = np.random.randint(1, 10, size=(num_devices, num_devices))
np.fill_diagonal(T, 0)  # Set diagonal to zero (no transfer time within the same device)

# Randomly generate full dense computation time matrix C for each layer on each device
C = np.random.randint(1, 10, size=(num_layers, num_devices))

# --------- Greedy Algorithm ---------
print("Running Greedy Algorithm...")
start_time = time.time()
tracemalloc.start()

X_greedy, final_transfer_time_greedy, final_computation_time_greedy = greedy_partitioning(num_layers, num_devices, T, C)

current, peak = tracemalloc.get_traced_memory()
end_time = time.time()
elapsed_time_greedy = end_time - start_time

tracemalloc.stop()

# Calculate final total time for Greedy Algorithm
final_total_time_greedy = final_transfer_time_greedy + final_computation_time_greedy

print("Greedy Algorithm Results:")
print("Final Layer-Device Assignment Matrix:")
print(X_greedy)
print(f"Final Transfer Time: {final_transfer_time_greedy} units")
print(f"Final Computation Time: {final_computation_time_greedy} units")
print(f"Final Total Time: {final_total_time_greedy} units")
print(f"Elapsed Time: {elapsed_time_greedy:.6f} seconds")
print(f"Current Memory Usage: {current / 1024:.2f} KB")
print(f"Peak Memory Usage: {peak / 1024:.2f} KB")
print("-" * 50)

# --------- Simulated Annealing Algorithm ---------
print("Running Simulated Annealing Algorithm...")
start_time = time.time()
tracemalloc.start()

X_annealing, final_time_annealing = simulated_annealing(num_layers, num_devices, T, C, initial_temp=1000, cooling_rate=0.995, min_temp=1)

current, peak = tracemalloc.get_traced_memory()
end_time = time.time()
elapsed_time_annealing = end_time - start_time

tracemalloc.stop()

print("Simulated Annealing Algorithm Results:")
print("Final Layer-Device Assignment Matrix:")
print(X_annealing)
print(f"Final Total Time (Transfer + Computation): {final_time_annealing} units")
print(f"Elapsed Time: {elapsed_time_annealing:.6f} seconds")
print(f"Current Memory Usage: {current / 1024:.2f} KB")
print(f"Peak Memory Usage: {peak / 1024:.2f} KB")
print("-" * 50)

# --------- Genetic Algorithm ---------
print("Running Genetic Algorithm...")
start_time = time.time()
tracemalloc.start()

best_X_genetic, best_cost_genetic = genetic_algorithm(num_layers, num_devices, T, C, population_size=50, num_generations=100, mutation_rate=0.01)

current, peak = tracemalloc.get_traced_memory()
end_time = time.time()
elapsed_time_genetic = end_time - start_time

tracemalloc.stop()

print("Genetic Algorithm Results:")
print("Best Layer-Device Assignment Matrix:")
print(best_X_genetic)
print(f"Final Total Time (Transfer + Computation): {best_cost_genetic} units")
print(f"Elapsed Time: {elapsed_time_genetic:.6f} seconds")
print(f"Current Memory Usage: {current / 1024:.2f} KB")
print(f"Peak Memory Usage: {peak / 1024:.2f} KB")
print("-" * 50)

# --------- Grid Search Algorithm ---------
print("Running Grid Search Algorithm...")
start_time = time.time()
tracemalloc.start()

best_X_grid, best_cost_grid = grid_search(num_layers, num_devices, T, C)

current, peak = tracemalloc.get_traced_memory()
end_time = time.time()
elapsed_time_grid = end_time - start_time

tracemalloc.stop()

print("Grid Search Algorithm Results:")
print("Best Layer-Device Assignment Matrix:")
print(best_X_grid)
print(f"Final Total Time (Transfer + Computation): {best_cost_grid} units")
print(f"Elapsed Time: {elapsed_time_grid:.6f} seconds")
print(f"Current Memory Usage: {current / 1024:.2f} KB")
print(f"Peak Memory Usage: {peak / 1024:.2f} KB")
print("-" * 50)

# --------- Particle Swarm Optimization (PSO) ---------
print("Running Particle Swarm Optimization (PSO) Algorithm...")
start_time = time.time()
tracemalloc.start()

best_X_pso, best_cost_pso = pso_partitioning(num_layers, num_devices, T, C, num_particles=30, max_iterations=100, w=0.5, c1=1.5, c2=1.5)

current, peak = tracemalloc.get_traced_memory()
end_time = time.time()
elapsed_time_pso = end_time - start_time

tracemalloc.stop()

print("Particle Swarm Optimization (PSO) Results:")
print("Best Layer-Device Assignment Matrix:")
print(best_X_pso)
print(f"Final Total Time (Transfer + Computation): {best_cost_pso} units")
print(f"Elapsed Time: {elapsed_time_pso:.6f} seconds")
print(f"Current Memory Usage: {current / 1024:.2f} KB")
print(f"Peak Memory Usage: {peak / 1024:.2f} KB")
print("-" * 50)

# --------- Ant Colony Optimization (ACO) ---------
# print("Running Ant Colony Optimization (ACO) Algorithm...")
# start_time = time.time()
# tracemalloc.start()

# best_X_aco, best_cost_aco = aco_partitioning(num_layers, num_devices, T, C, num_ants=30, max_iterations=100, alpha=1.0, beta=2.0, evaporation_rate=0.5, pheromone_init=1.0)

# current, peak = tracemalloc.get_traced_memory()
# end_time = time.time()
# elapsed_time_aco = end_time - start_time

# tracemalloc.stop()

# print("Ant Colony Optimization (ACO) Results:")
# print("Best Layer-Device Assignment Matrix:")
# print(best_X_aco)
# print(f"Final Total Time (Transfer + Computation): {best_cost_aco} units")
# print(f"Elapsed Time: {elapsed_time_aco:.6f} seconds")
# print(f"Current Memory Usage: {current / 1024:.2f} KB")
# print(f"Peak Memory Usage: {peak / 1024:.2f} KB")
# print("-" * 50)

# # --------- Branch and Bound Algorithm ---------
# print("Running Branch and Bound Algorithm...")
# start_time = time.time()
# tracemalloc.start()

# best_X_bnb, best_cost_bnb = branch_and_bound(num_layers, num_devices, T, C)

# current, peak = tracemalloc.get_traced_memory()
# end_time = time.time()
# elapsed_time_bnb = end_time - start_time

# tracemalloc.stop()

# print("Branch and Bound Algorithm Results:")
# print("Best Layer-Device Assignment Matrix:")
# print(best_X_bnb)
# print(f"Final Total Time (Transfer + Computation): {best_cost_bnb} units")
# print(f"Elapsed Time: {elapsed_time_bnb:.6f} seconds")
# print(f"Current Memory Usage: {current / 1024:.2f} KB")
# print(f"Peak Memory Usage: {peak / 1024:.2f} KB")
# print("-" * 50)




# --------- Hill Climbing Algorithm ---------
print("Running Hill Climbing Algorithm...")
start_time = time.time()
tracemalloc.start()

best_X_hill, best_cost_hill = hill_climbing(num_layers, num_devices, T, C, max_iterations=1000)

current, peak = tracemalloc.get_traced_memory()
end_time = time.time()
elapsed_time_hill = end_time - start_time

tracemalloc.stop()

print("Hill Climbing Algorithm Results:")
print("Best Layer-Device Assignment Matrix:")
print(best_X_hill)
print(f"Final Total Time (Transfer + Computation): {best_cost_hill} units")
print(f"Elapsed Time: {elapsed_time_hill:.6f} seconds")
print(f"Current Memory Usage: {current / 1024:.2f} KB")
print(f"Peak Memory Usage: {peak / 1024:.2f} KB")
print("-" * 50)



# --------- Random Search Algorithm ---------
print("Running Random Search Algorithm...")
start_time = time.time()

best_X_random, best_cost_random = random_search(num_layers, num_devices, T, C, num_trials=1000)

end_time = time.time()
elapsed_time_random = end_time - start_time

print("Random Search Results:")
print(f"Best Total Time (Transfer + Computation): {best_cost_random} units")
print(f"Elapsed Time: {elapsed_time_random:.6f} seconds")


# --------- MILP Algorithm ---------
# print("Running MILP Algorithm...")
# start_time = time.time()

# best_X_milp, best_cost_milp = milp_partitioning(num_layers, num_devices, T, C)

# end_time = time.time()
# elapsed_time_milp = end_time - start_time

# print("MILP Results:")
# print(f"Best Total Time (Transfer + Computation): {best_cost_milp} units")
# print(f"Elapsed Time: {elapsed_time_milp:.6f} seconds")



# --------- Tabu Search Algorithm ---------
print("Running Tabu Search Algorithm...")
start_time = time.time()

best_X_tabu, best_cost_tabu = tabu_search(num_layers, num_devices, T, C, max_iterations=1000, tabu_tenure=10)

end_time = time.time()
elapsed_time_tabu = end_time - start_time

print("Tabu Search Results:")
print(f"Best Total Time (Transfer + Computation): {best_cost_tabu} units")
print(f"Elapsed Time: {elapsed_time_tabu:.6f} seconds")


# --------- Summary ---------
print("Summary of Results:")
print(f"Greedy Algorithm: Final Total Time = {final_total_time_greedy}, Elapsed Time = {elapsed_time_greedy:.6f} seconds")
print(f"Simulated Annealing: Final Total Time = {final_time_annealing}, Elapsed Time = {elapsed_time_annealing:.6f} seconds")
print(f"Genetic Algorithm: Final Total Time = {best_cost_genetic}, Elapsed Time = {elapsed_time_genetic:.6f} seconds")
print(f"Grid Search: Final Total Time = {best_cost_grid}, Elapsed Time = {elapsed_time_grid:.6f} seconds")
print(f"Particle Swarm Optimization (PSO): Final Total Time = {best_cost_pso}, Elapsed Time = {elapsed_time_pso:.6f} seconds")
# print(f"Ant Colony Optimization (ACO): Final Total Time = {best_cost_aco}, Elapsed Time = {elapsed_time_aco:.6f} seconds")
# print(f"Branch and Bound: Final Total Time = {best_cost_bnb}, Elapsed Time = {elapsed_time_bnb:.6f} seconds")
print(f"Hill Climbing: Final Total Time = {best_cost_hill}, Elapsed Time = {elapsed_time_hill:.6f} seconds")
print(f"Random Search: Best Total Time = {best_cost_random}, Elapsed Time = {elapsed_time_random:.6f} seconds")
# print(f"MILP: Best Total Time = {best_cost_milp}, Elapsed Time = {elapsed_time_milp:.6f} seconds")
print(f"Tabu Search: Best Total Time = {best_cost_tabu}, Elapsed Time = {elapsed_time_tabu:.6f} seconds")

