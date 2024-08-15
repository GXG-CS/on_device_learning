import numpy as np
from .common import calculate_transfer_time, calculate_computation_time

def greedy_partitioning(num_layers, num_devices, T, C):
    X = np.zeros((num_layers, num_devices))
    
    for layer in range(num_layers):
        best_device = None
        best_total_time = float('inf')
        
        for device in range(num_devices):
            temp_X = X.copy()
            temp_X[layer, :] = 0
            temp_X[layer, device] = 1
            
            transfer_time = calculate_transfer_time(temp_X, T)
            computation_time = calculate_computation_time(temp_X, C)
            total_time = transfer_time + computation_time
            
            if total_time < best_total_time:
                best_total_time = total_time
                best_device = device
        
        X[layer, best_device] = 1
    
    final_transfer_time = calculate_transfer_time(X, T)
    final_computation_time = calculate_computation_time(X, C)
    
    return X, final_transfer_time, final_computation_time
