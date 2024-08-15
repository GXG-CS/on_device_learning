import numpy as np
import random
from .common import total_time, generate_individual

def simulated_annealing(num_layers, num_devices, T, C, initial_temp=1000, cooling_rate=0.995, min_temp=1):
    current_X = generate_individual(num_layers, num_devices)
    current_cost = total_time(current_X, T, C)
    best_X = current_X.copy()
    best_cost = current_cost
    
    temperature = initial_temp

    while temperature > min_temp:
        new_X = current_X.copy()
        layer = random.randint(0, num_layers - 1)
        current_device = np.argmax(new_X[layer])
        new_device = random.choice([i for i in range(num_devices) if i != current_device])
        new_X[layer, current_device] = 0
        new_X[layer, new_device] = 1
        
        new_cost = total_time(new_X, T, C)
        
        if new_cost < current_cost or random.random() < np.exp((current_cost - new_cost) / temperature):
            current_X = new_X
            current_cost = new_cost
        
        if new_cost < best_cost:
            best_X = new_X
            best_cost = new_cost
        
        temperature *= cooling_rate

    return best_X, best_cost
