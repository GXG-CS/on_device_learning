class Network:
    def __init__(self, nodes, network_uuid, app_key, net_key):
        """
        Initialize the BLE Mesh network with specific configuration and a list of nodes.

        :param nodes: A list of Node instances.
        :param network_uuid: UUID for the BLE Mesh network.
        :param app_key: Application key for encrypting application messages.
        :param net_key: Network key for encrypting network messages.
        """
        self.nodes = nodes
        self.network_uuid = network_uuid
        self.app_key = app_key
        self.net_key = net_key

    def get_nodes(self):
        """
        Retrieve the list of nodes in the network.

        Returns:
            List of Node instances.
        """
        return self.nodes

    def get_node_by_id(self, node_id):
        """
        Retrieve a node by its unique identifier.

        :param node_id: Unique identifier of the node.
        Returns:
            Node instance with the specified ID, or None if not found.
        """
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def add_node(self, node):
        """
        Add a new node to the network.

        :param node: Node instance to be added.
        """
        self.nodes.append(node)

    def remove_node(self, node_id):
        """
        Remove a node from the network by its ID.

        :param node_id: Unique identifier of the node to be removed.
        """
        self.nodes = [node for node in self.nodes if node.id != node_id]

    def provision_node(self, node_id):
        """
        Mark a node as provisioned in the network.

        :param node_id: Unique identifier of the node to be provisioned.
        """
        node = self.get_node_by_id(node_id)
        if node:
            node.provisioned = True
            print(f"Node {node_id} provisioned successfully.")

    def __str__(self):
        """
        String representation of the network.

        Returns:
            String listing all nodes and network configuration.
        """
        network_info = (f"Network UUID: {self.network_uuid}\n"
                        f"App Key: {self.app_key}\n"
                        f"Net Key: {self.net_key}\n"
                        f"Nodes:\n")
        return network_info + "\n".join(str(node) for node in self.nodes)

# Example usage
if __name__ == "__main__":
    # Create nodes
    node1 = Node(
        id='mcu1',
        mac_address='00:1A:7D:DA:71:13',
        uuid='123e4567-e89b-12d3-a456-426614174000',
        role='relay',
        features=['relay', 'proxy'],
        cpu_speed=0.24,
        sram=520,
        psram=4,
        flash=4,
        bandwidth=5
    )
    node2 = Node(
        id='mcu2',
        mac_address='00:1A:7D:DA:71:14',
        uuid='123e4567-e89b-12d3-a456-426614174001',
        role='node',
        features=['node'],
        cpu_speed=0.24,
        sram=520,
        psram=4,
        flash=4,
        bandwidth=5
    )

    # Create network with nodes
    network_uuid = 'f47ac10b-58cc-4372-a567-0e02b2c3d479'
    app_key = 'app_key_12345'
    net_key = 'net_key_12345'
    network = Network([node1, node2], network_uuid, app_key, net_key)

    print("Network configuration:")
    print(network)

    # Add a new node
    new_node = Node(
        id='mcu3',
        mac_address='00:1A:7D:DA:71:15',
        uuid='123e4567-e89b-12d3-a456-426614174002',
        role='low-power',
        features=['low-power'],
        cpu_speed=0.24,
        sram=520,
        psram=4,
        flash=4,
        bandwidth=5
    )
    network.add_node(new_node)
    print("\nUpdated network configuration after adding a node:")
    print(network)

    # Remove a node
    network.remove_node('mcu1')
    print("\nUpdated network configuration after removing a node:")
    print(network)
