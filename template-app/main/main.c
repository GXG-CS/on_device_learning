#include "nvs_flash.h"
#include "esp_bt.h"
#include "esp_gap_ble_api.h"
#include "esp_log.h"
#include "esp_bt_main.h"
#include "esp_mac.h" // Include the necessary header for MAC address functions

#define TAG "BLE_MESH_APP"
#define ADV_DATA_LEN 31

static uint8_t adv_data[ADV_DATA_LEN] = {0};
static esp_ble_adv_params_t adv_params = {
    .adv_int_min        = 0x20,
    .adv_int_max        = 0x40,
    .adv_type           = ADV_TYPE_IND,
    .own_addr_type      = BLE_ADDR_TYPE_PUBLIC,
    .channel_map        = ADV_CHNL_ALL,
    .adv_filter_policy  = ADV_FILTER_ALLOW_SCAN_ANY_CON_ANY,
};

static void gap_callback(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t *param) {
    switch (event) {
        case ESP_GAP_BLE_ADV_DATA_SET_COMPLETE_EVT:
            ESP_LOGI(TAG, "Advertising data set complete");
            esp_ble_gap_start_advertising(&adv_params);
            break;
        case ESP_GAP_BLE_SCAN_PARAM_SET_COMPLETE_EVT:
            ESP_LOGI(TAG, "Scan parameters set complete");
            esp_ble_gap_start_scanning(30);
            break;
        case ESP_GAP_BLE_SCAN_RESULT_EVT: {
            esp_ble_gap_cb_param_t *scan_result = (esp_ble_gap_cb_param_t *)param;
            if (scan_result->scan_rst.search_evt == ESP_GAP_SEARCH_INQ_RES_EVT) {
                char bda_str[18];
                snprintf(bda_str, sizeof(bda_str), "%02x:%02x:%02x:%02x:%02x:%02x",
                         scan_result->scan_rst.bda[0], scan_result->scan_rst.bda[1], scan_result->scan_rst.bda[2],
                         scan_result->scan_rst.bda[3], scan_result->scan_rst.bda[4], scan_result->scan_rst.bda[5]);

                // Check if the discovered device is an ESP32
                if (scan_result->scan_rst.ble_adv[5] == 0x4C && scan_result->scan_rst.ble_adv[6] == 0x00) { // Apple Manufacturer Specific Data
                    ESP_LOGI(TAG, "Discovered ESP32 device: %s, RSSI: %d", bda_str, scan_result->scan_rst.rssi);
                }
            }
            break;
        }
        case ESP_GAP_BLE_ADV_START_COMPLETE_EVT:
            if (param->adv_start_cmpl.status == ESP_BT_STATUS_SUCCESS) {
                ESP_LOGI(TAG, "Advertising started successfully");
            } else {
                ESP_LOGE(TAG, "Failed to start advertising");
            }
            break;
        default:
            break;
    }
}

void app_main(void) {
    esp_err_t ret;

    // Initialize NVS
    ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
    ESP_LOGI(TAG, "NVS initialized successfully");

    // Initialize Bluetooth
    ESP_ERROR_CHECK(esp_bt_controller_mem_release(ESP_BT_MODE_CLASSIC_BT));
    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_bt_controller_init(&bt_cfg));
    ESP_ERROR_CHECK(esp_bt_controller_enable(ESP_BT_MODE_BLE));
    ESP_ERROR_CHECK(esp_bluedroid_init());
    ESP_ERROR_CHECK(esp_bluedroid_enable());
    ESP_LOGI(TAG, "Bluetooth initialized successfully");

    // Configure BLE advertising data
    adv_data[0] = 0x02; // Length of Flags field
    adv_data[1] = ESP_BLE_AD_TYPE_FLAG;
    adv_data[2] = ESP_BLE_ADV_FLAG_GEN_DISC | ESP_BLE_ADV_FLAG_BREDR_NOT_SPT;
    adv_data[3] = 0x03; // Length of Service UUID field
    adv_data[4] = ESP_BLE_AD_TYPE_16SRV_CMPL;
    adv_data[5] = 0xAB; // Example Service UUID
    adv_data[6] = 0xCD;
    adv_data[7] = 0x09; // Length of Manufacturer specific data
    adv_data[8] = ESP_BLE_AD_MANUFACTURER_SPECIFIC_TYPE; // Corrected macro name
    esp_efuse_mac_get_default(&adv_data[9]); // Add MAC address to advertisement

    ESP_ERROR_CHECK(esp_ble_gap_config_adv_data_raw(adv_data, ADV_DATA_LEN));

    // Set scan parameters
    esp_ble_scan_params_t scan_params = {
        .scan_type              = BLE_SCAN_TYPE_ACTIVE,
        .own_addr_type          = BLE_ADDR_TYPE_PUBLIC,
        .scan_filter_policy     = BLE_SCAN_FILTER_ALLOW_ALL,
        .scan_interval          = 0x50,
        .scan_window            = 0x30
    };
    ESP_ERROR_CHECK(esp_ble_gap_set_scan_params(&scan_params));

    // Register GAP callback
    ESP_ERROR_CHECK(esp_ble_gap_register_callback(gap_callback));

    ESP_LOGI(TAG, "Advertising and scanning initialized");
}
