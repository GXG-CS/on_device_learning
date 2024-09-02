import re
import matplotlib.pyplot as plt

def parse_map_file(map_file_path):
    persistent_buffers_size = 0
    total_memory_used = 0

    # Define patterns to look for in the map file
    persistent_buffer_patterns = [
        re.compile(r'persistent_buffer'),
        re.compile(r'PersistentBuffer'),
    ]

    # Open and read the map file
    with open(map_file_path, 'r') as file:
        for line in file:
            # Extract the size from the line
            match = re.search(r'0x([0-9a-fA-F]+)\s+(\S+)', line)
            if match:
                size = int(match.group(1), 16)
                total_memory_used += size
                
                # Check if this line is part of the persistent buffers
                for pattern in persistent_buffer_patterns:
                    if pattern.search(line):
                        persistent_buffers_size += size

    return persistent_buffers_size, total_memory_used

def visualize_memory_usage(persistent_buffers_size, total_memory_used):
    # Calculate the rest of the memory usage
    other_memory_size = total_memory_used - persistent_buffers_size

    # Data for plotting
    labels = 'Persistent Buffers', 'Other Memory'
    sizes = [persistent_buffers_size, other_memory_size]
    colors = ['#ff9999','#66b3ff']
    
    # Plotting the pie chart
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Memory Usage Breakdown")
    plt.show()

# Usage example
if __name__ == "__main__":
    map_file_path = "person_detection.map"  # Replace with the path to your .map file
    persistent_buffers_size, total_memory_used = parse_map_file(map_file_path)
    
    print(f"Persistent Buffers Size: {persistent_buffers_size} bytes")
    print(f"Total Memory Used: {total_memory_used} bytes")
    
    visualize_memory_usage(persistent_buffers_size, total_memory_used)

