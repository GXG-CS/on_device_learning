import numpy as np
from scipy.sparse import csr_matrix
import time

# Increase the size of the Layer-Device Assignment Matrix X for more noticeable differences
layers = 1000  # Increase the number of layers
devices = 10   # Increase the number of devices

# Randomly generate a dense Layer-Device Assignment Matrix X
np.random.seed(0)  # For reproducibility
X_dense = np.random.randint(0, 2, size=(layers, devices))
X_dense[X_dense.sum(axis=1) == 0, 0] = 1  # Ensure every layer is assigned to at least one device
X_sparse = csr_matrix(X_dense)

# Randomly generate a Transfer Time Matrix T
T = np.random.randint(1, 5, size=(devices, devices))
np.fill_diagonal(T, 0)  # No self-transfers

# Randomly generate a dense Computation Time Matrix C
C = np.random.randint(1, 10, size=(layers, devices))

# Timing comparison with higher resolution timer
start_dense = time.perf_counter()

# Step 1: Create the shifted version of X (X_shifted) as a dense matrix
X_shifted_dense = np.roll(X_dense, -1, axis=0)
X_shifted_dense[-1, :] = 0  # Set the last row to all zeros

# Step 2: Compute the Transition Matrix M using dense matrix multiplication
M_dense = np.dot(X_dense.T, X_shifted_dense)

# Step 3: Perform element-wise multiplication with the Transfer Time Matrix T
transfer_matrix_dense = M_dense * T

# Step 4: Sum all elements to get the total transfer time
T_transfer_dense = np.sum(transfer_matrix_dense)

# Step 5: Calculate Computation Time for each device using the dense matrix C
T_comp_dense = np.sum(C, axis=0)  # Summing along the rows gives the total computation time per device

# Step 6: Determine the Total Computation Time (max of T_comp)
T_total_comp_dense = np.max(T_comp_dense)

end_dense = time.perf_counter()

start_sparse = time.perf_counter()

# Step 1: Create the shifted version of X (X_shifted) as a sparse matrix
X_shifted_sparse_data = np.roll(X_sparse.toarray(), -1, axis=0)
X_shifted_sparse_data[-1, :] = 0  # Set the last row to all zeros
X_shifted_sparse = csr_matrix(X_shifted_sparse_data)

# Step 2: Compute the Transition Matrix M using sparse matrix multiplication
M_sparse = X_sparse.T.dot(X_shifted_sparse)

# Step 3: Perform element-wise multiplication with the Transfer Time Matrix T
transfer_matrix_sparse = csr_matrix(M_sparse.toarray() * T)

# Step 4: Sum all elements to get the total transfer time
T_transfer_sparse = transfer_matrix_sparse.sum()

# Step 5: Calculate Computation Time for each device using the dense matrix C
T_comp_sparse = C.sum(axis=0)  # Summing along the rows gives the total computation time per device

# Step 6: Determine the Total Computation Time (max of T_comp)
T_total_comp_sparse = np.max(T_comp_sparse)

end_sparse = time.perf_counter()

# Output results
print(f"Total Transfer Time (Dense): {T_transfer_dense}")
print(f"Total Computation Time (Dense): {T_total_comp_dense}")
print(f"Time taken (Dense): {end_dense - start_dense:.6f} seconds\n")

print(f"Total Transfer Time (Sparse): {T_transfer_sparse}")
print(f"Total Computation Time (Sparse): {T_total_comp_sparse}")
print(f"Time taken (Sparse): {end_sparse - start_sparse:.6f} seconds")
