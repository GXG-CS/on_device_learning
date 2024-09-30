#ifndef MODEL_RUNNER_H
#define MODEL_RUNNER_H

#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/recording_micro_interpreter.h"
#include <cstdint>

// ModelRunner class to handle TensorFlow Lite Micro model initialization and inference
class ModelRunner {
public:
    // Constructor with a default tensor arena size of 64KB
    ModelRunner(size_t tensor_arena_size = 64 * 1024);

    // Initialize TFLM model and interpreter
    void initModel();

    // Run inference with the input data (provided each time dynamically)
    template <typename T>
    bool runInference(T* input_data);

    // Function to log the output after inference
    void logOutput();

    ~ModelRunner();  // Destructor to free dynamically allocated memory

private:
    const tflite::Model* model;
    tflite::RecordingMicroInterpreter* interpreter;
    TfLiteTensor* input;   // Single input tensor pointer
    TfLiteTensor* output;  // Single output tensor pointer

    size_t kTensorArenaSize;   // Size of the tensor arena
    uint8_t* tensor_arena;     // Pointer to the tensor arena, allocated dynamically
};

#endif  // MODEL_RUNNER_H
