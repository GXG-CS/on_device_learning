#include "model_runner.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "model_data.h"
#include <cstring>
#include "esp_log.h"

#define ModelRunner_TAG "ModelRunner"

// Constructor: initializes the tensor arena and sets default values
ModelRunner::ModelRunner(size_t tensor_arena_size)
    : model(nullptr),
      interpreter(nullptr),
      input(nullptr),
      output(nullptr),
      kTensorArenaSize(tensor_arena_size),
      tensor_arena(nullptr) {
    // Allocate tensor arena
    tensor_arena = new uint8_t[kTensorArenaSize];
}

// Destructor: frees up any allocated memory
ModelRunner::~ModelRunner() {
    if (tensor_arena) {
        delete[] tensor_arena;
        tensor_arena = nullptr;
    }
}

// Initialize the model and interpreter
void ModelRunner::initModel() {
    ESP_LOGI(ModelRunner_TAG, "Initializing model...");

    // Load the model
    model = tflite::GetModel(g_model);
    if (model->version() != TFLITE_SCHEMA_VERSION) {
        ESP_LOGE(ModelRunner_TAG, "Model version mismatch!");
        return;
    }

    // Setup the operator resolver
    static tflite::MicroMutableOpResolver<5> resolver;
    resolver.AddFullyConnected();
    resolver.AddConv2D();
    resolver.AddSoftmax();
    resolver.AddTanh();
    resolver.AddMul();  // Example of more operations if needed

    // Initialize the interpreter
    static tflite::RecordingMicroInterpreter static_interpreter(model, resolver, tensor_arena, kTensorArenaSize);
    interpreter = &static_interpreter;

    // Allocate tensors
    if (interpreter->AllocateTensors() != kTfLiteOk) {
        ESP_LOGE(ModelRunner_TAG, "Failed to allocate tensors!");
        return;
    }

    // Set input and output tensors
    input = interpreter->input(0);
    output = interpreter->output(0);

    ESP_LOGI(ModelRunner_TAG, "Model initialized successfully!");
}

// Run inference with dynamically provided input data (simple input size check)
template <typename T>
bool ModelRunner::runInference(T* input_data) {
    // Calculate expected input size from model dimensions
    size_t expected_input_size = input->bytes / sizeof(T);

    // Check if the input size matches the model's expected size
    if (input_data == nullptr || expected_input_size != input->bytes / sizeof(T)) {
        ESP_LOGE(ModelRunner_TAG, "Input size mismatch or null input data");
        return false;
    }

    // Copy input data into the input tensor
    std::memcpy(input->data.raw, input_data, input->bytes);

    // Perform inference
    if (interpreter->Invoke() != kTfLiteOk) {
        ESP_LOGE(ModelRunner_TAG, "Failed to invoke inference!");
        return false;
    }

    return true;
}

// Function to log the output after inference
void ModelRunner::logOutput() {
    ESP_LOGI(ModelRunner_TAG, "Inference complete. Output:");
    for (int i = 0; i < output->dims->data[output->dims->size - 1]; i++) {
        ESP_LOGI(ModelRunner_TAG, "Output[%d]: %f", i, output->data.f[i]);
    }
}

// Explicit template instantiation to handle float input data
template bool ModelRunner::runInference<float>(float* input_data);
template bool ModelRunner::runInference<int>(int* input_data);

