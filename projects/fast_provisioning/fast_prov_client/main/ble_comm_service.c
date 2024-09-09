#include "ble_comm_service.h"
#include "esp_gatts_api.h"
#include "esp_gap_ble_api.h"
#include "esp_bt_main.h"
#include "node_info.h"
#include <string.h>
#include "esp_log.h" 

#define TAG "BLE_COMM_SERVICE"

#define GATTS_DEMO_CHAR_VAL_LEN_MAX 100

static uint16_t service_handle = 0;
static uint16_t char_handle = 0;

static esp_gatt_char_prop_t char_property = 0;
static esp_gatt_if_t global_gatts_if;

static const uint16_t primary_service_uuid = ESP_GATT_UUID_PRI_SERVICE;
static const uint16_t character_declaration_uuid = ESP_GATT_UUID_CHAR_DECLARE;

// GATT database definition
static esp_gatts_attr_db_t gatt_db[] = {
    // Custom Service Declaration
// Custom Service Declaration
[0] = {
    {ESP_GATT_AUTO_RSP}, 
    {ESP_UUID_LEN_16, (uint8_t *)&primary_service_uuid, ESP_GATT_PERM_READ,
    sizeof(uint16_t), sizeof(CUSTOM_SERVICE_UUID), (uint8_t *)CUSTOM_SERVICE_UUID}
},
// Characteristic Declaration
[1] = {
    {ESP_GATT_AUTO_RSP}, 
    {ESP_UUID_LEN_16, (uint8_t *)&character_declaration_uuid, ESP_GATT_PERM_READ,
    sizeof(uint8_t), sizeof(char_property), &char_property}
},
// Characteristic Value
[2] = {
    {ESP_GATT_AUTO_RSP}, 
    {ESP_UUID_LEN_16, (uint8_t *)CUSTOM_CHARACTERISTIC_UUID, ESP_GATT_PERM_READ | ESP_GATT_PERM_WRITE, 
    GATTS_DEMO_CHAR_VAL_LEN_MAX, sizeof(uint8_t), NULL}
}

};

// GATT profile event handler
static void gatts_profile_event_handler(esp_gatts_cb_event_t event, 
                                        esp_gatt_if_t gatts_if, 
                                        esp_ble_gatts_cb_param_t *param) {
    switch (event) {
        case ESP_GATTS_REG_EVT:
            esp_ble_gatts_create_attr_tab(gatt_db, gatts_if, 3, 0);
            break;

        case ESP_GATTS_CREAT_ATTR_TAB_EVT: {
            if (param->add_attr_tab.status != ESP_GATT_OK) {
                ESP_LOGE(TAG, "Failed to create attribute table, error code: %x", param->add_attr_tab.status);
                return;
            }
            esp_ble_gatts_start_service(service_handle);
            char_handle = param->add_attr_tab.handles[2];
            break;
        }

        case ESP_GATTS_WRITE_EVT: {
            ESP_LOGI(TAG, "Characteristic written.");
            break;
        }

        default:
            break;
    }
}

// Function to initialize BLE communication service
esp_err_t ble_comm_service_init(void) {
    esp_err_t err;

    char_property = ESP_GATT_CHAR_PROP_BIT_READ | ESP_GATT_CHAR_PROP_BIT_WRITE | ESP_GATT_CHAR_PROP_BIT_NOTIFY;

    err = esp_ble_gatts_register_callback(gatts_profile_event_handler);
    if (err) {
        ESP_LOGE(TAG, "Failed to register GATT callback: %d", err);
        return err;
    }

    err = esp_ble_gatts_app_register(0);
    if (err) {
        ESP_LOGE(TAG, "Failed to register GATT app: %d", err);
        return err;
    }

    ESP_LOGI(TAG, "BLE communication service initialized.");
    return ESP_OK;
}

// Function to send node information via BLE
esp_err_t ble_comm_service_send_node_info(void) {
    uint8_t uuid[6] = {0};
    uint32_t free_dram = get_free_dram();
    char data_buffer[100];

    // Get UUID (MAC Address)
    get_node_uuid(uuid);

    // Prepare data to send
    snprintf(data_buffer, sizeof(data_buffer), "UUID: %02X:%02X:%02X:%02X:%02X:%02X, Free DRAM: %lu bytes",
             uuid[0], uuid[1], uuid[2], uuid[3], uuid[4], uuid[5], (unsigned long)free_dram);

    // Send data via GATT
    esp_err_t err = esp_ble_gatts_send_indicate(global_gatts_if, 0, char_handle, strlen(data_buffer), (uint8_t *)data_buffer, false);
    if (err) {
        ESP_LOGE(TAG, "Failed to send node info via BLE: %d", err);
        return err;
    }

    ESP_LOGI(TAG, "Node info successfully sent via BLE.");
    return ESP_OK;
}
