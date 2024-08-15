import numpy as np
import random
from .common import total_time, generate_individual, crossover, mutate, select_parents

def genetic_algorithm(num_layers, num_devices, T, C, population_size=50, num_generations=100, mutation_rate=0.01):
    population = [generate_individual(num_layers, num_devices) for _ in range(population_size)]
    
    for generation in range(num_generations):
        fitness_scores = [1 / total_time(individual, T, C) for individual in population]
        parents = select_parents(population, fitness_scores, population_size // 2)
        next_generation = []
        
        for i in range(0, len(parents), 2):
            parent1, parent2 = parents[i], parents[i + 1]
            child = crossover(parent1, parent2)
            child = mutate(child, num_devices, mutation_rate)
            next_generation.append(child)
        
        population = next_generation + parents[:len(next_generation)]
    
    final_fitness_scores = [1 / total_time(individual, T, C) for individual in population]
    best_index = np.argmax(final_fitness_scores)
    best_individual = population[best_index]
    best_cost = total_time(best_individual, T, C)
    
    return best_individual, best_cost
