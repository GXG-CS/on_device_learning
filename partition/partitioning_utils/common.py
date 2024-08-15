import numpy as np

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
    """
    Calculate the total time (transfer + computation) given the layer-device assignment matrix.

    Args:
        X (numpy.ndarray): Layer-device assignment matrix.
        T (numpy.ndarray): Transfer time matrix between devices.
        C (numpy.ndarray): Computation time matrix for each layer on each device.

    Returns:
        float: The total time (transfer + computation time).
    """
    transfer_time = calculate_transfer_time(X, T)
    computation_time = calculate_computation_time(X, C)
    return transfer_time + computation_time

def generate_individual(num_layers, num_devices):
    """
    Generate a random individual (solution) where each layer is assigned to a random device.

    Args:
        num_layers (int): Number of layers.
        num_devices (int): Number of available devices.

    Returns:
        numpy.ndarray: A random layer-device assignment matrix.
    """
    X = np.zeros((num_layers, num_devices))
    for layer in range(num_layers):
        device = np.random.randint(0, num_devices)
        X[layer, device] = 1
    return X

def crossover(parent1, parent2):
    """
    Perform crossover between two parents to produce a child solution.

    Args:
        parent1 (numpy.ndarray): First parent solution.
        parent2 (numpy.ndarray): Second parent solution.

    Returns:
        numpy.ndarray: The child solution resulting from crossover.
    """
    num_layers = parent1.shape[0]
    crossover_point = np.random.randint(1, num_layers - 1)
    child = np.vstack((parent1[:crossover_point], parent2[crossover_point:]))
    return child

def mutate(X, num_devices, mutation_rate=0.01):
    """
    Apply mutation to a solution by randomly changing the device assignment for some layers.

    Args:
        X (numpy.ndarray): Layer-device assignment matrix.
        num_devices (int): Number of available devices.
        mutation_rate (float): Probability of mutating a layer's assignment.

    Returns:
        numpy.ndarray: The mutated layer-device assignment matrix.
    """
    num_layers = X.shape[0]
    for layer in range(num_layers):
        if np.random.rand() < mutation_rate:
            current_device = np.argmax(X[layer])
            new_device = np.random.choice([i for i in range(num_devices) if i != current_device])
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
    
    # Ensure population is treated as a list of individuals (1D array)
    population = np.array(population)
    
    if num_parents % 2 != 0:
        num_parents += 1  # Ensure an even number of parents
        
    # Select parents using np.random.choice, which expects a 1-dimensional array
    selected_parents = np.random.choice(len(population), size=num_parents, p=selection_probs, replace=False)
    
    # Return the selected individuals, not just their indices
    return [population[i] for i in selected_parents]

