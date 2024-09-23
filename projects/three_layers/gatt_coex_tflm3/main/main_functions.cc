/* Copyright 2020 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/micro/recording_micro_interpreter.h"  // Include the recording interpreter


#include "main_functions.h"
#include "model_data.h"
#include "output_handler.h"

// Globals, used for compatibility with Arduino-style sketches.
namespace {
const tflite::Model* model = nullptr;
// tflite::MicroInterpreter* interpreter = nullptr;
tflite::RecordingMicroInterpreter* interpreter = nullptr;  // Change to RecordingMicroInterpreter

TfLiteTensor* input = nullptr;
TfLiteTensor* output = nullptr;

constexpr int kTensorArenaSize = 64 * 1024;  // Reduced size for small model
uint8_t tensor_arena[kTensorArenaSize];
}  // namespace

// The name of this function is important for Arduino compatibility.
void setup() {
  // Map the model into a usable data structure. This doesn't involve any
  // copying or parsing, it's a very lightweight operation.
  model = tflite::GetModel(g_model);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    MicroPrintf("Model provided is schema version %d not equal to supported "
                "version %d.", model->version(), TFLITE_SCHEMA_VERSION);
    return;
  }

  // Pull in only the operation implementations needed for the simplified model.
  static tflite::MicroMutableOpResolver<5> resolver;
  resolver.AddConv2D();      // Add Conv2D for simple model
  resolver.AddReshape();     // Add Reshape operation if needed
  resolver.AddFullyConnected(); // Add FC layer if present
  resolver.AddSoftmax();     // Add Softmax if used in output
  
  // // Build an interpreter to run the model with.
  // static tflite::MicroInterpreter static_interpreter(
  //     model, resolver, tensor_arena, kTensorArenaSize);
  // interpreter = &static_interpreter;

    // Build a recording interpreter to run the model with and record memory usage.
  static tflite::RecordingMicroInterpreter static_interpreter(
      model, resolver, tensor_arena, kTensorArenaSize);
  interpreter = &static_interpreter;

  // Allocate memory from the tensor_arena for the model's tensors.
  TfLiteStatus allocate_status = interpreter->AllocateTensors();
  if (allocate_status != kTfLiteOk) {
    MicroPrintf("AllocateTensors() failed");
    return;
  }

  // Log initial memory allocations after setup
  MicroPrintf("Memory info after setup:");
  interpreter->GetMicroAllocator().PrintAllocations();

  // Obtain pointers to the model's input and output tensors.
  input = interpreter->input(0);
  output = interpreter->output(0);

  // Log memory allocations
  // interpreter->GetMicroAllocator().PrintAllocations();
}

// Loop function to run inference
void loop() {
  // Prepare input data (example with all zeros)
  for (int i = 0; i < input->dims->data[1] * input->dims->data[2] * input->dims->data[3]; ++i) {
    input->data.f[i] = 0.0f;  // Replace this with actual data input logic
  }

  // Run inference
  TfLiteStatus invoke_status = interpreter->Invoke();
  if (invoke_status != kTfLiteOk) {
    MicroPrintf("Invoke failed");
    return;
  }

  // Log memory usage after each inference
  MicroPrintf("Memory info after inference:");
  interpreter->GetMicroAllocator().PrintAllocations();

  // Process output (example of reading values from output tensor)
  // for (int i = 0; i < output->dims->data[1]; ++i) {
  //   float value = output->data.f[i];
  //   // Process the output value as needed
  // }

  // Example: handle output using a custom function
  // HandleOutput(output->data.f, output->dims->data[1]);
  
}
