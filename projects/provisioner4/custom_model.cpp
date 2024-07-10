typedef struct {
    uint8_t  uuid[16];
    uint16_t unicast;
    uint8_t  elem_num;
    uint8_t  onoff;
    uint32_t memory;        // Memory in KB
    uint32_t processing_power; // Processing power in MHz
    // Add other fields as necessary
} esp_ble_mesh_node_info_t;


typedef struct {
    uint32_t memory;
    uint32_t processing_power;
} custom_status_t;

typedef struct {
    esp_ble_mesh_model_t *model;
    esp_ble_mesh_msg_ctx_t *ctx;
    uint32_t opcode;
    uint8_t *data;
    uint16_t length;
} custom_model_cb_param_t;



// ------------------query_node_capabilities-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// Define Custom Model and Operations

// Custom Model Operation Codes
#define OP_NODE_CAPABILITIES_GET 0xC001
#define OP_NODE_CAPABILITIES_STATUS 0xC002

// Define the custom model operations
static const esp_ble_mesh_client_op_pair_t custom_model_op[] = {
    { OP_NODE_CAPABILITIES_GET, 1 },
    { OP_NODE_CAPABILITIES_STATUS, 2 },
};


// Define the custom client model operations
static esp_ble_mesh_model_op_t custom_model_ops[] = {
    ESP_BLE_MESH_MODEL_OP(OP_NODE_CAPABILITIES_STATUS, sizeof(custom_status_t)),
    ESP_BLE_MESH_MODEL_OP_END,
};

static esp_ble_mesh_client_t custom_client = {
    .op_pair = custom_model_op,
    .op_pair_size = ARRAY_SIZE(custom_model_op),
};

// Define the custom model macro
#define ESP_BLE_MESH_MODEL_CUSTOM(cli_pub, cli_data) \
    {                                                \
        .model_id = 0xFFFF,                          \
        .op = custom_model_ops,                      \
        .keys = { ESP_BLE_MESH_KEY_UNUSED },         \
        .pub = cli_pub,                              \
        .user_data = cli_data                        \
    }



// Initialize the root models array
static esp_ble_mesh_model_t root_models[] = {
    ESP_BLE_MESH_MODEL_CFG_SRV(&config_server),
    ESP_BLE_MESH_MODEL_CFG_CLI(&config_client),
    ESP_BLE_MESH_MODEL_GEN_ONOFF_CLI(NULL, &onoff_client),
    ESP_BLE_MESH_MODEL_CUSTOM(NULL, &custom_client) // Use the custom model macro
};


// Send Custom Message
static esp_err_t send_node_capabilities_get(esp_ble_mesh_node_info_t *node)
{
    esp_ble_mesh_client_common_param_t common = {0};
    esp_err_t err;

    ESP_LOGI(TAG, "Entering send_node_capabilities_get for node 0x%04x", node->unicast);

    err = example_ble_mesh_set_msg_common(&common, node, &root_models[3], OP_NODE_CAPABILITIES_GET);
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

    ESP_LOGI(TAG, "Sending node capabilities get message to 0x%04x", node->unicast);
    ESP_LOGI(TAG, "Model: %p, Opcode: 0x%04lx", common.model, (unsigned long)common.opcode);
    ESP_LOGI(TAG, "Context - NetIdx: 0x%04x, AppIdx: 0x%04x, Addr: 0x%04x, TTL: %d",
             common.ctx.net_idx, common.ctx.app_idx, common.ctx.addr, common.ctx.send_ttl);

    err = esp_ble_mesh_client_model_send_msg(&root_models[3], &common.ctx, OP_NODE_CAPABILITIES_GET, payload_size, payload, true, MSG_TIMEOUT, MSG_ROLE);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to send node capabilities get message (err %d)", err);
        ESP_LOGE(TAG, "Model ID: 0x%04x, Opcode: 0x%04lx", root_models[3].model_id, (unsigned long)OP_NODE_CAPABILITIES_GET);
        ESP_LOGE(TAG, "Common parameters - NetIdx: 0x%04x, AppIdx: 0x%04x, Addr: 0x%04x, TTL: %d",
                 common.ctx.net_idx, common.ctx.app_idx, common.ctx.addr, common.ctx.send_ttl);
        ESP_LOG_BUFFER_HEX(TAG, payload, payload_size);
        return err;
    }

    ESP_LOGI(TAG, "Node capabilities get message sent to node 0x%04x", node->unicast);

    ESP_LOGI(TAG, "Exiting send_node_capabilities_get");
    return ESP_OK;
}



// Handle Custom Message Response
static void handle_node_capabilities_status(custom_model_cb_param_t *param)
{
    ESP_LOGI(TAG, "Entering handle_node_capabilities_status");

    if (param->opcode == OP_NODE_CAPABILITIES_STATUS) {
        ESP_LOGI(TAG, "Handling node capabilities status");
        ESP_LOG_BUFFER_HEX(TAG, param->data, param->length);
        if (param->length <= sizeof(custom_status_t)) {
            custom_status_t *status = (custom_status_t *)param->data;
            if (status) {
                esp_ble_mesh_node_info_t *node = example_ble_mesh_get_node_info(param->ctx->addr);
                if (node) {
                    node->memory = status->memory;
                    node->processing_power = status->processing_power;
                    ESP_LOGI(TAG, "Node capabilities - Memory: %" PRIu32 " KB, Processing Power: %" PRIu32 " MHz", status->memory, status->processing_power);
                } else {
                    ESP_LOGE(TAG, "Failed to get node info for address 0x%04x", param->ctx->addr);
                }
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



// Custom model callback function
static void example_ble_mesh_custom_model_cb(esp_ble_mesh_model_cb_event_t event,
                                             esp_ble_mesh_model_cb_param_t *param)
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
            // Handle event code 1
            ESP_LOGI(TAG, "Handling custom event 1");
            // Add handling code here if necessary
            break;

        default:
            ESP_LOGE(TAG, "Unhandled custom model event: %d", event);
            break;
    }
}



esp_ble_mesh_register_custom_model_callback(example_ble_mesh_custom_model_cb);
