import numpy as np
from .common import total_time

def aco_partitioning(num_layers, num_devices, T, C, num_ants=30, max_iterations=100, alpha=1.0, beta=2.0, evaporation_rate=0.5, pheromone_init=1.0):
    pheromone = np.full((num_layers, num_devices), pheromone_init)

    best_solution = None
    best_score = float('inf')

    for iteration in range(max_iterations):
        all_solutions = []
        all_scores = []

        for ant in range(num_ants):
            solution = np.zeros((num_layers, num_devices))

            for layer in range(num_layers):
                probabilities = []
                for device in range(num_devices):
                    heuristic_value = 1.0 / (C[layer, device] + 1e-6)
                    prob = (pheromone[layer, device] ** alpha) * (heuristic_value ** beta)
                    probabilities.append(prob)

                probabilities = np.array(probabilities) / np.sum(probabilities)
                device = np.random.choice(range(num_devices), p=probabilities)
                solution[layer, device] = 1
            
            score = total_time(solution, T, C)
            all_solutions.append(solution)
            all_scores.append(score)

            if score < best_score:
                best_solution = solution
                best_score = score

        pheromone *= (1 - evaporation_rate)
        for solution, score in zip(all_solutions, all_scores):
            pheromone += solution / score

    return best_solution, best_score
