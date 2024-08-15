import numpy as np
import random
import itertools
import pulp
from collections import deque


def calculate_transfer_time(X, T):
    """
    Calculate the total transfer time given the layer-device assignment matrix and transfer time matrix.

    Args:
        X (numpy.ndarray): Layer-device assignment matrix.
        T (numpy.ndarray): Transfer time matrix between devices.

    Returns:
        float: The total transfer time.
    """
    X_shifted = np.roll(X, shift=-1, axis=0)
    X_shifted[-1, :] = 0  # Ensure the last row is all zeros
    M = np.dot(X.T, X_shifted)
    transfer_matrix = M * T
    return np.sum(transfer_matrix)


def calculate_computation_time(X, C):
    """
    Calculate the total computation time given the layer-device assignment matrix and computation time matrix.

    Args:
        X (numpy.ndarray): Layer-device assignment matrix.
        C (numpy.ndarray): Computation time matrix for each layer on each device.

    Returns:
        float: The maximum computation time across all devices.
    """
    comp_time_per_device = np.sum(X * C, axis=0)
    return np.max(comp_time_per_device)


def total_time(X, T, C):
    transfer_time = calculate_transfer_time(X, T)
    computation_time = calculate_computation_time(X, C)
    return transfer_time + computation_time



def greedy_partitioning(num_layers, num_devices, T, C):
    """
    Greedy algorithm to partition layers across devices to minimize total transfer and computation time.

    Args:
        num_layers (int): Number of layers to be partitioned.
        num_devices (int): Number of available devices.
        T (numpy.ndarray): Transfer time matrix between devices.
        C (numpy.ndarray): Computation time matrix for each layer on each device.

    Returns:
        numpy.ndarray: Final layer-device assignment matrix.
        float: Final total transfer time.
        float: Final maximum computation time.
    """
    # Initialize the layer-device assignment matrix
    X = np.zeros((num_layers, num_devices))
    
    # Greedy algorithm for layer assignment
    for layer in range(num_layers):
        best_device = None
        best_total_time = float('inf')
        
        # Try assigning the layer to each device and calculate the total time
        for device in range(num_devices):
            # Temporarily assign the layer to the device
            temp_X = X.copy()
            temp_X[layer, :] = 0  # Reset current assignment
            temp_X[layer, device] = 1
            
            # Calculate total time (transfer + computation)
            transfer_time = calculate_transfer_time(temp_X, T)
            computation_time = calculate_computation_time(temp_X, C)
            total_time = transfer_time + computation_time
            
            # Choose the assignment that minimizes the total time
            if total_time < best_total_time:
                best_total_time = total_time
                best_device = device
        
        # Assign the layer to the best device found
        X[layer, best_device] = 1
    
    # Calculate final times
    final_transfer_time = calculate_transfer_time(X, T)
    final_computation_time = calculate_computation_time(X, C)
    
    return X, final_transfer_time, final_computation_time



def simulated_annealing(num_layers, num_devices, T, C, initial_temp=1000, cooling_rate=0.995, min_temp=1):

    """
    Simulated annealing algorithm to partition layers across devices to minimize total transfer and computation time.

    Args:
        num_layers (int): Number of layers to be partitioned.
        num_devices (int): Number of available devices.
        T (numpy.ndarray): Transfer time matrix between devices.
        C (numpy.ndarray): Computation time matrix for each layer on each device.
        initial_temp (float): Initial temperature for simulated annealing.
        cooling_rate (float): Rate at which the temperature decreases.
        min_temp (float): Minimum temperature to stop the algorithm.

    Returns:
        numpy.ndarray: Final layer-device assignment matrix.
        float: Final total time (transfer + computation time).
    """
    # Initialize with a random solution
    current_X = np.zeros((num_layers, num_devices))
    for layer in range(num_layers):
        device = random.randint(0, num_devices - 1)
        current_X[layer, device] = 1

    current_cost = total_time(current_X, T, C)
    best_X = current_X.copy()
    best_cost = current_cost
    
    temperature = initial_temp

    # Simulated annealing loop
    while temperature > min_temp:
        # Randomly choose a layer and change its device assignment
        new_X = current_X.copy()
        layer = random.randint(0, num_layers - 1)
        current_device = np.argmax(new_X[layer])
        new_device = random.choice([i for i in range(num_devices) if i != current_device])
        new_X[layer, current_device] = 0
        new_X[layer, new_device] = 1
        
        # Calculate the new cost
        new_cost = total_time(new_X, T, C)
        
        # Determine if the new solution should be accepted
        if new_cost < current_cost or random.random() < np.exp((current_cost - new_cost) / temperature):
            current_X = new_X
            current_cost = new_cost
        
        # Update the best solution found
        if new_cost < best_cost:
            best_X = new_X
            best_cost = new_cost
        
        # Decrease the temperature
        temperature *= cooling_rate

    return best_X, best_cost











def generate_individual(num_layers, num_devices):
    """
    Generate a random individual (solution) where each layer is assigned to a random device.
    """
    X = np.zeros((num_layers, num_devices))
    for layer in range(num_layers):
        device = random.randint(0, num_devices - 1)
        X[layer, device] = 1
    return X

def crossover(parent1, parent2):
    """
    Perform crossover between two parents to produce a child solution.
    """
    num_layers = parent1.shape[0]
    crossover_point = random.randint(1, num_layers - 2)
    child = np.vstack((parent1[:crossover_point], parent2[crossover_point:]))
    return child

def mutate(X, num_devices, mutation_rate=0.01):
    """
    Apply mutation to a solution by randomly changing the device assignment for some layers.
    """
    num_layers = X.shape[0]
    for layer in range(num_layers):
        if random.random() < mutation_rate:
            current_device = np.argmax(X[layer])
            new_device = random.choice([i for i in range(num_devices) if i != current_device])
            X[layer, current_device] = 0
            X[layer, new_device] = 1
    return X

def select_parents(population, fitness_scores, num_parents):
    """
    Select parents based on fitness scores using a roulette wheel selection mechanism.
    Ensure that the number of parents selected is even.
    """
    fitness_sum = sum(fitness_scores)
    selection_probs = [f / fitness_sum for f in fitness_scores]
    if num_parents % 2 != 0:
        num_parents += 1  # Ensure an even number of parents
    selected_parents = random.choices(population, weights=selection_probs, k=num_parents)
    return selected_parents

def genetic_algorithm(num_layers, num_devices, T, C, population_size=50, num_generations=100, mutation_rate=0.01):
    """
    Genetic algorithm to partition layers across devices to minimize total transfer and computation time.

    Args:
        num_layers (int): Number of layers to be partitioned.
        num_devices (int): Number of available devices.
        T (numpy.ndarray): Transfer time matrix between devices.
        C (numpy.ndarray): Computation time matrix for each layer on each device.
        population_size (int): Number of individuals in the population.
        num_generations (int): Number of generations to evolve.
        mutation_rate (float): Probability of mutating a layer's assignment.

    Returns:
        numpy.ndarray: Final layer-device assignment matrix.
        float: Final total time (transfer + computation time).
    """
    # Initialize population
    population = [generate_individual(num_layers, num_devices) for _ in range(population_size)]
    
    # Evolve over generations
    for generation in range(num_generations):
        # Calculate fitness scores (inverse of total time)
        fitness_scores = [1 / total_time(individual, T, C) for individual in population]

        # Select parents
        parents = select_parents(population, fitness_scores, population_size // 2)

        # Create the next generation
        next_generation = []
        for i in range(0, len(parents), 2):
            parent1, parent2 = parents[i], parents[i+1]
            child = crossover(parent1, parent2)
            child = mutate(child, num_devices, mutation_rate)
            next_generation.append(child)
        
        # Add some of the best current generation individuals to preserve elitism
        population = next_generation + parents[:len(next_generation)]

    # Find the best individual in the final population
    final_fitness_scores = [1 / total_time(individual, T, C) for individual in population]
    best_index = np.argmax(final_fitness_scores)
    best_individual = population[best_index]
    best_cost = total_time(best_individual, T, C)
    
    return best_individual, best_cost










def grid_search(num_layers, num_devices, T, C):

    """
    Grid search to partition layers across devices to minimize total transfer and computation time.

    Args:
        num_layers (int): Number of layers to be partitioned.
        num_devices (int): Number of available devices.
        T (numpy.ndarray): Transfer time matrix between devices.
        C (numpy.ndarray): Computation time matrix for each layer on each device.

    Returns:
        numpy.ndarray: Best layer-device assignment matrix.
        float: Best total time (transfer + computation time).
    """
    # Generate all possible assignments of layers to devices
    possible_assignments = list(itertools.product(range(num_devices), repeat=num_layers))
    
    best_X = None
    best_total_time = float('inf')
    
    # Iterate over all possible assignments
    for assignment in possible_assignments:
        # Create the layer-device assignment matrix X based on the assignment tuple
        X = np.zeros((num_layers, num_devices))
        for layer, device in enumerate(assignment):
            X[layer, device] = 1
        
        # Calculate the total time (transfer + computation)
        transfer_time = calculate_transfer_time(X, T)
        computation_time = calculate_computation_time(X, C)
        total_time = transfer_time + computation_time
        
        # Update the best solution if the current one is better
        if total_time < best_total_time:
            best_total_time = total_time
            best_X = X
    
    return best_X, best_total_time










def pso_partitioning(num_layers, num_devices, T, C, num_particles=30, max_iterations=100, w=0.5, c1=1.5, c2=1.5):
    """
    Particle Swarm Optimization (PSO) to partition layers across devices to minimize total transfer and computation time.

    Args:
        num_layers (int): Number of layers to be partitioned.
        num_devices (int): Number of available devices.
        T (numpy.ndarray): Transfer time matrix between devices.
        C (numpy.ndarray): Computation time matrix for each layer on each device.
        num_particles (int): Number of particles in the swarm.
        max_iterations (int): Maximum number of iterations.
        w (float): Inertia weight to control the influence of previous velocities.
        c1 (float): Cognitive constant to control the influence of personal best positions.
        c2 (float): Social constant to control the influence of the global best position.

    Returns:
        numpy.ndarray: Best layer-device assignment matrix.
        float: Best total time (transfer + computation time).
    """
    # Initialize particles with random assignments
    particles = [generate_individual(num_layers, num_devices) for _ in range(num_particles)]
    velocities = [np.zeros((num_layers, num_devices)) for _ in range(num_particles)]
    
    personal_best_positions = particles.copy()
    personal_best_scores = [total_time(p, T, C) for p in particles]
    
    global_best_position = personal_best_positions[np.argmin(personal_best_scores)]
    global_best_score = min(personal_best_scores)
    
    # PSO loop
    for iteration in range(max_iterations):
        for i in range(num_particles):
            # Update particle velocity
            r1 = np.random.rand(num_layers, num_devices)
            r2 = np.random.rand(num_layers, num_devices)
            velocities[i] = (w * velocities[i] + 
                             c1 * r1 * (personal_best_positions[i] - particles[i]) + 
                             c2 * r2 * (global_best_position - particles[i]))
            
            # Update particle position (assignment matrix)
            particles[i] += velocities[i]
            
            # Apply a discrete assignment (convert to one-hot matrix)
            for layer in range(num_layers):
                device = np.argmax(particles[i][layer])
                particles[i][layer] = np.zeros(num_devices)
                particles[i][layer][device] = 1
            
            # Evaluate particle's fitness
            current_score = total_time(particles[i], T, C)
            
            # Update personal best
            if current_score < personal_best_scores[i]:
                personal_best_positions[i] = particles[i].copy()
                personal_best_scores[i] = current_score
            
            # Update global best
            if current_score < global_best_score:
                global_best_position = particles[i].copy()
                global_best_score = current_score
    
    return global_best_position, global_best_score



def aco_partitioning(num_layers, num_devices, T, C, num_ants=30, max_iterations=100, alpha=1.0, beta=2.0, evaporation_rate=0.5, pheromone_init=1.0):
    """
    Ant Colony Optimization (ACO) to partition layers across devices to minimize total transfer and computation time.

    Args:
        num_layers (int): Number of layers to be partitioned.
        num_devices (int): Number of available devices.
        T (numpy.ndarray): Transfer time matrix between devices.
        C (numpy.ndarray): Computation time matrix for each layer on each device.
        num_ants (int): Number of ants in the colony.
        max_iterations (int): Maximum number of iterations.
        alpha (float): Influence of pheromone trails.
        beta (float): Influence of heuristic information (inverse of total time).
        evaporation_rate (float): Rate at which pheromone evaporates.
        pheromone_init (float): Initial amount of pheromone on each edge.

    Returns:
        numpy.ndarray: Best layer-device assignment matrix.
        float: Best total time (transfer + computation time).
    """
    # Initialize pheromone matrix
    pheromone = np.full((num_layers, num_devices), pheromone_init)

    best_solution = None
    best_score = float('inf')

    # ACO loop
    for iteration in range(max_iterations):
        all_solutions = []
        all_scores = []

        # Each ant constructs a solution
        for ant in range(num_ants):
            solution = np.zeros((num_layers, num_devices))

            for layer in range(num_layers):
                probabilities = []
                for device in range(num_devices):
                    # Calculate probability for each device based on pheromone and heuristic (inverse of computation time)
                    heuristic_value = 1.0 / (C[layer, device] + 1e-6)  # Avoid division by zero
                    prob = (pheromone[layer, device] ** alpha) * (heuristic_value ** beta)
                    probabilities.append(prob)

                # Normalize probabilities
                probabilities = np.array(probabilities) / np.sum(probabilities)
                
                # Choose a device for the current layer based on probabilities
                device = np.random.choice(range(num_devices), p=probabilities)
                solution[layer, device] = 1
            
            # Calculate the total time (transfer + computation)
            score = total_time(solution, T, C)
            all_solutions.append(solution)
            all_scores.append(score)

            # Update best solution
            if score < best_score:
                best_solution = solution
                best_score = score

        # Update pheromones (evaporation + deposition)
        pheromone *= (1 - evaporation_rate)  # Evaporation
        for solution, score in zip(all_solutions, all_scores):
            pheromone += solution / score  # Deposit pheromone inversely proportional to the score

    return best_solution, best_score





def branch_and_bound(num_layers, num_devices, T, C):
    """
    Branch and Bound algorithm to partition layers across devices to minimize total transfer and computation time.

    Args:
        num_layers (int): Number of layers to be partitioned.
        num_devices (int): Number of available devices.
        T (numpy.ndarray): Transfer time matrix between devices.
        C (numpy.ndarray): Computation time matrix for each layer on each device.

    Returns:
        numpy.ndarray: Best layer-device assignment matrix.
        float: Best total time (transfer + computation time).
    """
    # Initialize best solution
    best_solution = None
    best_cost = float('inf')

    # Stack to store the branches
    stack = [(0, np.zeros((num_layers, num_devices)), 0)]  # (layer index, solution matrix, current cost)

    while stack:
        layer_index, current_solution, current_cost = stack.pop()

        # If all layers are assigned, calculate the final total time
        if layer_index == num_layers:
            total_time = calculate_transfer_time(current_solution, T) + calculate_computation_time(current_solution, C)
            if total_time < best_cost:
                best_cost = total_time
                best_solution = current_solution.copy()
            continue

        # Explore all possible assignments for the current layer
        for device in range(num_devices):
            # Create a new solution by assigning the current layer to the current device
            new_solution = current_solution.copy()
            new_solution[layer_index, :] = 0  # Reset current layer assignments
            new_solution[layer_index, device] = 1

            # Estimate the lower bound for this partial solution (using a heuristic)
            lower_bound = current_cost + C[layer_index, device]  # Adding the computation cost for this layer
            if lower_bound >= best_cost:
                continue  # Prune this branch if the lower bound is worse than the best known solution

            # Push the new solution onto the stack for further exploration
            stack.append((layer_index + 1, new_solution, lower_bound))

    return best_solution, best_cost






def hill_climbing(num_layers, num_devices, T, C, max_iterations=1000):
    """
    Hill Climbing algorithm to partition layers across devices to minimize total transfer and computation time.

    Args:
        num_layers (int): Number of layers to be partitioned.
        num_devices (int): Number of available devices.
        T (numpy.ndarray): Transfer time matrix between devices.
        C (numpy.ndarray): Computation time matrix for each layer on each device.
        max_iterations (int): Maximum number of iterations for the algorithm.

    Returns:
        numpy.ndarray: Best layer-device assignment matrix.
        float: Best total time (transfer + computation time).
    """
    # Initialize with a random solution
    current_solution = generate_individual(num_layers, num_devices)
    current_cost = total_time(current_solution, T, C)

    best_solution = current_solution.copy()
    best_cost = current_cost

    for iteration in range(max_iterations):
        # Generate a neighboring solution by changing the assignment of one layer
        new_solution = current_solution.copy()
        layer_to_change = np.random.randint(0, num_layers)
        current_device = np.argmax(new_solution[layer_to_change])
        new_device = np.random.choice([i for i in range(num_devices) if i != current_device])
        new_solution[layer_to_change, current_device] = 0
        new_solution[layer_to_change, new_device] = 1

        # Calculate the new cost
        new_cost = total_time(new_solution, T, C)

        # If the new solution is better, update the current solution
        if new_cost < current_cost:
            current_solution = new_solution
            current_cost = new_cost

            # Update the best solution found so far
            if new_cost < best_cost:
                best_solution = new_solution
                best_cost = new_cost

    return best_solution, best_cost






def random_search(num_layers, num_devices, T, C, num_trials=1000):
    """
    Random Search algorithm to partition layers across devices to minimize total transfer and computation time.

    Args:
        num_layers (int): Number of layers to be partitioned.
        num_devices (int): Number of available devices.
        T (numpy.ndarray): Transfer time matrix between devices.
        C (numpy.ndarray): Computation time matrix for each layer on each device.
        num_trials (int): Number of random solutions to try.

    Returns:
        numpy.ndarray: Best layer-device assignment matrix.
        float: Best total time (transfer + computation time).
    """
    best_solution = None
    best_cost = float('inf')

    for _ in range(num_trials):
        # Generate a random solution
        solution = generate_individual(num_layers, num_devices)
        cost = total_time(solution, T, C)
        
        # Update the best solution if the current one is better
        if cost < best_cost:
            best_solution = solution
            best_cost = cost

    return best_solution, best_cost








def milp_partitioning(num_layers, num_devices, T, C):
    """
    Mixed-Integer Linear Programming (MILP) to partition layers across devices to minimize total transfer and computation time.

    Args:
        num_layers (int): Number of layers to be partitioned.
        num_devices (int): Number of available devices.
        T (numpy.ndarray): Transfer time matrix between devices.
        C (numpy.ndarray): Computation time matrix for each layer on each device.

    Returns:
        numpy.ndarray: Best layer-device assignment matrix.
        float: Best total time (transfer + computation time).
    """
    # Create the MILP problem
    prob = pulp.LpProblem("Layer_Device_Partitioning", pulp.LpMinimize)

    # Decision variables: X[i, j] is 1 if layer i is assigned to device j, otherwise 0
    X = pulp.LpVariable.dicts("X", (range(num_layers), range(num_devices)), cat="Binary")

    # Auxiliary variables for transfer times between consecutive layers
    Transfer = pulp.LpVariable.dicts("Transfer", (range(num_layers - 1), range(num_devices), range(num_devices)), cat="Binary")

    # Objective function: Minimize the sum of computation and transfer times
    # Computation time: sum of C[i, j] * X[i, j]
    computation_time = pulp.lpSum(C[i][j] * X[i][j] for i in range(num_layers) for j in range(num_devices))

    # Transfer time: sum of T[k, j] * Transfer[i, k, j] for each consecutive layer
    transfer_time = pulp.lpSum(T[k][j] * Transfer[i][k][j] for i in range(num_layers - 1) for k in range(num_devices) for j in range(num_devices))

    # Objective: Minimize the total time (computation + transfer)
    prob += computation_time + transfer_time

    # Constraints: Each layer must be assigned to exactly one device
    for i in range(num_layers):
        prob += pulp.lpSum(X[i][j] for j in range(num_devices)) == 1

    # Constraints: Define transfer variables based on X
    for i in range(num_layers - 1):
        for k in range(num_devices):
            for j in range(num_devices):
                # Transfer[i, k, j] is 1 if layer i is on device k and layer i+1 is on device j
                prob += Transfer[i][k][j] <= X[i][k]
                prob += Transfer[i][k][j] <= X[i + 1][j]
                prob += Transfer[i][k][j] >= X[i][k] + X[i + 1][j] - 1

    # Solve the problem
    prob.solve()

    # Extract the solution
    best_solution = np.zeros((num_layers, num_devices))
    for i in range(num_layers):
        for j in range(num_devices):
            if pulp.value(X[i][j]) == 1:
                best_solution[i, j] = 1

    # Calculate the best total time
    best_cost = pulp.value(prob.objective)

    return best_solution, best_cost





def tabu_search(num_layers, num_devices, T, C, max_iterations=1000, tabu_tenure=10):
    """
    Tabu Search algorithm to partition layers across devices to minimize total transfer and computation time.

    Args:
        num_layers (int): Number of layers to be partitioned.
        num_devices (int): Number of available devices.
        T (numpy.ndarray): Transfer time matrix between devices.
        C (numpy.ndarray): Computation time matrix for each layer on each device.
        max_iterations (int): Maximum number of iterations for the search.
        tabu_tenure (int): Number of iterations a move remains tabu.

    Returns:
        numpy.ndarray: Best layer-device assignment matrix.
        float: Best total time (transfer + computation time).
    """
    # Initialize with a random solution
    current_solution = generate_individual(num_layers, num_devices)
    current_cost = total_time(current_solution, T, C)

    best_solution = current_solution.copy()
    best_cost = current_cost

    # Tabu list to store recent moves (layer, device assignment)
    tabu_list = deque(maxlen=tabu_tenure)

    for iteration in range(max_iterations):
        # Generate all possible neighboring solutions by changing one layer assignment
        neighbors = []
        for layer in range(num_layers):
            current_device = np.argmax(current_solution[layer])
            for device in range(num_devices):
                if device != current_device:
                    new_solution = current_solution.copy()
                    new_solution[layer, current_device] = 0
                    new_solution[layer, device] = 1
                    neighbors.append((new_solution, (layer, device)))

        # Find the best non-tabu neighbor
        best_neighbor_solution = None
        best_neighbor_cost = float('inf')
        best_move = None

        for neighbor_solution, move in neighbors:
            if move in tabu_list:
                continue  # Skip tabu moves

            neighbor_cost = total_time(neighbor_solution, T, C)
            if neighbor_cost < best_neighbor_cost:
                best_neighbor_solution = neighbor_solution
                best_neighbor_cost = neighbor_cost
                best_move = move

        # Update the current solution to the best non-tabu neighbor
        if best_neighbor_solution is not None:
            current_solution = best_neighbor_solution
            current_cost = best_neighbor_cost
            tabu_list.append(best_move)

            # Update the best solution found so far
            if current_cost < best_cost:
                best_solution = current_solution
                best_cost = current_cost

    return best_solution, best_cost













