#include "gap_handler.h"
#include "esp_log.h"
#include "esp_gap_ble_api.h"

void gap_event_handler(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t *param) {
    switch (event) {
        case ESP_GAP_BLE_ADV_DATA_SET_COMPLETE_EVT:
            ESP_LOGI("GAP_HANDLER", "Advertisement data set");
            break;
        case ESP_GAP_BLE_SCAN_RESULT_EVT:
            ESP_LOGI("GAP_HANDLER", "Scan result event");
            if (param->scan_rst.search_evt == ESP_GAP_SEARCH_INQ_RES_EVT) {
                process_received_device_info(param->scan_rst.ble_adv, param->scan_rst.adv_data_len);
            }
            break;
        default:
            break;
    }
}

void process_received_device_info(const uint8_t *adv_data, uint8_t adv_data_len) {
    char adv_data_str[adv_data_len * 2 + 1];
    for (int i = 0; i < adv_data_len; i++) {
        sprintf(&adv_data_str[i * 2], "%02X", adv_data[i]);
    }
    adv_data_str[adv_data_len * 2] = '\0';
    ESP_LOGI("GAP_HANDLER", "Received device info: %s", adv_data_str);
}
