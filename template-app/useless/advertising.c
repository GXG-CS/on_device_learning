#include "advertising.h"
#include "esp_log.h"
#include "esp_gap_ble_api.h"
#include "uuid.h"

static const char *TAG = "ADVERTISING";

void start_advertising(void) {
    esp_ble_adv_params_t adv_params = {
        .adv_int_min        = 0x20,
        .adv_int_max        = 0x40,
        .adv_type           = ADV_TYPE_IND,
        .own_addr_type      = BLE_ADDR_TYPE_PUBLIC,
        .channel_map        = ADV_CHNL_ALL,
        .adv_filter_policy  = ADV_FILTER_ALLOW_SCAN_ANY_CON_ANY,
    };

    uint8_t adv_data[] = {
        0x02, 0x01, 0x06, // Flags
        0x03, 0x03, 0xAB, 0xCD, // UUID 16-bit
        0x0A, 0x09, 'E', 'S', 'P', '_', 'D', 'E', 'V', 'I', 'C', 'E' // Device Name
    };

    esp_ble_adv_data_t adv_data_config = {
        .set_scan_rsp = false,
        .include_name = true,
        .include_txpower = true,
        .min_interval = 0x20,
        .max_interval = 0x40,
        .appearance = 0x00,
        .manufacturer_len = 0,
        .p_manufacturer_data = NULL,
        .service_data_len = sizeof(adv_data),
        .p_service_data = adv_data,
        .service_uuid_len = sizeof(adv_data) - 1,
        .p_service_uuid = adv_data + 3,
        .flag = (ESP_BLE_ADV_FLAG_GEN_DISC | ESP_BLE_ADV_FLAG_BREDR_NOT_SPT)
    };

    ESP_ERROR_CHECK(esp_ble_gap_config_adv_data(&adv_data_config));
    ESP_ERROR_CHECK(esp_ble_gap_start_advertising(&adv_params));

    ESP_LOGI(TAG, "Advertising started");
}
