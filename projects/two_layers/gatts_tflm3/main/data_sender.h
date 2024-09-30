#ifndef DATA_SENDER_H
#define DATA_SENDER_H

#include <cstdint>
#include <cstddef>
#include <vector>
#include "esp_gatts_api.h"  // For esp_gatt_if_t and other BLE types


// Class to handle sending model outputs through GATT
class DataSender {
public:
    // Constructor to initialize the sender with maximum capacity and output size
    DataSender(size_t max_outputs_capacity, size_t per_output_size);

    // Destructor
    ~DataSender();

    // Function to add an output data to the sender queue
    bool addOutput(const std::vector<uint8_t>& output);

    // Function to get the next output data to be sent
    std::vector<uint8_t> getNextOutput();

    // Check if there is output data available to be sent
    bool hasOutput() const;

    // Remove the sent output from the queue
    bool popOutput();

    // Reset the sender queue for new data
    void resetQueue();

    // Function to send the next output using BLE GATT notification
    bool sendOutput(esp_gatt_if_t gatts_if, uint16_t conn_id, uint16_t char_handle);

    // Get the current size of the queue
    size_t getQueueSize() const;

    // Get the maximum output size allowed in the queue
    size_t getMaxOutputSize() const;

private:
    std::vector<std::vector<uint8_t>> output_queue;  // Queue to store output data
    size_t per_output_size;                          // Size of each output packet
    size_t max_outputs_capacity;                     // Maximum number of outputs that can be stored
};

#endif  // DATA_SENDER_H
