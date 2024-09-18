#ifndef GATTC_INIT_H
#define GATTC_INIT_H


#include "esp_gap_ble_api.h"
#include "esp_gattc_api.h"
#include "esp_gatt_defs.h"
#include "esp_gatt_common_api.h"
#include "esp_log.h"

// Define application profile ID
#define GATTC_TAG "GATTC_INIT"
#define REMOTE_SERVICE_UUID        0x00FF
#define REMOTE_NOTIFY_CHAR_UUID    0xFF01
#define PROFILE_NUM      1
#define PROFILE_A_APP_ID 0
#define INVALID_HANDLE   0

// Device-specific parameters
extern const char remote_device_name[];
extern bool connect;
extern bool get_server;
extern esp_gattc_char_elem_t *char_elem_result;
extern esp_gattc_descr_elem_t *descr_elem_result;

// Structure definition
struct gattc_profile_inst {
    esp_gattc_cb_t gattc_cb;
    uint16_t gattc_if;
    uint16_t app_id;
    uint16_t conn_id;
    uint16_t service_start_handle;
    uint16_t service_end_handle;
    uint16_t char_handle;
    esp_bd_addr_t remote_bda;
};


// Defined GAP and GATTC callback functions
void esp_gap_cb(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t *param);
void esp_gattc_cb(esp_gattc_cb_event_t event, esp_gatt_if_t gattc_if, esp_ble_gattc_cb_param_t *param);
void gattc_profile_event_handler(esp_gattc_cb_event_t event, esp_gatt_if_t gattc_if, esp_ble_gattc_cb_param_t *param);



// Function declarations for GATT client initialization
void gattc_init(void);

#endif // GATTC_INIT_H
