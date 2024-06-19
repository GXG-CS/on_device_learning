#include "esp_log.h"
#include "esp_system.h"
#include "esp_mac.h"
#include "esp_chip_info.h"
#include "device_info.h"

static const char *TAG = "DEVICE_INFO";

void create_device_info(void) {
    esp_chip_info_t chip_info;
    esp_chip_info(&chip_info);

    uint8_t mac[6];
    esp_read_mac(mac, ESP_MAC_BT); // Read the MAC address for Bluetooth

    ESP_LOGI(TAG, "Model: %s", "ESP32");
    ESP_LOGI(TAG, "CPU Cores: %d", chip_info.cores);
    ESP_LOGI(TAG, "CPU Revision: %d", chip_info.revision);
    ESP_LOGI(TAG, "Memory Size: %" PRIu32 " KB", esp_get_free_heap_size() / 1024);
    ESP_LOGI(TAG, "MAC Address: %02X:%02X:%02X:%02X:%02X:%02X", mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
}
