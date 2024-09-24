#include "output_handler.h"
#include "tensorflow/lite/micro/micro_log.h"

// Function to handle the model's output
void HandleOutput(const float* output_data, int output_size) {
  // In this case, output_size represents the total number of elements in the output tensor.
  
  // Assume the simplified model has an output feature map of 30x30 with 8 channels.
  // Adjust these values based on the actual output dimensions of your model.
  int output_width = 30;  // Example value, change based on the actual output width
  int output_height = 30; // Example value, change based on the actual output height
  int output_channels = 8; // Example value, change based on the actual number of channels

  // Log the dimensions of the output feature map
  MicroPrintf("Output feature map size: %d x %d x %d", output_width, output_height, output_channels);

  // Process and log a few example values from the output feature map
  for (int i = 0; i < output_channels; ++i) {
    for (int j = 0; j < 3; ++j) { // Log first 3 values in each channel for brevity
      int index = i * output_width * output_height + j;
      MicroPrintf("Channel %d, Value %d: %f", i, j, static_cast<double>(output_data[index]));
    }
  }

  // Example: Apply a global max pooling to reduce the feature map to a single value per channel
  for (int i = 0; i < output_channels; ++i) {
    float max_value = output_data[i * output_width * output_height];
    for (int j = 1; j < output_width * output_height; ++j) {
      int index = i * output_width * output_height + j;
      if (output_data[index] > max_value) {
        max_value = output_data[index];
      }
    }
    MicroPrintf("Channel %d, Max value: %f", i, static_cast<double>(max_value));
  }
}
