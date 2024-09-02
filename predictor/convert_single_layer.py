import tensorflow as tf
from tensorflow.keras.models import Model

# Load the pre-trained MobileNetV2 model
base_model = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=False, input_shape=(32, 32, 3))

# Choose a single layer to extract, for example, the first convolutional layer
single_layer_model = Model(inputs=base_model.input, outputs=base_model.get_layer('block_1_expand').output)

# Convert the single layer model to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(single_layer_model)
tflite_single_layer_model = converter.convert()

# Save the single layer model as a .tflite file
with open('mobilenetv2_single_layer.tflite', 'wb') as f:
    f.write(tflite_single_layer_model)

print("Conversion to TensorFlow Lite format completed and saved as 'mobilenetv2_single_layer.tflite'.")
