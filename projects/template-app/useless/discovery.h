#ifndef DISCOVERY_H
#define DISCOVERY_H

#include "esp_gap_ble_api.h"

#define MAX_DEVICES 10

typedef struct {
    uint8_t addr[ESP_BD_ADDR_LEN];
    int rssi;
} discovered_device_t;

void gap_event_handler(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t *param);
discovered_device_t *get_discovered_devices(int *count);

#endif // DISCOVERY_H
