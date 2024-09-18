#include "esp_log.h"
#include "esp_gap_ble_api.h"
#include "esp_gatts_api.h"
#include "esp_bt_defs.h"
#include "esp_bt_device.h"
#include "esp_gatt_common_api.h"

#define GATTS_TAG "GATTS_INIT"

//Declare the static function
void gatts_profile_a_event_handler(esp_gatts_cb_event_t event, esp_gatt_if_t gatts_if, esp_ble_gatts_cb_param_t *param);
void gatts_profile_b_event_handler(esp_gatts_cb_event_t event, esp_gatt_if_t gatts_if, esp_ble_gatts_cb_param_t *param);

#define GATTS_SERVICE_UUID_TEST_A   0x00FF
#define GATTS_CHAR_UUID_TEST_A      0xFF01
#define GATTS_DESCR_UUID_TEST_A     0x3333
#define GATTS_NUM_HANDLE_TEST_A     4

#define GATTS_SERVICE_UUID_TEST_B   0x00EE
#define GATTS_CHAR_UUID_TEST_B      0xEE01
#define GATTS_DESCR_UUID_TEST_B     0x2222
#define GATTS_NUM_HANDLE_TEST_B     4

// char test_device_name[ESP_BLE_ADV_NAME_LEN_MAX];
// char test_device_name[ESP_BLE_ADV_NAME_LEN_MAX] = "ESP_GATTS_DEMO";


#define TEST_MANUFACTURER_DATA_LEN  17

#define GATTS_DEMO_CHAR_VAL_LEN_MAX 0x40

#define PREPARE_BUF_MAX_SIZE 1024


#define PROFILE_NUM 2
#define PROFILE_A_APP_ID 0
#define PROFILE_B_APP_ID 1

#define adv_config_flag      (1 << 0)
#define scan_rsp_config_flag (1 << 1)


#define TEST_DEVICE_NAME_MAX_LEN 31

struct gatts_profile_inst {
    esp_gatts_cb_t gatts_cb;
    uint16_t gatts_if;
    uint16_t app_id;
    uint16_t conn_id;
    uint16_t service_handle;
    esp_gatt_srvc_id_t service_id;
    uint16_t char_handle;
    esp_bt_uuid_t char_uuid;
    esp_gatt_perm_t perm;
    esp_gatt_char_prop_t property;
    uint16_t descr_handle;
    esp_bt_uuid_t descr_uuid;
};


typedef struct {
    uint8_t                 *prepare_buf;
    int                     prepare_len;
} prepare_type_env_t;


// static prepare_type_env_t a_prepare_write_env;
// static prepare_type_env_t b_prepare_write_env;

extern prepare_type_env_t a_prepare_write_env;
extern prepare_type_env_t b_prepare_write_env;

void example_write_event_env(esp_gatt_if_t gatts_if, prepare_type_env_t *prepare_write_env, esp_ble_gatts_cb_param_t *param);
void example_exec_write_event_env(prepare_type_env_t *prepare_write_env, esp_ble_gatts_cb_param_t *param);

void gatts_init();