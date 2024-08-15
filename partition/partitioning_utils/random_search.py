import numpy as np
from .common import total_time, generate_individual

def random_search(num_layers, num_devices, T, C, num_trials=1000):
    best_solution = None
    best_cost = float('inf')

    for _ in range(num_trials):
        solution = generate_individual(num_layers, num_devices)
        cost = total_time(solution, T, C)
        
        if cost < best_cost:
            best_solution = solution
            best_cost = cost

    return best_solution, best_cost
