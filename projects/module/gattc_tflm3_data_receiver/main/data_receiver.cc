#include "data_receiver.h"
#include "esp_log.h"  // Add this line for ESP logging functions
#include <cstring>
#include <iostream>

// Set a unique tag for this module to identify logs easily
static const char* TAG = "DataReceiver";

// Constructor to initialize the receiver with the specified maximum number of inputs and input size
DataReceiver::DataReceiver(size_t max_inputs_capacity, size_t per_input_size)
    : per_input_size(per_input_size), max_inputs_capacity(max_inputs_capacity) { }

// Destructor to free up allocated resources
DataReceiver::~DataReceiver() {
    // No dynamic allocation needs manual freeing
}

// Function to receive a raw data packet and store it into the current input buffer
bool DataReceiver::receiveDataPacket(const uint8_t* data, size_t length) {
    // Check if the packet can fit into the current input
    if (current_input.size() + length > per_input_size) {
        ESP_LOGE(TAG, "Received packet exceeds input capacity. Dropping packet.");
        return false;
    }

    // Append the received packet into the current input
    current_input.insert(current_input.end(), data, data + length);
    ESP_LOGI(TAG, "Data packet received and stored. Current input size: %d", current_input.size());
    return true;
}

// Check if the current input is complete based on the expected input size
bool DataReceiver::isCurrentInputComplete() const {
    ESP_LOGI(TAG, "Checking if input is complete. Current input size: %d, Expected size: %d", current_input.size(), per_input_size);
    return current_input.size() == per_input_size;
}

// Push the current input into the queue if it is complete
bool DataReceiver::pushCurrentInput() {
    if (!isCurrentInputComplete()) {
        ESP_LOGE(TAG, "Attempt to push incomplete input to queue.");
        return false;
    }
    
    if (isQueueFull()) {
        ESP_LOGE(TAG, "Queue is full: Cannot push more inputs.");
        return false;
    }

    input_queue.push(current_input);  // Add the completed input to the queue
    // ESP_LOGI("DataReceiver", "Input pushed to queue. Queue size after pushing: %d", input_queue.size());

    resetCurrentInput();              // Reset for the next input
    // ESP_LOGI(TAG, "Input successfully pushed to the queue. Queue size: %d", input_queue.size());
    return true;
}

// Retrieve a complete input from the queue
std::vector<uint8_t> DataReceiver::getNextInput() {
    if (input_queue.empty()) {
        return {};  // Return an empty vector if the queue is empty
    }
    std::vector<uint8_t> next_input = input_queue.front();  // Get the next input
    input_queue.pop();  // Remove it from the queue
    return next_input;
}

// Check if the queue has inputs available
bool DataReceiver::hasInput() const {
    return !input_queue.empty();
}

// Reset the current input buffer to prepare for the next input
void DataReceiver::resetCurrentInput() {
    ESP_LOGI("DataReceiver", "Resetting current input buffer. Size before reset: %d", current_input.size());
    current_input.clear();  // Clear the current input buffer
    ESP_LOGI("DataReceiver", "Current input buffer size after reset: %d", current_input.size());

}

// Get the current number of inputs stored in the queue
size_t DataReceiver::getQueueSize() const {
    return input_queue.size();
}

// Check if the queue is full based on the max input capacity
bool DataReceiver::isQueueFull() const {
    return input_queue.size() >= max_inputs_capacity;
}
