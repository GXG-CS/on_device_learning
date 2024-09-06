// ble_mesh_fast_prov.h
#ifndef BLE_MESH_FAST_PROV_H
#define BLE_MESH_FAST_PROV_H

#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <inttypes.h>

#include "esp_ble_mesh_defs.h"
#include "esp_ble_mesh_common_api.h"
#include "esp_ble_mesh_provisioning_api.h"
#include "esp_ble_mesh_networking_api.h"
#include "esp_ble_mesh_config_model_api.h"
#include "esp_ble_mesh_generic_model_api.h"

#include "ble_mesh_fast_prov_common.h"
#include "ble_mesh_fast_prov_operation.h"
#include "ble_mesh_fast_prov_client_model.h"
#include "ble_mesh_example_init.h"

#define TAG "EXAMPLE"

#define PROV_OWN_ADDR       0x0001
#define APP_KEY_OCTET       0x12
#define GROUP_ADDRESS       0xC000


// extern uint8_t dev_uuid[16] = { 0xdd, 0xdd };
// extern uint8_t match[] = { 0xdd, 0xdd };
extern uint8_t dev_uuid[16];
extern uint8_t match[2];


esp_err_t ble_mesh_init(void);


#endif // BLE_MESH_FAST_PROV_H