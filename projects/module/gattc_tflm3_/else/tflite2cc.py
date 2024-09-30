# Define the input and output file names
input_file = 'mobilenetv2_single_layer.tflite'
output_file = 'model_data.cc'
array_name = 'mobilenetv2_single_layer_model'

# Read the binary content of the .tflite model
with open(input_file, 'rb') as f:
    model_content = f.read()

# Create the C array string
c_array = f"unsigned char {array_name}[] = {{\n"
c_array += ',\n'.join('  ' + ', '.join(f'0x{b:02x}' for b in model_content[i:i+12]) for i in range(0, len(model_content), 12))
c_array += f"\n}};\nunsigned int {array_name}_len = {len(model_content)};\n"

# Write the C array to the output .cc file
with open(output_file, 'w') as f:
    f.write(c_array)

print(f"Model converted to C array and saved as {output_file}.")
