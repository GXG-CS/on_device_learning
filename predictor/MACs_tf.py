import tensorflow as tf
import numpy as np

def calculate_macs(model):
    macs = 0
    
    for layer in model.layers:
        if isinstance(layer, tf.keras.layers.Conv2D):
            output_shape = layer.output.shape[1:]  # Ignore batch size
            kernel_shape = layer.kernel.shape
            input_channels = kernel_shape[-2]
            output_channels = kernel_shape[-1]
            # Conv2D MACs calculation: Output height * Output width * Output channels * Kernel height * Kernel width * Input channels
            layer_macs = (output_shape[0] * output_shape[1] * output_channels *
                          kernel_shape[0] * kernel_shape[1] * input_channels)
            macs += layer_macs
            
        elif isinstance(layer, tf.keras.layers.DepthwiseConv2D):
            output_shape = layer.output.shape[1:]  # Ignore batch size
            kernel_shape = layer.depthwise_kernel.shape
            input_channels = output_shape[-1]
            # DepthwiseConv2D MACs calculation: Output height * Output width * Input channels * Kernel height * Kernel width
            layer_macs = (output_shape[0] * output_shape[1] * input_channels *
                          kernel_shape[0] * kernel_shape[1])
            macs += layer_macs
            
        elif isinstance(layer, tf.keras.layers.Dense):
            input_units = layer.input.shape[-1]
            output_units = layer.units
            # Dense MACs calculation: Input units * Output units
            layer_macs = (input_units * output_units)
            # Add the MACs for the biases (one addition per output unit)
            layer_macs += output_units
            macs += layer_macs

        elif isinstance(layer, tf.keras.layers.Add):
            # Add layers don't typically have MACs as they perform element-wise addition.
            output_shape = layer.output.shape[1:]  # Ignore batch size
            layer_macs = np.prod(output_shape)
            macs += layer_macs

    return macs

def load_model():
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=(32, 32, 3)),  # Example input shape for an image
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),  # 32 filters, 3x3 kernel
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),  # Max pooling
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),  # 64 filters, 3x3 kernel
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),  # Max pooling
        tf.keras.layers.Flatten(),  # Flatten before fully connected layers
        tf.keras.layers.Dense(128, activation='relu'),  # Dense layer with 128 units
        tf.keras.layers.Dense(10, activation='softmax')  # Output layer with 10 units
    ])
    
    return model


if __name__ == "__main__":
    model = load_model()
    model.summary()

    # Calculate MACs dynamically based on the model layers
    macs = calculate_macs(model)
    print(f"Total MACs in the model: {macs}")
