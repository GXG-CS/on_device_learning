/*
 * SPDX-FileCopyrightText: 2017 Intel Corporation
 * SPDX-FileContributor: 2018-2021 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Apache-2.0
 */

// #include <stdio.h>
// #include <string.h>
// #include <inttypes.h>

#include "esp_system.h"
#include "esp_log.h"
#include "nvs_flash.h"

#include "ble_mesh_fast_prov.h"
#include "node_info.h"
// #include "ble_comm_service.h"



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

    err = bluetooth_init();
    if (err) {
        ESP_LOGE(TAG, "esp32_bluetooth_init failed (err %d)", err);
        return;
    }

    ble_mesh_get_dev_uuid(dev_uuid);

    /* Initialize the Bluetooth Mesh Subsystem */
    err = ble_mesh_init();
    if (err) {
        ESP_LOGE(TAG, "Failed to initialize BLE Mesh (err %d)", err);
    }

    // // Initialize BLE Communication for node info transfer
    // err = ble_comm_service_init();
    // if (err) {
    //     ESP_LOGE(TAG, "Failed to initialize BLE communication (err %d)", err);
    //     return;
    // }

    // node info
    print_node_info();

    // // Periodically send node info
    // while (1) {
    //     ble_comm_service_send_node_info();
    //     vTaskDelay(5000 / portTICK_PERIOD_MS);
    // }

}