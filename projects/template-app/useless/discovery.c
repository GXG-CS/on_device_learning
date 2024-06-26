#include <string.h>
#include "esp_log.h"
#include "esp_gap_ble_api.h"
#include "discovery.h"
#include "device_info.h"

// Structure to store discovered device information
typedef struct {
    esp_bd_addr_t addr;
    int rssi;
    uint8_t adv_data[ADV_DATA_MAX_LEN];
    uint8_t adv_data_len;
} discovered_device_t;

#define MAX_DEVICES 10
static discovered_device_t devices[MAX_DEVICES];
static int num_devices = 0;

static const char *TAG = "DISCOVERY";

// Function to handle GAP events
void gap_event_handler(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t *param) {
    switch (event) {
    case ESP_GAP_BLE_SCAN_RESULT_EVT:
        if (param->scan_rst.search_evt == ESP_GAP_SEARCH_INQ_RES_EVT) {
            ESP_LOGI(TAG, "Device found: %s, RSSI: %d", esp_log_buffer_hex(TAG, param->scan_rst.bda, ESP_BD_ADDR_LEN), param->scan_rst.rssi);

            // Check if the device is already in the list
            int device_idx = -1;
            for (int i = 0; i < num_devices; i++) {
                if (memcmp(devices[i].addr, param->scan_rst.bda, ESP_BD_ADDR_LEN) == 0) {
                    device_idx = i;
                    break;
                }
            }

            // If the device is not in the list, add it
            if (device_idx == -1 && num_devices < MAX_DEVICES) {
                device_idx = num_devices++;
                memcpy(devices[device_idx].addr, param->scan_rst.bda, ESP_BD_ADDR_LEN);
            }

            // Update device information
            if (device_idx != -1) {
                devices[device_idx].rssi = param->scan_rst.rssi;
                devices[device_idx].adv_data_len = param->scan_rst.adv_data_len;
                memcpy(devices[device_idx].adv_data, param->scan_rst.ble_adv, param->scan_rst.adv_data_len);
            }
        }
        break;
    default:
        break;
    }
}

// Function to start scanning
void start_scanning(void) {
    esp_ble_scan_params_t ble_scan_params = {
        .scan_type = BLE_SCAN_TYPE_PASSIVE,
        .own_addr_type = BLE_ADDR_TYPE_PUBLIC,
        .scan_filter_policy = BLE_SCAN_FILTER_ALLOW_ALL,
        .scan_interval = 0x50,
        .scan_window = 0x30
    };
    ESP_ERROR_CHECK(esp_ble_gap_set_scan_params(&ble_scan_params));
}

// Function to get the list of discovered devices
discovered_device_t *get_discovered_devices(int *num) {
    *num = num_devices;
    return devices;
}
