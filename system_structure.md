# System Architecture Overview

## Distributed Inference and Application Layer
- **DNN Model Partitioning**: layer-wise profiling, partition search using algorithms.
- **Failure Recovery & Redundancy**: dynamic reassignment, backup paths, recovery feedback loop.
- **Optimization & Feedback**: real-time performance feedback, energy and memory optimization.
- **Final Output Aggregation**: collect and merge intermediate results from distributed nodes.

## Virtual Network Coordination Layer
- **Network Communication and Abstraction**:
  - Heartbeat, confirmation message format, retries, reliable delivery.
  - Sequence numbers, ACK/retransmission, message integrity, real-time status checks.
- **Resources and Workload Management (Scheduler)**:
  - Dynamic task scheduling, task prioritization, workload distribution, load balancing.
  - Feedback integration for real-time adjustment of task allocation.
- **Parallelism and Pipeline Execution**:
  - Pipeline-based task execution, multitasking, multi-threading, task synchronization.
  - Task barriers for synchronization across nodes, ensuring in-order execution.
- **Data Preprocessing and Transfer Management**:
  - Data normalization, compression, segmentation, and efficient data transfer.
  - Flow control, batching, and fragmentation/reassembly of large data sets.
- **Hardware Profiling and Abstraction**:
  - CPU load monitoring, memory profiling, energy consumption tracking, dynamic adaptation.
  - Hardware abstraction layer, real-time reconfiguration based on resource profiling.

## Core Infrastructure Layer
- **BLE Mesh Framework**: dynamic topology, provisioning, role assignment.
- **Communication Protocols**: GATT, flooding, message integrity with ACK, retries, fragmentation.
- **Network Diagnostics**: node health monitoring, failure detection, provisioner-based coordination.
- **Message Control**: packet fragmentation, reassembly, and flow control.
