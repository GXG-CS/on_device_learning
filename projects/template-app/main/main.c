#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_system.h"
#include "esp_gap_ble_api.h"
#include "device_info.h"
#include "init.h"
#include "main.h"

#define UUID_LEN 16
#define MAX_DEVICES 10

typedef struct {
    esp_bd_addr_t addr; // Device address
    uint8_t uuid[UUID_LEN]; // Device UUID
} device_t;

static const char *TAG = "MAIN";

uint8_t network_uuid[UUID_LEN] = {0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0}; // Network UUID

device_t devices[MAX_DEVICES]; // Array to store discovered devices
int device_count = 0; // Counter for the number of discovered devices

void uuid_to_string(const uint8_t *uuid, char *str) {
    for (int i = 0; i < UUID_LEN; i++) {
        sprintf(&str[i * 2], "%02X", uuid[i]);
    }
    str[UUID_LEN * 2] = '\0';
}

void start_advertising(void) {
    char uuid_str[UUID_LEN * 2 + 1];
    uuid_to_string(network_uuid, uuid_str);

    ESP_LOGI(TAG, "Starting advertising with Network UUID: %s", uuid_str);

    esp_ble_adv_data_t adv_data = {
        .set_scan_rsp = false,
        .include_name = true,
        .include_txpower = true,
        .min_interval = 0x20,
        .max_interval = 0x40,
        .appearance = 0x00,
        .manufacturer_len = 0,
        .p_manufacturer_data = NULL,
        .service_data_len = 0,
        .p_service_data = NULL,
        .service_uuid_len = UUID_LEN,
        .p_service_uuid = network_uuid,
        .flag = (ESP_BLE_ADV_FLAG_GEN_DISC | ESP_BLE_ADV_FLAG_BREDR_NOT_SPT),
    };

    esp_ble_adv_params_t adv_params = {
        .adv_int_min        = 0x20,
        .adv_int_max        = 0x40,
        .adv_type           = ADV_TYPE_IND,
        .own_addr_type      = BLE_ADDR_TYPE_PUBLIC,
        .channel_map        = ADV_CHNL_ALL,
        .adv_filter_policy  = ADV_FILTER_ALLOW_SCAN_ANY_CON_ANY,
    };

    ESP_ERROR_CHECK(esp_ble_gap_config_adv_data(&adv_data));
    ESP_ERROR_CHECK(esp_ble_gap_start_advertising(&adv_params));
}

void gap_event_handler(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t *param) {
    if (event == ESP_GAP_BLE_SCAN_RESULT_EVT) {
        if (param->scan_rst.search_evt == ESP_GAP_SEARCH_INQ_RES_EVT) {
            char device_uuid_str[UUID_LEN * 2 + 1];
            uuid_to_string(param->scan_rst.ble_adv, device_uuid_str);

            ESP_LOGI(TAG, "Received packet Device UUID: %s, MAC: %02X:%02X:%02X:%02X:%02X:%02X",
                     device_uuid_str, param->scan_rst.bda[0], param->scan_rst.bda[1], param->scan_rst.bda[2],
                     param->scan_rst.bda[3], param->scan_rst.bda[4], param->scan_rst.bda[5]);

            bool contains_network_uuid = false;
            for (int i = 0; i < param->scan_rst.adv_data_len - UUID_LEN; i++) {
                if (memcmp(param->scan_rst.ble_adv + i, network_uuid, UUID_LEN) == 0) {
                    contains_network_uuid = true;
                    break;
                }
            }

            if (contains_network_uuid) {
                ESP_LOGI(TAG, "Packet contains Network UUID: %s", device_uuid_str);

                device_t device;
                memcpy(device.addr, param->scan_rst.bda, ESP_BD_ADDR_LEN);
                memcpy(device.uuid, param->scan_rst.ble_adv, UUID_LEN);

                if (device_count < MAX_DEVICES) {
                    devices[device_count++] = device;
                    ESP_LOGI(TAG, "Discovered device with matching Network UUID: %02X:%02X:%02X:%02X:%02X:%02X",
                             device.addr[0], device.addr[1], device.addr[2], device.addr[3], device.addr[4], device.addr[5]);
                }
            } else {
                ESP_LOGI(TAG, "Packet does not contain Network UUID");
            }
        }
    }
}

void display_devices_task(void *param) {
    char uuid_str[UUID_LEN * 2 + 1];
    uuid_to_string(network_uuid, uuid_str);
    while (1) {
        ESP_LOGI(TAG, "Network UUID: %s", uuid_str);
        for (int i = 0; i < device_count; i++) {
            char device_uuid_str[UUID_LEN * 2 + 1];
            uuid_to_string(devices[i].uuid, device_uuid_str);
            ESP_LOGI(TAG, "Discovered Device %d: MAC %02X:%02X:%02X:%02X:%02X:%02X, Device UUID: %s",
                     i, devices[i].addr[0], devices[i].addr[1], devices[i].addr[2],
                     devices[i].addr[3], devices[i].addr[4], devices[i].addr[5], device_uuid_str);
        }
        vTaskDelay(pdMS_TO_TICKS(3000));
    }
}

void app_main() {
    ESP_LOGI("FLASH", "Firmware flashed successfully!");

    initialize_nvs();
    initialize_bluetooth();
    initialize_gap_callback();
    initialize_scanning();
    start_advertising();

    create_device_info();
    initialize_tasks();
}
