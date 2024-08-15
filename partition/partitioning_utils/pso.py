import numpy as np
from .common import total_time, generate_individual

def pso_partitioning(num_layers, num_devices, T, C, num_particles=30, max_iterations=100, w=0.5, c1=1.5, c2=1.5):
    particles = [generate_individual(num_layers, num_devices) for _ in range(num_particles)]
    velocities = [np.zeros((num_layers, num_devices)) for _ in range(num_particles)]
    
    personal_best_positions = particles.copy()
    personal_best_scores = [total_time(p, T, C) for p in particles]
    
    global_best_position = personal_best_positions[np.argmin(personal_best_scores)]
    global_best_score = min(personal_best_scores)
    
    for iteration in range(max_iterations):
        for i in range(num_particles):
            r1 = np.random.rand(num_layers, num_devices)
            r2 = np.random.rand(num_layers, num_devices)
            velocities[i] = (w * velocities[i] + 
                             c1 * r1 * (personal_best_positions[i] - particles[i]) + 
                             c2 * r2 * (global_best_position - particles[i]))
            
            particles[i] += velocities[i]
            
            for layer in range(num_layers):
                device = np.argmax(particles[i][layer])
                particles[i][layer] = np.zeros(num_devices)
                particles[i][layer][device] = 1
            
            current_score = total_time(particles[i], T, C)
            
            if current_score < personal_best_scores[i]:
                personal_best_positions[i] = particles[i].copy()
                personal_best_scores[i] = current_score
            
            if current_score < global_best_score:
                global_best_position = particles[i].copy()
                global_best_score = current_score
    
    return global_best_position, global_best_score
