class Node:
    def __init__(self, id, mac_address, uuid, role, features, cpu_speed, sram, psram, flash, bandwidth):
        """
        Initialize a node with specific hardware and network characteristics.

        :param id: Unique identifier for the node.
        :param mac_address: MAC address of the node.
        :param uuid: UUID for the node or its services.
        :param role: Role of the node in the network (e.g., relay, low-power).
        :param features: BLE Mesh features supported by the node (e.g., relay, proxy).
        :param cpu_speed: CPU speed of the node in GHz.
        :param sram: SRAM capacity of the node in KB.
        :param psram: PSRAM capacity of the node in MB.
        :param flash: Flash storage capacity of the node in MB.
        :param bandwidth: Network bandwidth of the node in MB/s.
        """
        self.id = id
        self.mac_address = mac_address
        self.uuid = uuid
        self.role = role
        self.features = features
        self.cpu_speed = cpu_speed
        self.sram = sram
        self.psram = psram
        self.flash = flash
        self.bandwidth = bandwidth
        self.type = 'ESP32-WROVER'  # Node type indicating the hardware platform

    def __str__(self):
        return (f"Node(id={self.id}, mac_address={self.mac_address}, uuid={self.uuid}, role={self.role}, "
                f"features={self.features}, cpu_speed={self.cpu_speed}GHz, sram={self.sram}KB, "
                f"psram={self.psram}MB, flash={self.flash}MB, bandwidth={self.bandwidth}MB/s, type={self.type})")

# Example of creating a node
node = Node(
    id='mcu1',
    mac_address='00:1A:7D:DA:71:13',
    uuid='123e4567-e89b-12d3-a456-426614174000',
    role='relay',
    features=['relay', 'proxy'],
    cpu_speed=0.24,  # 240 MHz
    sram=520,        # 520 KB SRAM
    psram=4,         # 4 MB PSRAM
    flash=4,         # 4 MB Flash
    bandwidth=5      # 5 MB/s
)

print(node)
