import numpy as np

# Define the Layer-Device Assignment Matrix X
X = np.array([
    [0, 1, 0],  # Layer 1 on Device 2
    [1, 0, 0],  # Layer 2 on Device 1
    [0, 0, 1],  # Layer 3 on Device 3
    [1, 0, 0],  # Layer 4 on Device 1
])

# Define the Transfer Time Matrix T
T = np.array([
    [0, 3, 5],  # From Device 1 to others
    [3, 0, 2],  # From Device 2 to others
    [5, 2, 0],  # From Device 3 to others
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

print("Layer-Device Assignment Matrix (X):")
print(X)
print("\nShifted Assignment Matrix (X_shifted):")
print(X_shifted)
print("\nTransition Matrix (M):")
print(M)
print("\nElement-wise Multiplication (M * T):")
print(transfer_matrix)
print("\nTotal Transfer Time (T_transfer):", T_transfer)
