import tensorflow as tf

def calculate_macs_tflite(interpreter):
    macs = 0

    # Get details of the operations in the model
    for op_index in range(len(interpreter._get_ops_details())):
        op = interpreter._get_ops_details()[op_index]
        op_type = op['op_name']

        # Handle Conv2D operations
        if op_type == 'CONV_2D':
            output_details = interpreter.get_tensor_details()[op['outputs'][0]]
            output_shape = output_details['shape']
            kernel_shape = interpreter.get_tensor_details()[op['inputs'][1]]['shape']

            # Calculate MACs for Conv2D
            input_channels = kernel_shape[-2]
            output_channels = kernel_shape[-1]
            kernel_height = kernel_shape[0]
            kernel_width = kernel_shape[1]
            output_height, output_width = output_shape[1], output_shape[2]

            layer_macs = (output_height * output_width * output_channels *
                          kernel_height * kernel_width * input_channels)
            macs += layer_macs

        # Handle DepthwiseConv2D operations
        elif op_type == 'DEPTHWISE_CONV_2D':
            output_details = interpreter.get_tensor_details()[op['outputs'][0]]
            output_shape = output_details['shape']
            kernel_shape = interpreter.get_tensor_details()[op['inputs'][1]]['shape']

            # Calculate MACs for DepthwiseConv2D
            input_channels = kernel_shape[-2]
            kernel_height = kernel_shape[0]
            kernel_width = kernel_shape[1]
            output_height, output_width = output_shape[1], output_shape[2]

            layer_macs = (output_height * output_width * input_channels *
                          kernel_height * kernel_width)
            macs += layer_macs

        # Handle FullyConnected (Dense) operations
        elif op_type == 'FULLY_CONNECTED':
            output_details = interpreter.get_tensor_details()[op['outputs'][0]]
            output_shape = output_details['shape']
            input_details = interpreter.get_tensor_details()[op['inputs'][0]]
            input_shape = input_details['shape']

            # Calculate MACs for FullyConnected
            input_units = input_shape[-1]
            output_units = output_shape[-1]
            layer_macs = input_units * output_units
            macs += layer_macs

        # Handle Add operations (element-wise addition)
        elif op_type == 'ADD':
            output_details = interpreter.get_tensor_details()[op['outputs'][0]]
            output_shape = output_details['shape']

            # Calculate MACs for Add (element-wise addition)
            layer_macs = tf.reduce_prod(output_shape).numpy()  # Number of elements in the output
            macs += layer_macs

        # Handle GlobalAveragePooling2D operations
        elif op_type == 'MEAN':
            output_details = interpreter.get_tensor_details()[op['outputs'][0]]
            output_shape = output_details['shape']
            input_details = interpreter.get_tensor_details()[op['inputs'][0]]
            input_shape = input_details['shape']

            # Calculate MACs for GlobalAveragePooling2D
            input_height = input_shape[1]
            input_width = input_shape[2]
            input_channels = input_shape[3]
            layer_macs = input_height * input_width * input_channels
            macs += layer_macs

    return macs

def load_tflite_model(model_path):
    # Load the TFLite model and allocate tensors
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

if __name__ == "__main__":
    model_path = 'model.tflite'  # Replace with your .tflite model path
    interpreter = load_tflite_model(model_path)

    # Calculate MACs for the .tflite model
    macs = calculate_macs_tflite(interpreter)
    print(f"Total MACs in the .tflite model: {macs}")
