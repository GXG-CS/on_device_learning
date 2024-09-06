import numpy as np

# Define the Layer-Device Assignment Matrix X
X = np.array([
    [1, 0, 0],  # Layer 1 on Device 1
    [1, 0, 0],  # Layer 2 on Device 1
    [1, 0, 0],  # Layer 3 on Device 1
    [0, 1, 0],  # Layer 4 on Device 2
    [0, 0, 1],  # Layer 5 on Device 3
    [0, 0, 1],  # Layer 6 on Device 3
])

# Define the Transfer Time Matrix T
T = np.array([
    [0, 2, 4],  # From Device 1 to others
    [2, 0, 3],  # From Device 2 to others
    [4, 3, 0],  # From Device 3 to others
])

# Define the Computation Time Matrix C
C = np.array([
    [3, 0, 0],  # Computation time for Layer 1 on Device 1
    [3, 0, 0],  # Computation time for Layer 2 on Device 1
    [3, 0, 0],  # Computation time for Layer 3 on Device 1
    [0, 2, 0],  # Computation time for Layer 4 on Device 2
    [0, 0, 4],  # Computation time for Layer 5 on Device 3
    [0, 0, 4],  # Computation time for Layer 6 on Device 3
])

# Step 1: Create the shifted version of X (X_shifted)
X_shifted = np.roll(X, -1, axis=0)
X_shifted[-1, :] = 0  # Set the last row to all zeros

# Step 2: Compute the Transition Matrix M
M = np.dot(X.T, X_shifted)

# Step 3: Perform element-wise multiplication with the Transfer Time Matrix T
transfer_matrix = M * T

# Step 4: Sum all elements to get the total transfer time
T_transfer = np.sum(transfer_matrix)

# Step 5: Calculate Computation Time for each device
T_comp = np.sum(C, axis=0)

# Step 6: Determine the Total Computation Time (max of T_comp)
T_total_comp = np.max(T_comp)

print("Layer-Device Assignment Matrix (X):")
print(X)
print("\nShifted Assignment Matrix (X_shifted):")
print(X_shifted)
print("\nTransition Matrix (M):")
print(M)
print("\nElement-wise Multiplication (M * T):")
print(transfer_matrix)
print("\nTotal Transfer Time (T_transfer):", T_transfer)

print("\nComputation Time per Device (T_comp):", T_comp)
print("Total Computation Time (T_total_comp):", T_total_comp)

# Explanation example
# M[1,2] Counts how many times a layer processed on Device 1 is followed by another layer on Device 2.




