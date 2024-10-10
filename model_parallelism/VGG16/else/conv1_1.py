import tensorflow as tf
import numpy as np
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Input, Conv2D
from tensorflow.keras.models import Model

# Step 1: Load Pre-trained VGG16 Model and Extract Conv1_1 Layer
vgg16 = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
conv1_1_layer = vgg16.get_layer("block1_conv1")  # Get the Conv1_1 layer (first convolutional layer in VGG16)

# Get the weights and biases of the Conv1_1 layer
conv1_1_weights, conv1_1_biases = conv1_1_layer.get_weights()
print(f"Original Conv1_1 Weights Shape: {conv1_1_weights.shape}")
print(f"Original Conv1_1 Biases Shape: {conv1_1_biases.shape}")

# Step 2: Define Partition Parameters
partition_indices = [
    {"partition": 1, "start_row": 0, "end_row": 46, "output_rows": 45},
    {"partition": 2, "start_row": 45, "end_row": 91, "output_rows": 45},
    {"partition": 3, "start_row": 90, "end_row": 136, "output_rows": 45},
    {"partition": 4, "start_row": 135, "end_row": 181, "output_rows": 45},
    {"partition": 5, "start_row": 180, "end_row": 225, "output_rows": 44}
]

# Step 3: Partition Conv1_1 Weights and Create Models for Each Partition
filter_height, filter_width, in_channels, out_channels = conv1_1_weights.shape

# Loop through each partition, partition the weights, and create new models
for partition in partition_indices:
    partition_id = partition['partition']
    start_row = partition['start_row']
    end_row = partition['end_row']
    
    # Calculate the number of input rows for this partition
    input_height = end_row - start_row + 1
    partition_input_shape = (input_height, 224, 3)  # Input shape for the partition
    
    # Create partitioned weights for this section
    partitioned_weights = conv1_1_weights[:, :, :, :]  # All the filters are used for each partition
    
    # Create a new model for this partition with appropriate input shape
    input_layer = Input(shape=partition_input_shape)
    
    # Add a Conv2D layer with the same parameters as the original Conv1_1
    conv_layer = Conv2D(filters=64, kernel_size=(3, 3), strides=(1, 1), padding='same', name=f'Conv1_1_Partition_{partition_id}')(input_layer)
    
    # Create the model for this partition
    partition_model = Model(inputs=input_layer, outputs=conv_layer)
    
    # Set the weights and biases for the new model's convolution layer
    partition_model.get_layer(f'Conv1_1_Partition_{partition_id}').set_weights([partitioned_weights, conv1_1_biases])
    
    # Print the input and output shape for confirmation
    print(f"Partition {partition_id} - Input Shape: {partition_input_shape}, Output Shape: {partition_model.output_shape}")
    
    # Step 4: Convert the Partitioned Model to TFLite
    converter = tf.lite.TFLiteConverter.from_keras_model(partition_model)
    tflite_model = converter.convert()
    
    # Save the TFLite model for this partition
    tflite_filename = f"vgg16_conv1_partition_{partition_id}.tflite"
    with open(tflite_filename, "wb") as f:
        f.write(tflite_model)
        print(f"Saved TFLite model for Partition {partition_id} as {tflite_filename}")
