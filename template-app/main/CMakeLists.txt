idf_component_register(
    SRCS "main.c"
    INCLUDE_DIRS "."
    REQUIRES nvs_flash bt app_update
    INCLUDE_DIRS
        ${IDF_PATH}/components/bt/include/esp32/include
        ${IDF_PATH}/components/bt/esp_ble_mesh/api/core/include
        ${IDF_PATH}/components/bt/esp_ble_mesh/api
        ${IDF_PATH}/components/bt/esp_ble_mesh/common/include
        ${IDF_PATH}/components/bt/esp_ble_mesh/core/include
        ${IDF_PATH}/components/bt/host/nimble/nimble/nimble/host/mesh/include
)
