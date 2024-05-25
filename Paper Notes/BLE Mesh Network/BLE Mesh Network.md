# BLE Mesh Network

<!-- - [[communication]] -->

## Key Characteristics of BLE Mesh Network
- [[many-to-many]]:
    - Nodes in BLE mesh network can communicate with multiple nodes simultaneously.

- Relay Nodes
    - Nodes designated as relays can forward messages to extend the range of the network.
    - Relays nodes help propagate messages to nodes that are out of range of the original sender.

- Managed Flooding
    - Message are broadcased and relayed throughout the newrok using a mechanism called managed flooding.
    - Each node taht receives a message decides whether to replay it based on specific rules, such as the Time to Live(TTL) value.

- Addressing
    - BLE mesh uses unicast, group, and virtual addresses to direct messages to specific nodes or groups of nodes.
    - Unicast addresses are unique to each node, group addresses are shared by multiple nodes, and virtual addresses are used for logical grouping.

- Scalability
    - BLE mesh networks can support thousands of nodes.
    - The network can be extended by adding more nodes or relay nodes.