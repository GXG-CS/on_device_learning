#include "output_handler.h"
#include "tensorflow/lite/micro/micro_log.h"

// Modify this to match the number of classes in your model
constexpr int kNumberOfClasses = 10;

// Class labels for MNIST (0-9)
const char* kClassLabels[kNumberOfClasses] = {
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
};

// Function to handle the model's output
void HandleOutput(const float* output_data, int output_size) {
  // Ensure the output size matches the expected number of classes
  if (output_size != kNumberOfClasses) {
    MicroPrintf("Unexpected output size: %d", output_size);
    return;
  }

  // Find the class with the highest probability
  int predicted_class = 0;
  float max_probability = output_data[0];
  for (int i = 1; i < output_size; ++i) {
    if (output_data[i] > max_probability) {
      max_probability = output_data[i];
      predicted_class = i;
    }
  }

  // Log the predicted class and its probability
  MicroPrintf("Predicted class: %s, Probability: %f",
              kClassLabels[predicted_class],
              static_cast<double>(max_probability));

  // Optional: Log all class probabilities
  for (int i = 0; i < output_size; ++i) {
    MicroPrintf("Class %s: %f", kClassLabels[i], static_cast<double>(output_data[i]));
  }
}
