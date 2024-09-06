#!/bin/bash
# Script to load ESP-IDF environment manually

# Set the path to the ESP-IDF directory
ESP_IDF_PATH="$HOME/esp/esp-idf"

# Check if the ESP-IDF directory exists
if [ -d "$ESP_IDF_PATH" ]; then
    . $ESP_IDF_PATH/export.sh
    echo "ESP-IDF environment loaded."
else
    echo "ESP-IDF directory not found at $ESP_IDF_PATH"
fi