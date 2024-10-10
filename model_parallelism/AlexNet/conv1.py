import tensorflow as tf
import numpy as np

# Define the original Conv1 layer configuration for AlexNet with full input shape
class OriginalAlexNetConv1(tf.keras.Model):
    def __init__(self):
        super(OriginalAlexNetConv1, self).__init__()
        # Define Conv1 layer for the entire input shape (e.g., [227, 227, 3])
        self.conv1 = tf.keras.layers.Conv2D(
            filters=96,
            kernel_size=11,
            strides=4,
            activation='relu',
            input_shape=(227, 227, 3)
        )

    def call(self, inputs):
        return self.conv1(inputs)

# Load the full original Conv1 model
full_model = OriginalAlexNetConv1()

# Initialize the weights by passing a dummy input through the model
dummy_input = np.random.rand(1, 227, 227, 3).astype(np.float32)  # Shape [1, 227, 227, 3]
full_model(dummy_input)  # Run a forward pass to build the model and initialize the weights

# Extract weights and biases from the original Conv1 layer after initialization
conv1_weights, conv1_biases = full_model.conv1.get_weights()

# Print the original weights shape for reference
print(f"Original Conv1 Weights Shape: {conv1_weights.shape}")  # Should be (11, 11, 3, 96)
print(f"Original Conv1 Biases Shape: {conv1_biases.shape}")    # Should be (96,)

# Define the specific input row indices for each partition
partition_indices = [
    {"partition": 1, "start_row": 1, "end_row": 51},
    {"partition": 2, "start_row": 45, "end_row": 95},
    {"partition": 3, "start_row": 89, "end_row": 139},
    {"partition": 4, "start_row": 133, "end_row": 183},
    {"partition": 5, "start_row": 177, "end_row": 227}
]

# Create new models for each partition using the original weights
for partition_info in partition_indices:
    partition_id = partition_info["partition"]
    start_row = partition_info["start_row"]
    end_row = partition_info["end_row"]

    # Calculate the input height for each partition
    partition_height = end_row - start_row + 1
    print(f"Creating model for Partition {partition_id} with rows {start_row} to {end_row} (Height: {partition_height})")

    # Create a new partitioned Conv1 model using the specific height
    class PartitionedConv1(tf.keras.Model):
        def __init__(self):
            super(PartitionedConv1, self).__init__()
            self.conv1 = tf.keras.layers.Conv2D(
                filters=96,
                kernel_size=11,
                strides=4,
                activation='relu',
                input_shape=(partition_height, 227, 3)
            )

        def call(self, inputs):
            return self.conv1(inputs)

    # Create the new partitioned model
    partition_model = PartitionedConv1()

    # **Build the partitioned model by passing a dummy input through it**
    dummy_partition_input = np.random.rand(1, partition_height, 227, 3).astype(np.float32)
    partition_model(dummy_partition_input)  # Initialize the weights structure

    # Now set the weights using the original Conv1 weights and biases
    partition_model.conv1.set_weights([conv1_weights, conv1_biases])

    # Convert the partitioned model to TFLite format
    converter = tf.lite.TFLiteConverter.from_keras_model(partition_model)
    tflite_model = converter.convert()

    # Save the partitioned model as a .tflite file
    filename = f"alexnet_conv1_partition_{partition_id}.tflite"
    with open(filename, "wb") as f:
        f.write(tflite_model)
        print(f"Saved TFLite model for Partition {partition_id}: {filename}")

print("All partitioned models created successfully!")
