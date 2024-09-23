import tensorflow as tf

def estimate_memory_usage(interpreter, total_sram=320 * 1024, total_eflash=1 * 1024 * 1024):
    # Ensure tensors are allocated
    interpreter.allocate_tensors()

    # Initialize memory usage values
    sram_usage = {
        "Persistent Buffers": 0,
        "Intermediate Tensors": 0,
        "Runtime Memory": 0,  # Placeholder for runtime memory usage
    }
    eflash_usage = {
        "Quantization Params and Graph": 0,
        "Weights + Biases": 0,
    }

    # Analyze the tensors to estimate memory usage
    tensor_details = interpreter.get_tensor_details()

    for tensor in tensor_details:
        tensor_shape = tensor['shape']
        tensor_dtype_size = tf.dtypes.as_dtype(tensor['dtype']).size
        tensor_size = tf.reduce_prod(tensor_shape) * tensor_dtype_size

        # Assuming weights and biases are constant tensors (this is typical)
        if tensor['name'].lower().endswith(('weight', 'bias')):
            eflash_usage["Weights + Biases"] += tensor_size.numpy()  # Add to eFlash usage
        else:
            sram_usage["Intermediate Tensors"] += tensor_size.numpy()  # Add to SRAM usage

    # Estimate runtime memory based on typical overhead or documentation (e.g., 4KB)
    sram_usage["Runtime Memory"] = 4 * 1024  # Example: 4KB overhead for TFLM runtime

    # Calculate Persistent Buffers as the remaining SRAM after Intermediate Tensors and Runtime Memory
    sram_usage["Persistent Buffers"] = total_sram - (sram_usage["Intermediate Tensors"] + sram_usage["Runtime Memory"])

    # Calculate Free Memory
    sram_usage["Free"] = max(0, total_sram - (sram_usage["Persistent Buffers"] + sram_usage["Intermediate Tensors"] + sram_usage["Runtime Memory"]))
    eflash_usage["Free"] = max(0, total_eflash - sum(eflash_usage.values()))

    return sram_usage, eflash_usage, total_sram, total_eflash

def main():
    model_path = 'model.tflite'  # Replace with your .tflite model path
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    sram_usage, eflash_usage, total_sram, total_eflash = estimate_memory_usage(interpreter)

    # Output the estimated memory usage values
    print("Estimated Memory Usage:")
    print(f"SRAM Usage:")
    print(f"  - Runtime Memory: {sram_usage['Runtime Memory'] / 1024:.2f} KB")
    print(f"  - Persistent Buffers: {sram_usage['Persistent Buffers'] / 1024:.2f} KB")
    print(f"  - Intermediate Tensors: {sram_usage['Intermediate Tensors'] / 1024:.2f} KB")
    print(f"  - Free: {sram_usage['Free'] / 1024:.2f} KB")
    print(f"Total SRAM: {total_sram / 1024:.2f} KB")

    print(f"eFlash Usage:")
    print(f"  - Quantization Params and Graph: {eflash_usage['Quantization Params and Graph'] / 1024:.2f} KB")
    print(f"  - Weights + Biases: {eflash_usage['Weights + Biases'] / 1024:.2f} KB")
    print(f"  - Free: {eflash_usage['Free'] / 1024:.2f} KB")
    print(f"Total eFlash: {total_eflash / 1024:.2f} KB")

if __name__ == "__main__":
    main()
