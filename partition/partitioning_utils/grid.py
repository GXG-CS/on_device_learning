import numpy as np
import itertools
from .common import calculate_transfer_time, calculate_computation_time

def grid_search(num_layers, num_devices, T, C):
    possible_assignments = list(itertools.product(range(num_devices), repeat=num_layers))
    
    best_X = None
    best_total_time = float('inf')
    
    for assignment in possible_assignments:
        X = np.zeros((num_layers, num_devices))
        for layer, device in enumerate(assignment):
            X[layer, device] = 1
        
        transfer_time = calculate_transfer_time(X, T)
        computation_time = calculate_computation_time(X, C)
        total_time = transfer_time + computation_time
        
        if total_time < best_total_time:
            best_total_time = total_time
            best_X = X
    
    return best_X, best_total_time
