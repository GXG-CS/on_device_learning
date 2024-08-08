def bin_to_c_header(input_filename, output_filename, array_name):
    """
    Converts a binary file to a C header file.
    
    Args:
    input_filename (str): Path to the binary input file.
    output_filename (str): Path to the output C header file.
    array_name (str): Name of the array in the generated C header.
    """
    try:
        with open(input_filename, "rb") as binary_file:
            data = binary_file.read()
        with open(output_filename, "w") as header_file:
            header_file.write(f"unsigned char {array_name}[] = {{\n")
            byte_array = ["0x{:02x}".format(byte) for byte in data]
            line_length = 12
            for i in range(0, len(byte_array), line_length):
                line = ", ".join(byte_array[i:i+line_length]) + ","
                if i + line_length >= len(byte_array):
                    line = line[:-1]  # Remove the last comma on the last line
                header_file.write("    " + line + "\n")
            header_file.write("};\n")
        print("Header file created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    bin_to_c_header("mobilenetv2_segment.tflite", "model_data.h", "model_data")
