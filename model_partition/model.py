import tensorflow as tf
from tensorflow.keras import layers, models

class Model:
    def __init__(self, tf_model):
        """
        Initialize the Model with a TensorFlow model.

        :param tf_model: A TensorFlow Keras model.
        """
        self.tf_model = tf_model
        self.layer_details = self.extract_layer_details()

    def extract_layer_details(self):
        """
        Extracts detailed information about each layer in the model.

        Returns:
            A list of dictionaries, each containing details for a layer.
        """
        layer_info = []
        for layer in self.tf_model.layers:
            flops, params = self.calculate_flops_and_params(layer)
            layer_info.append({
                'name': layer.name,
                'type': layer.__class__.__name__,
                'flops': flops,
                'params': params
            })
        return layer_info

    def calculate_flops_and_params(self, layer):
        """
        Calculate FLOPs and parameters for a given layer.

        :param layer: The Keras layer.
        Returns:
            Tuple (FLOPs, number of parameters)
        """
        # Calculate the number of parameters
        params = layer.count_params()

        # Estimate FLOPs (floating-point operations)
        if isinstance(layer, (layers.Conv2D, layers.Dense)):
            flops = params * 2  # Rough estimate for Conv2D/Dense layers
        else:
            flops = 0  # For simplicity, treat others as negligible

        return flops, params

    def get_layers(self):
        return self.layer_details

# Example of a simple CNN model
def create_simple_cnn():
    model = models.Sequential([
        layers.Input(shape=(32, 32, 3)),
        layers.Conv2D(16, kernel_size=(3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    return model

tf_model = create_simple_cnn()
model = Model(tf_model)
layer_details = model.get_layers()
print("Layer details:", layer_details)
