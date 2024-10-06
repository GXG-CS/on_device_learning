### Inputs for the Heuristic Procedure (`DistributeDNNModel`)

1. **DNN Model**:
   - **Structure**: Represented as a **Directed Acyclic Graph (DAG)**: `G = (V, E)`
     - **Vertices (`V`)**: Each vertex `v_i ∈ V` corresponds to a layer in the DNN model.
     - **Edges (`E`)**: Each edge `e_{ij} = (v_i, v_j) ∈ E` indicates a dependency between layers `v_i` and `v_j`.

2. **Device List (`N`)**:
   - A set of available devices: `N = {n_1, n_2, ..., n_m}`
   - **Properties of Each Device**:
     - **`mem_size(n_i)`**: Available memory capacity of device `n_i`.
     - **`compute_power(n_i)`**: Computation capability or speed of device `n_i`.
     - **`battery_level(n_i)`**: Initial energy level of device `n_i`.
     - **`role(n_i)`**: Role of the device (e.g., `Central`, `Peripheral`, `Coordinator`).

3. **Network Communication (`C`)**:
   - Represents the communication structure between devices: `C = (N, L)`
   - **Vertices (`N`)**: Nodes/devices in the network.
   - **Edges (`L`)**: Each edge `l_{ij} = (n_i, n_j) ∈ L` represents a communication link between devices `n_i` and `n_j`.
   - **Communication Properties**:
     - **`transfer_time(l_{ij})`**: Estimated time to transfer data from device `n_i` to device `n_j`.
     - **`bandwidth(l_{ij})`**: Available bandwidth for data exchange.
     - **`mtu_size(l_{ij})`**: Maximum Transmission Unit size for BLE GATT communication.

### Summary
- **DNN Model**: DAG structure `G = (V, E)` with layers and dependencies.
- **Device List**: `N` with properties (`mem_size`, `compute_power`, `battery_level`, `role`).
- **Network Communication**: `C = (N, L)` with `transfer_time`, `bandwidth`, and `mtu_size` properties.
