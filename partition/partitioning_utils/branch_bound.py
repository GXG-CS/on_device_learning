import numpy as np
from .common import calculate_transfer_time, calculate_computation_time

def branch_and_bound(num_layers, num_devices, T, C):
    best_solution = None
    best_cost = float('inf')

    stack = [(0, np.zeros((num_layers, num_devices)), 0)]

    while stack:
        layer_index, current_solution, current_cost = stack.pop()

        if layer_index == num_layers:
            total_time = calculate_transfer_time(current_solution, T) + calculate_computation_time(current_solution, C)
            if total_time < best_cost:
                best_cost = total_time
                best_solution = current_solution.copy()
            continue

        for device in range(num_devices):
            new_solution = current_solution.copy()
            new_solution[layer_index, :] = 0
            new_solution[layer_index, device] = 1

            lower_bound = current_cost + C[layer_index, device]
            if lower_bound >= best_cost:
                continue

            stack.append((layer_index + 1, new_solution, lower_bound))

    return best_solution, best_cost
