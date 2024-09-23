#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "model_data.h"  // Contains your model data in binary form

// Model data and tensor arena settings
constexpr int kTensorArenaSize = 64 * 1024;  // Tentative size, adjust as needed
uint8_t tensor_arena[kTensorArenaSize];

// Function to calculate total memory usage
void CalculateMemoryUsage() {
  // Load the TFLite model
  const tflite::Model* model = tflite::GetModel(g_model_data);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    printf("Model schema version mismatch!\n");
    return;
  }

  // Set up an operator resolver
  static tflite::MicroMutableOpResolver<5> resolver;
  resolver.AddConv2D();
  resolver.AddFullyConnected();
  resolver.AddSoftmax();
  // Add other necessary operators here

  // Set up the interpreter
  tflite::MicroInterpreter interpreter(model, resolver, tensor_arena, kTensorArenaSize);

  // Allocate memory for the tensors
  TfLiteStatus allocate_status = interpreter.AllocateTensors();
  if (allocate_status != kTfLiteOk) {
    printf("Memory allocation failed!\n");
    return;
  }

  // Output the total memory used in the arena
  printf("Total memory allocated: %d bytes\n", kTensorArenaSize);
}

int main() {
  tflite::InitializeTarget();  // TFLM initialization
  CalculateMemoryUsage();      // Calculate total memory required
  return 0;
}
