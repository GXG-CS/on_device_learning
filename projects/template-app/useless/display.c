#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "device_info.h"
#include "discovery.h"
#include "display.h"

void display_device_info_task(void *pvParameters) {
    while (1) {
        // Display own device info
        create_device_info();

        // Display discovered devices
        for (int i = 0; i < device_count; i++) {
            ESP_LOGI("DEVICE_INFO", "Discovered Device %d: MAC %02X:%02X:%02X:%02X:%02X:%02X",
                     i,
                     devices[i].addr[0], devices[i].addr[1], devices[i].addr[2],
                     devices[i].addr[3], devices[i].addr[4], devices[i].addr[5]);
        }

        // Delay for 3 seconds
        vTaskDelay(pdMS_TO_TICKS(3000));
    }
}
