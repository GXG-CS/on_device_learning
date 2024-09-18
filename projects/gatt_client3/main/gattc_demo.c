#include "nvs.h"
#include "nvs_flash.h"
#include "esp_bt.h"
#include "esp_bt_main.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"

#include "gattc_init.h"

#include "esp_task_wdt.h"


void app_main(void)
{
     // Initialize Task Watchdog to disable it
    esp_task_wdt_config_t twdt_config = {
        .timeout_ms = 0,      // Set timeout to 0 to disable
        .idle_core_mask = 0,  // Disable on all cores
        .trigger_panic = false // Don't trigger a panic
    };
    
    esp_err_t ret_w = esp_task_wdt_init(&twdt_config);
    if (ret_w != ESP_OK) {
        printf("Failed to initialize Task Watchdog, error: %s\n", esp_err_to_name(ret_w));
    }


    // Initialize NVS.
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK( ret );

    ESP_ERROR_CHECK(esp_bt_controller_mem_release(ESP_BT_MODE_CLASSIC_BT));

    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
    ret = esp_bt_controller_init(&bt_cfg);
    if (ret) {
        ESP_LOGE(GATTC_TAG, "%s initialize controller failed: %s", __func__, esp_err_to_name(ret));
        return;
    }

    ret = esp_bt_controller_enable(ESP_BT_MODE_BLE);
    if (ret) {
        ESP_LOGE(GATTC_TAG, "%s enable controller failed: %s", __func__, esp_err_to_name(ret));
        return;
    }

    ret = esp_bluedroid_init();
    if (ret) {
        ESP_LOGE(GATTC_TAG, "%s init bluetooth failed: %s", __func__, esp_err_to_name(ret));
        return;
    }

    ret = esp_bluedroid_enable();
    if (ret) {
        ESP_LOGE(GATTC_TAG, "%s enable bluetooth failed: %s", __func__, esp_err_to_name(ret));
        return;
    }

   
    // Define the GATT client configuration struct
    static gattc_init_config_t config = {
        .remote_device_name = "ESP_GATTS_DEMO",  // Device name
        .remote_filter_service_uuid = {          // Remote service UUID
            .len = ESP_UUID_LEN_16,
            .uuid = {.uuid16 = 0x00FF},          // Example service UUID
        },
        .remote_filter_char_uuid = {             // Remote characteristic UUID
            .len = ESP_UUID_LEN_16,
            .uuid = {.uuid16 = 0xFF01},          // Example characteristic UUID
        },
        .notify_descr_uuid = {                   // Notify descriptor UUID (CCCD)
            .len = ESP_UUID_LEN_16,
            .uuid = {.uuid16 = ESP_GATT_UUID_CHAR_CLIENT_CONFIG},  // 0x2902
        },
        .ble_scan_params = {                     // Scan parameters
            .scan_type = BLE_SCAN_TYPE_ACTIVE,
            .own_addr_type = BLE_ADDR_TYPE_PUBLIC,
            .scan_filter_policy = BLE_SCAN_FILTER_ALLOW_ALL,
            .scan_interval = 0x50,
            .scan_window = 0x30,
            .scan_duplicate = BLE_SCAN_DUPLICATE_DISABLE,
        },

    };



    gattc_init(&config);
}
