import numpy as np
import pulp
from .common import calculate_transfer_time, calculate_computation_time

def milp_partitioning(num_layers, num_devices, T, C):
    prob = pulp.LpProblem("Layer_Device_Partitioning", pulp.LpMinimize)

    X = pulp.LpVariable.dicts("X", (range(num_layers), range(num_devices)), cat="Binary")
    Transfer = pulp.LpVariable.dicts("Transfer", (range(num_layers - 1), range(num_devices), range(num_devices)), cat="Binary")

    computation_time = pulp.lpSum(C[i][j] * X[i][j] for i in range(num_layers) for j in range(num_devices))
    transfer_time = pulp.lpSum(T[k][j] * Transfer[i][k][j] for i in range(num_layers - 1) for k in range(num_devices) for j in range(num_devices))

    prob += computation_time + transfer_time

    for i in range(num_layers):
        prob += pulp.lpSum(X[i][j] for j in range(num_devices)) == 1

    for i in range(num_layers - 1):
        for k in range(num_devices):
            for j in range(num_devices):
                prob += Transfer[i][k][j] <= X[i][k]
                prob += Transfer[i][k][j] <= X[i + 1][j]
                prob += Transfer[i][k][j] >= X[i][k] + X[i + 1][j] - 1

    prob.solve()

    best_solution = np.zeros((num_layers, num_devices))
    for i in range(num_layers):
        for j in range(num_devices):
            if pulp.value(X[i][j]) == 1:
                best_solution[i, j] = 1

    best_cost = pulp.value(prob.objective)
    return best_solution, best_cost
