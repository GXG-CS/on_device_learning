import argparse

# Function to convert the tflite model to C array
def convert_to_cc(input_file, output_file, array_name):
    # Read the binary content of the .tflite model
    with open(input_file, 'rb') as f:
        model_content = f.read()

    # Start writing the C array with proper alignment and model length declaration
    c_array = f'#include "model_data.h"\n\n'
    c_array += f'alignas(8) const unsigned char {array_name}[] = {{\n'

    # Format the binary content as hex values, 12 bytes per line
    c_array += ',\n'.join('  ' + ', '.join(f'0x{b:02x}' for b in model_content[i:i+12]) for i in range(0, len(model_content), 12))

    # End the array and declare the model length
    c_array += f'\n}};\nconst int {array_name}_len = {len(model_content)};\n'

    # Write the C array to the output .cc file
    with open(output_file, 'w') as f:
        f.write(c_array)

    print(f"Model converted to C array and saved as {output_file}.")

# Set up argument parsing
def main():
    parser = argparse.ArgumentParser(description="Convert a .tflite model to a C array")
    parser.add_argument("input_file", help="Path to the input .tflite model file")
    parser.add_argument("output_file", help="Path to the output .cc file")
    parser.add_argument("array_name", help="Name of the C array")

    args = parser.parse_args()

    # Call the conversion function
    convert_to_cc(args.input_file, args.output_file, args.array_name)

if __name__ == "__main__":
    main()

# Convert layer_1.tflite to C array
# python tflite2cc.py layer_1.tflite layer_1.cc g_model

# Convert layer_2.tflite to C array
# python tflite2cc.py layer_2.tflite layer_2.cc g_model

