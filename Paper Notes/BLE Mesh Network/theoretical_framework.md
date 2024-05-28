# Decentralized Distributed BLE Mesh MCUs Network

### Profiling the BLE Mesh Network

### Graph Representation in MCU BLE Mesh Networks

#### 1. Nodes

In the context of a BLE mesh network, nodes represent the MCUs (Microcontroller Units) participating in the network. Different types of nodes can have distinct roles and capabilities:

- **Standard Nodes**: Regular nodes that participate in the mesh network for data transmission and reception.
- **Relay Nodes**: Nodes that help in forwarding data to other nodes, extending the range of the network.
- **Proxy Nodes**: Nodes that interface with devices that do not support BLE mesh, acting as intermediaries.
- **Friend Nodes**: Nodes that store messages for low-power nodes and deliver them when requested.
- **Low-Power Nodes**: Energy-efficient nodes that periodically wake up to communicate with friend nodes.

#### 2. Edges

Edges represent the undirected communication links between the nodes in the BLE mesh network. These edges can have various properties:

- **Weights**: Edges can be weighted to represent various factors such as:
  - **Distance**: The physical distance between two nodes.
  - **Signal Strength**: The strength of the BLE signal between two nodes.
  - **Latency**: The time delay in communication between two nodes.
  - **Bandwidth**: The available communication bandwidth between two nodes.
  - **Energy Consumption**: The energy cost of communication between two nodes.

- **Types**: Different types of edges can exist based on the nature of communication:
  - **Data Transmission Edges**: Used for regular data exchange between nodes.
  - **Control Edges**: Used for sending control signals or commands between nodes.
  - **Broadcast Edges**: Used for broadcasting information to multiple nodes.



### Data Storage Strategy for BLE Mesh MCU Network

### Model Parallelism

### Data Parallelism


### Incremental Learning

### Gradient Compression
peer-to-peer learning 