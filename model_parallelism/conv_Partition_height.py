def partition_conv_layer_by_output(input_height, filter_size, stride, padding, num_partitions):
    """
    Partition a convolutional layer by height into `num_partitions` segments, ensuring each partition produces 
    non-overlapping output rows and includes the necessary padding rows.

    Args:
    - input_height (int): Height of the input tensor (e.g., 224).
    - filter_size (int): Size of the convolutional filter (e.g., 3 for [3, 3]).
    - stride (int): Stride size for the convolution operation (e.g., 1).
    - padding (int): Padding added to the input tensor (e.g., 1).
    - num_partitions (int): Number of vertical partitions to create.

    Returns:
    - List of dictionaries, where each dictionary represents a partition with:
      {'partition_id': id, 'start_row': start, 'end_row': end, 'input_rows': ..., 'output_rows': ...}.
    """
    # Calculate effective input height including padding
    effective_input_height = input_height + 2 * padding

    # Calculate total output height after the convolution operation
    output_height = (effective_input_height - filter_size) // stride + 1

    # Calculate the output rows each partition should handle
    partition_output_height = output_height // num_partitions  # Base height for each partition's output rows
    remainder = output_height % num_partitions  # Extra rows to distribute

    # List to store partition details
    partitions = []
    current_output_start = 1

    for i in range(num_partitions):
        # Calculate how many output rows this partition should produce
        current_output_end = current_output_start + partition_output_height - 1

        # Distribute remainder output rows evenly among the first few partitions
        if i < remainder:
            current_output_end += 1

        # Calculate the corresponding input rows required to produce these output rows
        required_input_start = (current_output_start - 1) * stride - padding + 1
        required_input_end = (current_output_end - 1) * stride + filter_size - padding

        # Handle input row bounds and padding inclusion
        if required_input_start < 1:
            required_input_start = 0  # Include the top padding row
        if required_input_end > input_height:
            required_input_end = input_height + padding  # Include the bottom padding row

        # Store partition details
        partitions.append({
            'partition_id': i + 1,
            'start_row': required_input_start,
            'end_row': required_input_end,
            'input_rows': f"{required_input_start} - {required_input_end}",
            'output_rows': f"{current_output_start} - {current_output_end}"
        })

        # Update start index for the next partition
        current_output_start = current_output_end + 1

    return partitions

# Example Usage
conv_params = {
    'input_height': 224,  # Input height for the layer
    'filter_size': 3,     # Filter size for Conv1_1
    'stride': 1,          # Stride for Conv1_1
    'padding': 1,         # Padding for Conv1_1
    'num_partitions': 5   # Number of partitions
}

# conv_params = {
#     'input_height': 227,  # Input height for the layer
#     'filter_size': 11,     # Filter size for Conv1_1
#     'stride': 4,          # Stride for Conv1_1
#     'padding': 0,         # Padding for Conv1_1
#     'num_partitions': 5   # Number of partitions
# }

# Get partitions for the given convolution layer parameters
partitions = partition_conv_layer_by_output(**conv_params)

# Print the partition results
print("Model Parallelism Partitioning for Conv Layer (Conv1_1 Example):")
for part in partitions:
    print(f"Partition {part['partition_id']}: Input Rows = {part['input_rows']}, Output Rows = {part['output_rows']}")
