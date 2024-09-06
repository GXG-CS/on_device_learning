// node_info.h

#ifndef NODE_INFO_H
#define NODE_INFO_H

#include <stdint.h>

// Function to get free DRAM of the node
uint32_t get_free_dram(void);

// Function to get the node's UUID (MAC Address for ESP32 BLE Mesh)
void get_node_uuid(uint8_t* uuid);

// Function to print node info (UUID, MAC, DRAM)
void print_node_info(void);

#endif // NODE_INFO_H
