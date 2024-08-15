import numpy as np
from collections import deque
from .common import total_time, generate_individual

def tabu_search(num_layers, num_devices, T, C, max_iterations=1000, tabu_tenure=10):
    current_solution = generate_individual(num_layers, num_devices)
    current_cost = total_time(current_solution, T, C)

    best_solution = current_solution.copy()
    best_cost = current_cost

    tabu_list = deque(maxlen=tabu_tenure)

    for iteration in range(max_iterations):
        neighbors = []
        for layer in range(num_layers):
            current_device = np.argmax(current_solution[layer])
            for device in range(num_devices):
                if device != current_device:
                    new_solution = current_solution.copy()
                    new_solution[layer, current_device] = 0
                    new_solution[layer, device] = 1
                    neighbors.append((new_solution, (layer, device)))

        best_neighbor_solution = None
        best_neighbor_cost = float('inf')
        best_move = None

        for neighbor_solution, move in neighbors:
            if move in tabu_list:
                continue

            neighbor_cost = total_time(neighbor_solution, T, C)
            if neighbor_cost < best_neighbor_cost:
                best_neighbor_solution = neighbor_solution
                best_neighbor_cost = neighbor_cost
                best_move = move

        if best_neighbor_solution is not None:
            current_solution = best_neighbor_solution
            current_cost = best_neighbor_cost
            tabu_list.append(best_move)

            if current_cost < best_cost:
                best_solution = current_solution
                best_cost = current_cost

    return best_solution, best_cost
