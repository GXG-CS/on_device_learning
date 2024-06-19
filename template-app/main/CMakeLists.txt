idf_component_register(
    SRCS "init.c" "main.c" "device_info.c"
    INCLUDE_DIRS "." "../include"
    REQUIRES nvs_flash bt app_update json esp_timer mbedtls
)
