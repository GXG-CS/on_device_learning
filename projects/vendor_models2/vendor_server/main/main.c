/* main.c - Application main entry point */

/*
 * SPDX-FileCopyrightText: 2017 Intel Corporation
 * SPDX-FileContributor: 2018-2021 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <stdio.h>
#include <string.h>
#include <inttypes.h>

#include "esp_log.h"
#include "nvs_flash.h"
#include "esp_bt.h"

#include "esp_ble_mesh_defs.h"
#include "esp_ble_mesh_common_api.h"
#include "esp_ble_mesh_networking_api.h"
#include "esp_ble_mesh_provisioning_api.h"
#include "esp_ble_mesh_config_model_api.h"
#include "esp_ble_mesh_local_data_operation_api.h"

#include "board.h"
#include "ble_mesh_example_init.h"

#define TAG "EXAMPLE"

#define CID_ESP     0x02E5

#define ESP_BLE_MESH_VND_MODEL_ID_CLIENT    0x0000
#define ESP_BLE_MESH_VND_MODEL_ID_SERVER    0x0001

#define ESP_BLE_MESH_VND_MODEL_OP_SEND      ESP_BLE_MESH_MODEL_OP_3(0x00, CID_ESP)
#define ESP_BLE_MESH_VND_MODEL_OP_STATUS    ESP_BLE_MESH_MODEL_OP_3(0x01, CID_ESP)
#define ESP_BLE_MESH_VND_MODEL_OP_ACK    ESP_BLE_MESH_MODEL_OP_3(0x02, CID_ESP)  // Define the acknowledgment opcode



//-------------------------------------------------------------------------------------------------------

#include "esp_ble_mesh_networking_api.h"
#include "esp_log.h"

// Model input and output sizes
#define INPUT_SIZE 4

// Define input tensor
float input_data[INPUT_SIZE];

// Function to perform ReLU activation
void relu_activation(float* input, int size) {
    for (int i = 0; i < size; i++) {
        if (input[i] < 0) {
            input[i] = 0;
        }
    }
}


// Define a simple transformation function
void transform_data(float* input, float* output, int size) {
    for (int i = 0; i < size; i++) {
        output[i] = input[i] * 2.0; // Example transformation: scaling the input data by 2
    }
}



#define MSG_SEND_TTL 3 // Define the TTL value




//-----------------------------------------------------------------------------------------------------------



static uint8_t dev_uuid[ESP_BLE_MESH_OCTET16_LEN] = { 0x32, 0x10 };

static esp_ble_mesh_cfg_srv_t config_server = {
    /* 3 transmissions with 20ms interval */
    .net_transmit = ESP_BLE_MESH_TRANSMIT(2, 20),
    .relay = ESP_BLE_MESH_RELAY_DISABLED,
    .relay_retransmit = ESP_BLE_MESH_TRANSMIT(2, 20),
    .beacon = ESP_BLE_MESH_BEACON_ENABLED,
#if defined(CONFIG_BLE_MESH_GATT_PROXY_SERVER)
    .gatt_proxy = ESP_BLE_MESH_GATT_PROXY_ENABLED,
#else
    .gatt_proxy = ESP_BLE_MESH_GATT_PROXY_NOT_SUPPORTED,
#endif
#if defined(CONFIG_BLE_MESH_FRIEND)
    .friend_state = ESP_BLE_MESH_FRIEND_ENABLED,
#else
    .friend_state = ESP_BLE_MESH_FRIEND_NOT_SUPPORTED,
#endif
    .default_ttl = 7,
};

static esp_ble_mesh_model_t root_models[] = {
    ESP_BLE_MESH_MODEL_CFG_SRV(&config_server),
};

static esp_ble_mesh_model_op_t vnd_op[] = {
    ESP_BLE_MESH_MODEL_OP(ESP_BLE_MESH_VND_MODEL_OP_SEND, 2),
    ESP_BLE_MESH_MODEL_OP_END,
};

static esp_ble_mesh_model_t vnd_models[] = {
    ESP_BLE_MESH_VENDOR_MODEL(CID_ESP, ESP_BLE_MESH_VND_MODEL_ID_SERVER,
    vnd_op, NULL, NULL),
};

static esp_ble_mesh_elem_t elements[] = {
    ESP_BLE_MESH_ELEMENT(0, root_models, vnd_models),
};

static esp_ble_mesh_comp_t composition = {
    .cid = CID_ESP,
    .element_count = ARRAY_SIZE(elements),
    .elements = elements,
};

static esp_ble_mesh_prov_t provision = {
    .uuid = dev_uuid,
};

static void prov_complete(uint16_t net_idx, uint16_t addr, uint8_t flags, uint32_t iv_index)
{
    ESP_LOGI(TAG, "net_idx 0x%03x, addr 0x%04x", net_idx, addr);
    ESP_LOGI(TAG, "flags 0x%02x, iv_index 0x%08" PRIx32, flags, iv_index);
    board_led_operation(LED_G, LED_OFF);
}

static void example_ble_mesh_provisioning_cb(esp_ble_mesh_prov_cb_event_t event,
                                             esp_ble_mesh_prov_cb_param_t *param)
{
    switch (event) {
    case ESP_BLE_MESH_PROV_REGISTER_COMP_EVT:
        ESP_LOGI(TAG, "ESP_BLE_MESH_PROV_REGISTER_COMP_EVT, err_code %d", param->prov_register_comp.err_code);
        break;
    case ESP_BLE_MESH_NODE_PROV_ENABLE_COMP_EVT:
        ESP_LOGI(TAG, "ESP_BLE_MESH_NODE_PROV_ENABLE_COMP_EVT, err_code %d", param->node_prov_enable_comp.err_code);
        break;
    case ESP_BLE_MESH_NODE_PROV_LINK_OPEN_EVT:
        ESP_LOGI(TAG, "ESP_BLE_MESH_NODE_PROV_LINK_OPEN_EVT, bearer %s",
            param->node_prov_link_open.bearer == ESP_BLE_MESH_PROV_ADV ? "PB-ADV" : "PB-GATT");
        break;
    case ESP_BLE_MESH_NODE_PROV_LINK_CLOSE_EVT:
        ESP_LOGI(TAG, "ESP_BLE_MESH_NODE_PROV_LINK_CLOSE_EVT, bearer %s",
            param->node_prov_link_close.bearer == ESP_BLE_MESH_PROV_ADV ? "PB-ADV" : "PB-GATT");
        break;
    case ESP_BLE_MESH_NODE_PROV_COMPLETE_EVT:
        ESP_LOGI(TAG, "ESP_BLE_MESH_NODE_PROV_COMPLETE_EVT");
        prov_complete(param->node_prov_complete.net_idx, param->node_prov_complete.addr,
            param->node_prov_complete.flags, param->node_prov_complete.iv_index);
        break;
    case ESP_BLE_MESH_NODE_PROV_RESET_EVT:
        ESP_LOGI(TAG, "ESP_BLE_MESH_NODE_PROV_RESET_EVT");
        break;
    case ESP_BLE_MESH_NODE_SET_UNPROV_DEV_NAME_COMP_EVT:
        ESP_LOGI(TAG, "ESP_BLE_MESH_NODE_SET_UNPROV_DEV_NAME_COMP_EVT, err_code %d", param->node_set_unprov_dev_name_comp.err_code);
        break;
    default:
        break;
    }
}

static void example_ble_mesh_config_server_cb(esp_ble_mesh_cfg_server_cb_event_t event,
                                              esp_ble_mesh_cfg_server_cb_param_t *param)
{
    if (event == ESP_BLE_MESH_CFG_SERVER_STATE_CHANGE_EVT) {
        switch (param->ctx.recv_op) {
        case ESP_BLE_MESH_MODEL_OP_APP_KEY_ADD:
            ESP_LOGI(TAG, "ESP_BLE_MESH_MODEL_OP_APP_KEY_ADD");
            ESP_LOGI(TAG, "net_idx 0x%04x, app_idx 0x%04x",
                param->value.state_change.appkey_add.net_idx,
                param->value.state_change.appkey_add.app_idx);
            ESP_LOG_BUFFER_HEX("AppKey", param->value.state_change.appkey_add.app_key, 16);
            break;
        case ESP_BLE_MESH_MODEL_OP_MODEL_APP_BIND:
            ESP_LOGI(TAG, "ESP_BLE_MESH_MODEL_OP_MODEL_APP_BIND");
            ESP_LOGI(TAG, "elem_addr 0x%04x, app_idx 0x%04x, cid 0x%04x, mod_id 0x%04x",
                param->value.state_change.mod_app_bind.element_addr,
                param->value.state_change.mod_app_bind.app_idx,
                param->value.state_change.mod_app_bind.company_id,
                param->value.state_change.mod_app_bind.model_id);
            break;
        default:
            break;
        }
    }
}

// static void example_ble_mesh_custom_model_cb(esp_ble_mesh_model_cb_event_t event,
//                                              esp_ble_mesh_model_cb_param_t *param)
// {
//     switch (event) {
//     case ESP_BLE_MESH_MODEL_OPERATION_EVT:
//         if (param->model_operation.opcode == ESP_BLE_MESH_VND_MODEL_OP_SEND) {
//             uint16_t tid = *(uint16_t *)param->model_operation.msg;
//             ESP_LOGI(TAG, "Recv 0x%06" PRIx32 ", tid 0x%04x", param->model_operation.opcode, tid);
//             esp_err_t err = esp_ble_mesh_server_model_send_msg(&vnd_models[0],
//                     param->model_operation.ctx, ESP_BLE_MESH_VND_MODEL_OP_STATUS,
//                     sizeof(tid), (uint8_t *)&tid);
//             if (err) {
//                 ESP_LOGE(TAG, "Failed to send message 0x%06x", ESP_BLE_MESH_VND_MODEL_OP_STATUS);
//             }
//         }
//         break;
//     case ESP_BLE_MESH_MODEL_SEND_COMP_EVT:
//         if (param->model_send_comp.err_code) {
//             ESP_LOGE(TAG, "Failed to send message 0x%06" PRIx32, param->model_send_comp.opcode);
//             break;
//         }
//         ESP_LOGI(TAG, "Send 0x%06" PRIx32, param->model_send_comp.opcode);
//         break;
//     default:
//         break;
//     }
// }


static void example_ble_mesh_custom_model_cb(esp_ble_mesh_model_cb_event_t event,
                                             esp_ble_mesh_model_cb_param_t *param)
{
    float transformed_data[INPUT_SIZE]; // Array to store transformed data

    switch (event) {
    case ESP_BLE_MESH_MODEL_OPERATION_EVT:
        if (param->model_operation.opcode == ESP_BLE_MESH_VND_MODEL_OP_SEND) {
            ESP_LOGI(TAG, "Received vendor model message 0x%06" PRIx32, param->model_operation.opcode);

            // Assuming the message length matches the expected tensor size
            if (param->model_operation.length == INPUT_SIZE * sizeof(float)) {
                memcpy(input_data, param->model_operation.msg, param->model_operation.length);

                // Log the received data from the client
                ESP_LOGI(TAG, "Received from client:");
                for (int i = 0; i < INPUT_SIZE; i++) {
                    ESP_LOGI(TAG, "Input[%d]: %f", i, input_data[i]);
                }

                // Perform ReLU activation
                relu_activation(input_data, INPUT_SIZE);

                // Log the data after ReLU activation
                ESP_LOGI(TAG, "After ReLU activation:");
                for (int i = 0; i < INPUT_SIZE; i++) {
                    ESP_LOGI(TAG, "Input[%d]: %f", i, input_data[i]);
                }

                // Apply transformation to the data
                transform_data(input_data, transformed_data, INPUT_SIZE);

                // Log the data after transformation
                ESP_LOGI(TAG, "After transformation:");
                for (int i = 0; i < INPUT_SIZE; i++) {
                    ESP_LOGI(TAG, "Output[%d]: %f", i, transformed_data[i]);
                }

                // Send acknowledgment back to the client
                ESP_LOGI(TAG, "Preparing to send acknowledgment to client...");

                // Send acknowledgment back to the client
                esp_ble_mesh_msg_ctx_t ctx = {
                    .net_idx = param->model_operation.ctx->net_idx,
                    .app_idx = param->model_operation.ctx->app_idx,
                    .addr = param->model_operation.ctx->addr,
                    .send_ttl = MSG_SEND_TTL,
                    .recv_dst = param->model_operation.ctx->recv_dst,
                    .recv_rssi = param->model_operation.ctx->recv_rssi,
                    .recv_ttl = param->model_operation.ctx->recv_ttl,
                };
                uint32_t ack_opcode = ESP_BLE_MESH_VND_MODEL_OP_ACK;
                ESP_LOGI(TAG, "Sending acknowledgment to client with opcode 0x%06" PRIx32, ack_opcode);


                esp_err_t err = esp_ble_mesh_server_model_send_msg(param->model_operation.model, &ctx, ack_opcode,
                        sizeof(transformed_data), (uint8_t *)transformed_data);
                if (err != ESP_OK) {
                    ESP_LOGE(TAG, "Failed to send acknowledgment 0x%06" PRIx32, ack_opcode);
                } else {
                    ESP_LOGI(TAG, "Sent to client:");
                    for (int i = 0; i < INPUT_SIZE; i++) {
                        ESP_LOGI(TAG, "Output[%d]: %f", i, transformed_data[i]);
                    }
                    ESP_LOGI(TAG, "Message sent successfully, waiting for client to process...");
                }

            } else {
                ESP_LOGE(TAG, "Unexpected message length: %d", param->model_operation.length);
            }
        }
        break;
    case ESP_BLE_MESH_MODEL_SEND_COMP_EVT:
        if (param->model_send_comp.err_code) {
            ESP_LOGE(TAG, "Failed to send message 0x%06" PRIx32, param->model_send_comp.opcode);
        } else {
            ESP_LOGI(TAG, "Sent vendor message 0x%06" PRIx32, param->model_send_comp.opcode);
        }
        break;
    case ESP_BLE_MESH_CLIENT_MODEL_RECV_PUBLISH_MSG_EVT:
        ESP_LOGI(TAG, "Receive publish message 0x%06" PRIx32, param->client_recv_publish_msg.opcode);
        break;
    case ESP_BLE_MESH_CLIENT_MODEL_SEND_TIMEOUT_EVT:
        ESP_LOGW(TAG, "Client message 0x%06" PRIx32 " timeout", param->client_send_timeout.opcode);
        break;
    default:
        ESP_LOGE(TAG, "Invalid custom model event %u", event);
        break;
    }
}







static esp_err_t ble_mesh_init(void)
{
    esp_err_t err;

    esp_ble_mesh_register_prov_callback(example_ble_mesh_provisioning_cb);
    esp_ble_mesh_register_config_server_callback(example_ble_mesh_config_server_cb);
    esp_ble_mesh_register_custom_model_callback(example_ble_mesh_custom_model_cb);

    err = esp_ble_mesh_init(&provision, &composition);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to initialize mesh stack");
        return err;
    }

    err = esp_ble_mesh_node_prov_enable((esp_ble_mesh_prov_bearer_t)(ESP_BLE_MESH_PROV_ADV | ESP_BLE_MESH_PROV_GATT));
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to enable mesh node");
        return err;
    }

    board_led_operation(LED_G, LED_ON);

    ESP_LOGI(TAG, "BLE Mesh Node initialized");

    return ESP_OK;
}

void app_main(void)
{
    esp_err_t err;

    ESP_LOGI(TAG, "Initializing...");

    err = nvs_flash_init();
    if (err == ESP_ERR_NVS_NO_FREE_PAGES) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        err = nvs_flash_init();
    }
    ESP_ERROR_CHECK(err);

    board_init();

    err = bluetooth_init();
    if (err) {
        ESP_LOGE(TAG, "esp32_bluetooth_init failed (err %d)", err);
        return;
    }

    ble_mesh_get_dev_uuid(dev_uuid);

    /* Initialize the Bluetooth Mesh Subsystem */
    err = ble_mesh_init();
    if (err) {
        ESP_LOGE(TAG, "Bluetooth mesh init failed (err %d)", err);
    }
}
