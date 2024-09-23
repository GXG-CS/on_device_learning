import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, Input

# Define a simple and small base model
input_layer = Input(shape=(32, 32, 3))
x = Conv2D(8, (3, 3), activation='relu', padding='same')(input_layer)  # 8 filters
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)  # Another simple layer
base_model = Model(inputs=input_layer, outputs=x)

# Extract a single layer from the simple model
single_layer_model = Model(inputs=base_model.input, outputs=base_model.get_layer(index=1).output)

# Convert the single layer model to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(single_layer_model)
tflite_single_layer_model = converter.convert()

# Save the single layer model as a .tflite file
with open('simple_single_layer_model.tflite', 'wb') as f:
    f.write(tflite_single_layer_model)

print("Conversion to TensorFlow Lite format completed and saved as 'simple_single_layer_model.tflite'.")
