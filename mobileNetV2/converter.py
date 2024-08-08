import tensorflow as tf

# Ensure you have the latest version of TensorFlow
print("TensorFlow version:", tf.__version__)

# Load the MobileNetV2 model
model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')

# Extract the desired segment by specifying the output layer
# 'block_2_add' is the output after the second bottleneck block
output_layer = model.get_layer('block_2_add').output

# Create a new model with the specified input and output
segment_model = tf.keras.Model(inputs=model.input, outputs=output_layer)

# Convert the model segment to TensorFlow Lite format without optimizations
converter = tf.lite.TFLiteConverter.from_keras_model(segment_model)
tflite_model = converter.convert()

# Save the converted model to a TFLite file
with open('mobilenetv2_segment.tflite', 'wb') as f:
    f.write(tflite_model)

print("Model conversion successful, saved as 'mobilenetv2_segment.tflite'.")
