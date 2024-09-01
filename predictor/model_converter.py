import tensorflow as tf

# Load a very simple pre-trained model (e.g., a single Dense layer)
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


def convert_to_tflite(model):
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    
    # Save the .tflite model
    with open('model.tflite', 'wb') as f:
        f.write(tflite_model)
    print("Model converted to .tflite and saved as simple_model.tflite")

if __name__ == "__main__":
    model = load_model()
    print(model.summary())
    convert_to_tflite(model)
