#ifndef DATA_RECEIVER_H
#define DATA_RECEIVER_H

#include <cstdint>
#include <cstddef>
#include <vector>
#include <queue>

// Class to handle data reception, storage, and queue management for multiple inputs
class DataReceiver {
public:
    // Constructor that initializes the receiver with a specified maximum number of inputs and input size
    DataReceiver(size_t max_inputs_capacity, size_t per_input_size);

    // Destructor to free up allocated resources
    ~DataReceiver();

    // Function to receive a raw data packet and store it into the current input buffer
    bool receiveDataPacket(const uint8_t* data, size_t length);

    // Check if the current input is complete based on the expected input size
    bool isCurrentInputComplete() const;

    // Push the current input into the queue if it is complete
    bool pushCurrentInput();

    // Retrieve a complete input from the queue
    std::vector<uint8_t> getNextInput();

    // Check if the queue has inputs available
    bool hasInput() const;

    // Reset the current input buffer to prepare for the next input
    void resetCurrentInput();

    // Get the current number of inputs stored in the queue
    size_t getQueueSize() const;

    // Check if the queue is full based on the max input capacity
    bool isQueueFull() const;

    // Get the current size of the input being received
    size_t getCurrentInputSize() const;  

private:
    std::queue<std::vector<uint8_t>> input_queue; // Queue to store completed inputs
    std::vector<uint8_t> current_input;           // Buffer for the current input being received
    size_t per_input_size;                        // Expected size of each input
    size_t max_inputs_capacity;                   // Maximum number of inputs the queue can store
};

#endif  // DATA_RECEIVER_H
