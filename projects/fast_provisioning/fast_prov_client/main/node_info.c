#include <stdio.h>
#include <string.h>
#include <inttypes.h>  // Include for PRIu32
#include "node_info.h"
#include "esp_system.h"
#include "esp_log.h"
#include "esp_heap_caps.h"
#include "esp_wifi.h"
#include "esp_mac.h"

#define TAG "NODE_INFO"

// Function to get the free DRAM of the node
uint32_t get_free_dram(void) {
    return heap_caps_get_free_size(MALLOC_CAP_8BIT);
}

// Function to get the node's UUID (MAC Address for ESP32 BLE Mesh)
void get_node_uuid(uint8_t* uuid) {
    // Retrieve the base MAC address (usually used as UUID in BLE Mesh)
    esp_err_t err = esp_read_mac(uuid, ESP_MAC_BT);  // Get MAC for Bluetooth
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to get MAC address, err: %d", err);
        memset(uuid, 0, 6); // Set to 0 in case of error
    }
}

// Function to print node info (UUID, MAC, DRAM)
void print_node_info(void) {
    uint8_t uuid[6] = {0};
    uint32_t free_dram = get_free_dram();

    // Get UUID (MAC Address)
    get_node_uuid(uuid);

    // Print Node Information
    ESP_LOGI(TAG, "Node Info:");
    ESP_LOGI(TAG, "UUID (MAC Address): %02X:%02X:%02X:%02X:%02X:%02X", 
             uuid[0], uuid[1], uuid[2], uuid[3], uuid[4], uuid[5]);
    // Use PRIu32 for printing the uint32_t value correctly
    ESP_LOGI(TAG, "Free DRAM: %" PRIu32 " bytes", free_dram);
}


