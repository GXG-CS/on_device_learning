### README for Model Partitioning and Deployment Framework

#### Overview
This framework facilitates the partitioning of machine learning models and their deployment across multiple ESP32 WROVER MCUs. The framework calculates optimal model split points based on network topology and node capabilities, partitions the model accordingly, and manages deployment to ensure efficient execution.

#### Repository Structure
- `model.py`: Defines the TensorFlow model architecture and includes utilities for extracting layer details and computing layer operations.
- `network.py`: Manages the BLE Mesh network configuration, including node management and network operations.
- `node.py`: Describes the individual nodes within the network, detailing their hardware and connectivity features.
- `partitioner.py`: Handles determination of model partitioning points based on node capabilities and network constraints.
- `deployer.py`: Manages the deployment of model segments to individual MCUs based on the partitioning results.
- `partition_methods/`
  - `autoSplit.py`: Automated model splitting based on predefined criteria.
  - `customPartitioner.py`: Custom logic for model partitioning, considering specific project requirements.
  - `DADS.py`: Dynamic Adaptive Deep Learning System partitioning.
  - `neurosurgeon.py`: Advanced model partitioning based on neural decision processes.
  - `QDMP.py`: Quantitative Decision-Making Partitioner for efficient resource utilization.




### Mathematical Formulation for Model Partitioning

#### Key Components:

1. **Model** ($m$): 
   - Represents the $m$ layers in the model.
   - Example: $m = 10$ for a model with 10 layers.

2. **Devices** ($n$): 
   - Number of devices available for deploying the model segments.
   - Example: $n = 3$ for three available devices.

#### Objective:
Minimize the following:
1. **Computation Time** ($T_{comp}$): 
   - Total time taken for computation across all devices.
   - Example: Minimize $T_{comp}$ to reduce processing delays.

2. **Transfer Time** ($T_{trans}$): 
   - Total time taken for transferring data between devices.
   - Example: Minimize $T_{trans}$ to reduce latency.

3. **Energy Cost** ($E$): 
   - Total energy consumed for both computation and data transfer.
   - Example: Minimize $E$ to enhance energy efficiency.

#### Formulation:
Minimize:
$$
\text{Objective} = \alpha \cdot T_{comp} + \beta \cdot T_{trans} + \gamma \cdot E
$$

Where:
- $\alpha, \beta, \gamma$ are weights representing the importance of computation time, transfer time, and energy cost, respectively.

#### Constraints:

1. **Memory Constraint**: 
   $$
   \sum_{L_j \in S_i} M_j \leq \text{Memory of Device}_i, \quad \forall i \in [1, n]
   $$
   - Where $M_j$ is the memory required by layer $L_j$ and $S_i$ is the set of layers assigned to device $i$.
   - Example: Ensure that memory usage does not exceed device capacity.

2. **Error Constraint**:
   $$
   \Delta \text{Error}_{\text{deployed}} \leq \epsilon
   $$
   - Where $\Delta \text{Error}_{\text{deployed}}$ is the increase in error due to model segmentation and $\epsilon$ is the acceptable error increase threshold.
   - Example: Maintain acceptable accuracy levels post-deployment.
#### Variables:
- **Partition Points** ($P_i$): 
  - Indicates where the model is split into segments.
  - Example: Determine optimal $P_i$ to balance load.

- **Segments** ($S_i$): 
  - Segments of the model assigned to each device.
  - Example: Define $S_i$ to ensure effective distribution.

### Problem Solution Strategy:
The problem can be approached using techniques like:
- **Dynamic Programming**: 
  - Optimize partition points based on computational and memory requirements.
  - Example: Use dynamic programming to systematically explore options.

- **Heuristic Methods**: 
  - Find feasible partitions quickly when exact methods are computationally infeasible.
  - Example: Apply heuristics to rapidly generate solutions.

- **Graph Partitioning Algorithms**: 
  - Effectively distribute the load while minimizing inter-device communication.
  - Example: Utilize graph algorithms to manage dependencies and balance workloads.
