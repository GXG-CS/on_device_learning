#include "custom_model.h"
#include "esp_ble_mesh_common_api.h"
#include "esp_ble_mesh_networking_api.h"
#include "esp_ble_mesh_config_model_api.h"
#include "esp_ble_mesh_generic_model_api.h"
#include "esp_log.h"

static const char *TAG = "CUSTOM_MODEL";

// Define the custom model operations
static const esp_ble_mesh_client_op_pair_t custom_model_op[] = {
    { OP_NODE_CAPABILITIES_GET, 1 },
    { OP_NODE_CAPABILITIES_STATUS, 2 },
};

const esp_ble_mesh_model_op_t custom_model_ops[] = {
    ESP_BLE_MESH_MODEL_OP(OP_NODE_CAPABILITIES_STATUS, sizeof(custom_status_t)),
    ESP_BLE_MESH_MODEL_OP_END,
};

// Define the custom client
esp_ble_mesh_client_t custom_client = {
    .op_pair = custom_model_op,
    .op_pair_size = ARRAY_SIZE(custom_model_op),
};

esp_err_t example_ble_mesh_set_msg_common_custom(esp_ble_mesh_client_common_param_t *common, uint16_t net_idx, uint16_t app_idx, uint16_t unicast_addr, uint32_t opcode, esp_ble_mesh_model_t *model)
{
    ESP_LOGI(TAG, "Entering example_ble_mesh_set_msg_common_custom");

    if (!common) {
        ESP_LOGE(TAG, "Invalid argument: common is NULL");
        return ESP_ERR_INVALID_ARG;
    }
    if (!model) {
        ESP_LOGE(TAG, "Invalid argument: model is NULL");
        return ESP_ERR_INVALID_ARG;
    }

    common->opcode = opcode;
    common->model = model;
    common->ctx.net_idx = net_idx;
    common->ctx.app_idx = app_idx;
    common->ctx.addr = unicast_addr;
    common->ctx.send_ttl = 3;  // Set TTL value directly here

    // Set message timeout and role directly here
    common->msg_timeout = 0;
    common->msg_role = ROLE_PROVISIONER;

    ESP_LOGI(TAG, "Common parameters set:");
    ESP_LOGI(TAG, "Opcode: 0x%08lx", (unsigned long)common->opcode);
    ESP_LOGI(TAG, "Model: %p", common->model);
    ESP_LOGI(TAG, "Addr: 0x%04x", common->ctx.addr);
    ESP_LOGI(TAG, "NetIdx: 0x%04x", common->ctx.net_idx);
    ESP_LOGI(TAG, "AppIdx: 0x%04x", common->ctx.app_idx);
    ESP_LOGI(TAG, "TTL: %d", common->ctx.send_ttl);

    ESP_LOGI(TAG, "Exiting example_ble_mesh_set_msg_common_custom");

    return ESP_OK;
}

esp_err_t send_node_capabilities_get(uint16_t net_idx, uint16_t app_idx, uint16_t unicast_addr, esp_ble_mesh_model_t *model)
{
    esp_ble_mesh_client_common_param_t common = {0};
    esp_err_t err;

    ESP_LOGI(TAG, "Entering send_node_capabilities_get for node 0x%04x", unicast_addr);

    err = example_ble_mesh_set_msg_common_custom(&common, net_idx, app_idx, unicast_addr, OP_NODE_CAPABILITIES_GET, model);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to set common message parameters");
        return err;
    }

    uint8_t payload[2] = {0x01, 0x02};
    size_t payload_size = sizeof(payload);

    if (payload_size > 384) {
        ESP_LOGE(TAG, "Payload size too large: %zu", payload_size);
        return ESP_ERR_INVALID_SIZE;
    }

    ESP_LOGI(TAG, "Payload size before sending: %zu", payload_size);
    ESP_LOG_BUFFER_HEX(TAG, payload, payload_size);

    ESP_LOGI(TAG, "Sending node capabilities get message to 0x%04x", unicast_addr);
    ESP_LOGI(TAG, "Model: %p, Opcode: 0x%04lx", common.model, (unsigned long)common.opcode);
    ESP_LOGI(TAG, "Context - NetIdx: 0x%04x, AppIdx: 0x%04x, Addr: 0x%04x, TTL: %d",
             common.ctx.net_idx, common.ctx.app_idx, common.ctx.addr, common.ctx.send_ttl);

    err = esp_ble_mesh_client_model_send_msg(model, &common.ctx, OP_NODE_CAPABILITIES_GET, payload_size, payload, true, common.msg_timeout, common.msg_role);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to send node capabilities get message (err %d)", err);
        ESP_LOGE(TAG, "Model ID: 0x%04x, Opcode: 0x%04lx", model->model_id, (unsigned long)OP_NODE_CAPABILITIES_GET);
        ESP_LOGE(TAG, "Common parameters - NetIdx: 0x%04x, AppIdx: 0x%04x, Addr: 0x%04x, TTL: %d",
                 common.ctx.net_idx, common.ctx.app_idx, common.ctx.addr, common.ctx.send_ttl);
        ESP_LOG_BUFFER_HEX(TAG, payload, payload_size);
        return err;
    }

    ESP_LOGI(TAG, "Node capabilities get message sent to node 0x%04x", unicast_addr);

    ESP_LOGI(TAG, "Exiting send_node_capabilities_get");
    return ESP_OK;
}

void handle_node_capabilities_status(custom_model_cb_param_t *param)
{
    ESP_LOGI(TAG, "Entering handle_node_capabilities_status");

    if (param->opcode == OP_NODE_CAPABILITIES_STATUS) {
        ESP_LOGI(TAG, "Handling node capabilities status");
        ESP_LOG_BUFFER_HEX(TAG, param->data, param->length);
        if (param->length <= sizeof(custom_status_t)) {
            custom_status_t *status = (custom_status_t *)param->data;
            if (status) {
                ESP_LOGI(TAG, "Node capabilities - Memory: %" PRIu32 " KB, Processing Power: %" PRIu32 " MHz", status->memory, status->processing_power);
            } else {
                ESP_LOGE(TAG, "Received status data is NULL");
            }
        } else {
            ESP_LOGE(TAG, "Received payload size is too large: %d", param->length);
        }
    } else {
        ESP_LOGE(TAG, "Unhandled opcode: 0x%08lx", (unsigned long)param->opcode);
    }

    ESP_LOGI(TAG, "Exiting handle_node_capabilities_status");
}

void example_ble_mesh_custom_model_cb(esp_ble_mesh_model_cb_event_t event, esp_ble_mesh_model_cb_param_t *param)
{
    ESP_LOGI(TAG, "Custom model callback event: %d", event);
    ESP_LOGI(TAG, "Model: %p, Opcode: 0x%08lx, Length: %d",
             param->model_operation.model,
             (unsigned long)param->model_operation.opcode,
             param->model_operation.length);

    switch (event) {
        case ESP_BLE_MESH_MODEL_OPERATION_EVT:
            ESP_LOGI(TAG, "Custom model operation event received, opcode: 0x%08lx, length: %d", 
                     (unsigned long)param->model_operation.opcode, param->model_operation.length);

            if (param->model_operation.opcode == OP_NODE_CAPABILITIES_STATUS) {
                custom_model_cb_param_t custom_param = {0};
                custom_param.model = param->model_operation.model;
                custom_param.ctx = param->model_operation.ctx;
                custom_param.opcode = param->model_operation.opcode;
                custom_param.data = param->model_operation.msg;
                custom_param.length = param->model_operation.length;

                ESP_LOGI(TAG, "Node Capabilities Status received, opcode: 0x%08lx, length: %d", 
                         (unsigned long)param->model_operation.opcode, param->model_operation.length);
                ESP_LOG_BUFFER_HEX(TAG, param->model_operation.msg, param->model_operation.length);

                handle_node_capabilities_status(&custom_param);
            } else {
                ESP_LOGE(TAG, "Unhandled custom model opcode: 0x%08lx", (unsigned long)param->model_operation.opcode);
                ESP_LOG_BUFFER_HEX(TAG, param->model_operation.msg, param->model_operation.length);
            }
            break;

        case 1:
            ESP_LOGI(TAG, "Handling custom event 1");
            break;

        default:
            ESP_LOGE(TAG, "Unhandled custom model event: %d", event);
            break;
    }
}
