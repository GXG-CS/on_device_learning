import numpy as np
from .common import total_time, generate_individual

def hill_climbing(num_layers, num_devices, T, C, max_iterations=1000):
    current_solution = generate_individual(num_layers, num_devices)
    current_cost = total_time(current_solution, T, C)

    best_solution = current_solution.copy()
    best_cost = current_cost

    for iteration in range(max_iterations):
        new_solution = current_solution.copy()
        layer_to_change = np.random.randint(0, num_layers)
        current_device = np.argmax(new_solution[layer_to_change])
        new_device = np.random.choice([i for i in range(num_devices) if i != current_device])
        new_solution[layer_to_change, current_device] = 0
        new_solution[layer_to_change, new_device] = 1

        new_cost = total_time(new_solution, T, C)

        if new_cost < current_cost:
            current_solution = new_solution
            current_cost = new_cost

            if new_cost < best_cost:
                best_solution = new_solution
                best_cost = new_cost

    return best_solution, best_cost
