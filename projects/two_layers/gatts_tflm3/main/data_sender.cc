#include "data_sender.h"
#include <esp_log.h>

// Define the tag for logging
#define DATA_SENDER_TAG "DataSender"

// Constructor to initialize DataSender with specified capacity and output size
DataSender::DataSender(size_t max_outputs_capacity, size_t per_output_size)
    : per_output_size(per_output_size), max_outputs_capacity(max_outputs_capacity)  // Correct the initialization order
{
    // Reserve space in the queue based on maximum capacity
    output_queue.reserve(max_outputs_capacity);
}
// Destructor to clean up dynamically allocated memory if necessary
DataSender::~DataSender() {}

// Function to add an output data to the sender queue
bool DataSender::addOutput(const std::vector<uint8_t>& output) {
    if (output.size() != per_output_size) {
        ESP_LOGE(DATA_SENDER_TAG, "Output size mismatch. Expected: %d, Provided: %d", per_output_size, output.size());
        return false;
    }

    if (output_queue.size() >= max_outputs_capacity) {
        ESP_LOGE(DATA_SENDER_TAG, "Output queue is full. Cannot add new output.");
        return false;
    }

    output_queue.push_back(output);
    ESP_LOGI(DATA_SENDER_TAG, "Output added to the queue. Current queue size: %d", getQueueSize());
    return true;
}

// Function to get the next output data to be sent
std::vector<uint8_t> DataSender::getNextOutput() {
    if (output_queue.empty()) {
        ESP_LOGW(DATA_SENDER_TAG, "No output data available in the queue.");
        return std::vector<uint8_t>();  // Return an empty vector
    }
    return output_queue.front();  // Return the first element in the queue
}

// Check if there is output data available to be sent
bool DataSender::hasOutput() const {
    return !output_queue.empty();
}

// Remove the sent output from the queue
bool DataSender::popOutput() {
    if (output_queue.empty()) {
        ESP_LOGW(DATA_SENDER_TAG, "No output data to pop from the queue.");
        return false;
    }
    output_queue.erase(output_queue.begin());  // Remove the first element in the queue
    ESP_LOGI(DATA_SENDER_TAG, "Output popped from the queue. Current queue size: %d", getQueueSize());
    return true;
}

// Reset the sender queue for new data
void DataSender::resetQueue() {
    ESP_LOGI(DATA_SENDER_TAG, "Resetting the output queue. Current size before reset: %d", getQueueSize());
    output_queue.clear();
    ESP_LOGI(DATA_SENDER_TAG, "Output queue reset. Current size after reset: %d", getQueueSize());
}

// Get the current size of the queue
size_t DataSender::getQueueSize() const {
    return output_queue.size();
}

// Get the maximum output size allowed in the queue
size_t DataSender::getMaxOutputSize() const {
    return per_output_size;
}

// Send the next output using BLE GATT notification
bool DataSender::sendOutput(esp_gatt_if_t gatts_if, uint16_t conn_id, uint16_t char_handle) {
    if (!hasOutput()) {
        ESP_LOGW(DATA_SENDER_TAG, "No output data available to send.");
        return false;
    }

    std::vector<uint8_t> output = getNextOutput();

    // Send the notification using the provided GATT parameters
    esp_err_t ret = esp_ble_gatts_send_indicate(gatts_if, conn_id, char_handle, output.size(), output.data(), false);  // false indicates non-confirmed notification
    if (ret != ESP_OK) {
        ESP_LOGE(DATA_SENDER_TAG, "Failed to send output notification, error code = %x", ret);
        return false;
    }

    ESP_LOGI(DATA_SENDER_TAG, "Output sent successfully. Removing from queue.");
    return popOutput();  // Remove the sent output from the queue
}


