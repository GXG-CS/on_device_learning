# Network Architecture for Decentralized Distributed Machine Learning on BLE Mesh MCU Network

#### Objectives
- **Decentralization**: Ensure that the network can operate without a central coordinator.
- **Scalability**: Allow the network to grow and accommodate more nodes.
- **Reliability**: Ensure robust communication and fault tolerance.
- **Efficiency**: Optimize energy consumption and communication overhead.

### Key Components of the Network Architecture

1. **Nodes**
   - **Sensor Nodes**: Collect and preprocess data from the environment.
   - **Processing Nodes**: Perform local data processing and machine learning tasks.
   - **Aggregation Nodes**: Aggregate data or model updates from other nodes.
   - **Relay Nodes**: Facilitate communication between distant nodes by forwarding data.

2. **Communication Protocols**
   - **BLE (Bluetooth Low Energy)**: Used for communication between nodes. BLE is chosen for its low power consumption and sufficient range for typical MCU deployments.

3. **Network Topology**
   - **Mesh Topology**: Nodes are connected in a mesh structure where each node can communicate with multiple other nodes. This ensures redundancy and robustness.
   - **Clusters**: Nodes are grouped into clusters based on proximity. Each cluster has a designated aggregation node and relay nodes to facilitate communication within and between clusters.

4. **Data Flow**
   - **Local Data Collection**: Sensor nodes collect data and preprocess it.
   - **Data Processing**: Processing nodes perform local training or inference on the collected data.
   - **Model Aggregation**: Aggregation nodes collect model updates from processing nodes and perform aggregation tasks.
   - **Model Distribution**: Aggregated models are distributed back to processing nodes for further training or inference.

### Detailed Description

#### 1. Node Types and Roles

- **Sensor Nodes**
  - **Function**: Collect environmental data using sensors (e.g., temperature, humidity, light).
  - **Characteristics**: Low power consumption, limited processing capability.
  - **Example**: ESP32-WROVER with attached sensors.

- **Processing Nodes**
  - **Function**: Perform local data preprocessing, feature extraction, and machine learning tasks.
  - **Characteristics**: Moderate power consumption, higher processing capability.
  - **Example**: ESP32-WROVER-DEV running TinyML models.

- **Aggregation Nodes**
  - **Function**: Collect and aggregate data or model updates from multiple nodes, perform intermediate data fusion or model averaging.
  - **Characteristics**: Higher power consumption, significant memory and processing capability.
  - **Example**: ESP32-WROVER with additional memory modules.

- **Relay Nodes**
  - **Function**: Extend the communication range by forwarding messages between nodes.
  - **Characteristics**: Moderate power consumption, minimal processing requirement.
  - **Example**: ESP32 modules configured as relays.

#### 2. Communication Protocols

- **BLE (Bluetooth Low Energy)**
  - **Advantages**: Low power consumption, sufficient range for most MCU-based networks.
  - **Implementation**: Nodes use BLE to advertise their presence, establish connections, and exchange data or model updates.

#### 3. Network Topology

- **Mesh Network**
  - **Structure**: Each node can communicate with multiple other nodes, forming a resilient network.
  - **Advantages**: Redundancy, fault tolerance, and robustness.
  - **Implementation**: Use BLE mesh capabilities to manage connections and data routing.

- **Cluster Formation**
  - **Local Clusters**: Nodes are grouped into clusters based on proximity. Each cluster has a local aggregation node.
  - **Inter-Cluster Communication**: Relay nodes facilitate communication between clusters, ensuring the network scales efficiently.

#### 4. Data Flow and Machine Learning Workflow

- **Data Collection and Preprocessing**
  - Sensor nodes collect raw data and perform initial preprocessing (e.g., filtering, normalization).

- **Local Training**
  - Processing nodes use preprocessed data to train local machine learning models. They may use lightweight frameworks like TensorFlow Lite for Microcontrollers.

- **Model Aggregation**
  - Aggregation nodes collect model updates (e.g., gradients, weights) from processing nodes. They perform aggregation tasks like federated averaging:
    $$w_{global} = \frac{1}{N} \sum_{i=1}^{N} w_i$$
  - where $w_{global}$ is the global model and $w_i$ are the local model updates.

- **Model Distribution**
  - Aggregated models are distributed back to processing nodes. Nodes update their local models with the new global parameters.

- **Inference**
  - Nodes use the trained global model to make predictions on new data. Results are shared with relevant nodes or used for local decision-making.

### Summary

The network architecture for a decentralized distributed machine learning system on a BLE mesh MCU network includes sensor nodes, processing nodes, aggregation nodes, and relay nodes, all interconnected using BLE in a mesh topology. This architecture ensures decentralization, scalability, reliability, and efficiency, enabling robust data collection, processing, training, and inference across the network.
