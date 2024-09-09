#ifndef BLE_MESH_PROVISIONER_H
#define BLE_MESH_PROVISIONER_H

#include "esp_err.h"


#define TAG "ble_mesh_provisioner"

#define LED_OFF             0x0
#define LED_ON              0x1

#define CID_ESP             0x02E5

#define PROV_OWN_ADDR       0x0001

#define MSG_SEND_TTL        3
#define MSG_TIMEOUT         0
#define MSG_ROLE            ROLE_PROVISIONER

#define COMP_DATA_PAGE_0    0x00

#define APP_KEY_IDX         0x0000
#define APP_KEY_OCTET       0x12

/**
 * @brief UUID of the device.
 *
 * This array holds the UUID of the provisioner device. It can be accessed by other files, including main.c.
 */
extern uint8_t dev_uuid[16];

/**
 * @brief Initializes BLE Mesh provisioner.
 * 
 * This function initializes the BLE Mesh stack and sets up the provisioner role.
 * It handles the provisioning, configuration, and setting up of the mesh network.
 *
 * @return esp_err_t ESP_OK on success or an error code on failure.
 */
esp_err_t ble_mesh_init(void);

#endif /* BLE_MESH_PROVISIONER_H */
