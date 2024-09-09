#ifndef BLE_COMM_SERVICE_H
#define BLE_COMM_SERVICE_H

#include "esp_err.h"

// Define a custom UUID for the service and its characteristics
#define CUSTOM_SERVICE_UUID          0x00FF
#define CUSTOM_CHARACTERISTIC_UUID   0xFF01

// Function to initialize BLE communication service
esp_err_t ble_comm_service_init(void);

// Function to send node information via BLE
esp_err_t ble_comm_service_send_node_info(void);

#endif // BLE_COMM_SERVICE_H
