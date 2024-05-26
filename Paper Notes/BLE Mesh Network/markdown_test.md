# BLE Mesh Decentralized MCUs Network

```mermaid
graph TD
    subgraph Cluster1 [Cluster 1]
        A1[Relay MCU 1] -- BLE --> A2[End Device MCU 2]
        A2 -- BLE --> A3[End Device MCU 3]
        A3 -- BLE --> A1
        A1 -- BLE --> A4[Friend MCU 4]
        A4 -- BLE --> A2
    end

    subgraph Cluster2 [Cluster 2]
        B1[Relay MCU 5] -- BLE --> B2[End Device MCU 6]
        B2 -- BLE --> B3[End Device MCU 7]
        B3 -- BLE --> B1
        B1 -- BLE --> B4[Friend MCU 8]
        B4 -- BLE --> B2
    end

    subgraph Cluster3 [Cluster 3]
        C1[Relay MCU 9] -- BLE --> C2[End Device MCU 10]
        C2 -- BLE --> C3[End Device MCU 11]
        C3 -- BLE --> C1
        C1 -- BLE --> C4[Friend MCU 12]
        C4 -- BLE --> C2
    end

    A1 -- BLE --> B1
    A2 -- BLE --> C2
    B2 -- BLE --> C3
    B3 -- BLE --> A3
    A4 -- BLE --> C4
    B4 -- BLE --> C4

```


### Explanation:

- **Cluster 1**:
  - **Relay MCU 1** connects to **End Device MCU 2**, **End Device MCU 3**, and **Friend MCU 4**.
  - **End Device MCU 2** connects to **End Device MCU 3** and **Friend MCU 4**.
- **Cluster 2**:
  - **Relay MCU 5** connects to **End Device MCU 6**, **End Device MCU 7**, and **Friend MCU 8**.
  - **End Device MCU 6** connects to **End Device MCU 7** and **Friend MCU 8**.
- **Cluster 3**:
  - **Relay MCU 9** connects to **End Device MCU 10**, **End Device MCU 11**, and **Friend MCU 12**.
  - **End Device MCU 10** connects to **End Device MCU 11** and **Friend MCU 12**.

- **Interconnections**:
  - **Relay MCU 1** (Cluster 1) is connected to **Relay MCU 5** (Cluster 2) using BLE.
  - **End Device MCU 2** (Cluster 1) is connected to **End Device MCU 10** (Cluster 3) using BLE.
  - **End Device MCU 6** (Cluster 2) is connected to **End Device MCU 11** (Cluster 3) using BLE.
  - **End Device MCU 7** (Cluster 2) is connected to **End Device MCU 3** (Cluster 1) using BLE.
  - **Friend MCU 4** (Cluster 1) is connected to **Friend MCU 12** (Cluster 3) using BLE.
  - **Friend MCU 8** (Cluster 2) is connected to **Friend MCU 12** (Cluster 3) using BLE.
