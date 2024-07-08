#ifndef CUSTOM_MODEL_H
#define CUSTOM_MODEL_H

#include "esp_ble_mesh_defs.h"

// Custom Model Operation Codes
#define OP_NODE_CAPABILITIES_GET 0xC001
#define OP_NODE_CAPABILITIES_STATUS 0xC002

typedef struct {
    uint8_t  uuid[16];
    uint16_t unicast;
    uint8_t  elem_num;
    uint8_t  onoff;
    uint32_t memory;        // Memory in KB
    uint32_t processing_power; // Processing power in MHz
} esp_ble_mesh_node_info_t;

// Custom Status Structure
typedef struct {
    uint32_t memory;
    uint32_t processing_power;
} custom_status_t;

// Custom Model Callback Parameters Structure
typedef struct {
    esp_ble_mesh_model_t *model;
    esp_ble_mesh_msg_ctx_t *ctx;
    uint32_t opcode;
    uint8_t *data;
    uint16_t length;
} custom_model_cb_param_t;

// Custom Model Operations
extern const esp_ble_mesh_model_op_t custom_model_ops[];

// Define the custom client
extern esp_ble_mesh_client_t custom_client;

// Define the custom model macro
#define ESP_BLE_MESH_MODEL_CUSTOM(cli_pub, cli_data) \
    {                                                \
        .model_id = 0xFFFF,                          \
        .op = custom_model_ops,                      \
        .keys = { ESP_BLE_MESH_KEY_UNUSED },         \
        .pub = cli_pub,                              \
        .user_data = cli_data                        \
    }

// Function declarations
esp_err_t send_node_capabilities_get(uint16_t net_idx, uint16_t app_idx, uint16_t unicast_addr, esp_ble_mesh_model_t *model);
void handle_node_capabilities_status(custom_model_cb_param_t *param);
void example_ble_mesh_custom_model_cb(esp_ble_mesh_model_cb_event_t event, esp_ble_mesh_model_cb_param_t *param);

esp_err_t example_ble_mesh_set_msg_common_custom(esp_ble_mesh_client_common_param_t *common, uint16_t net_idx, uint16_t app_idx, uint16_t unicast_addr, uint32_t opcode, esp_ble_mesh_model_t *model);

#endif // CUSTOM_MODEL_H
