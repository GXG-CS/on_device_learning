import os
import json
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from multiprocessing import Pool, cpu_count

# Function to process a single image for parallel execution
def process_image(data):
    img_path, ground_truth_label, index = data

    # Preprocess the image
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # Run inference using VGG16
    model = VGG16(weights='imagenet')
    preds = model.predict(x)

    # Decode the top-5 predictions
    top5_preds = np.argsort(preds[0])[-5:][::-1]  # Get top-5 indices
    top1_pred = top5_preds[0]  # Top-1 prediction

    # Check Top-1 and Top-5 accuracy
    top1_correct = 1 if top1_pred == ground_truth_label else 0
    top5_correct = 1 if ground_truth_label in top5_preds else 0

    return top1_correct, top5_correct, img_path, top1_pred, ground_truth_label

if __name__ == "__main__":
    # Paths to your dataset and necessary files
    base_dir = "/Users/xiaoguang_guo@mines.edu/Documents/projects/datasets/imagenet-mini"
    val_dir = os.path.join(base_dir, "val")
    ground_truth_file = os.path.join(base_dir, "imagenet_mini_gt.txt")
    class_index_file = os.path.join(base_dir, "imagenet_class_index.json")

    # Load ImageNet class index to get the human-readable labels
    with open(class_index_file, 'r') as f:
        imagenet_class_index = json.load(f)
        index_to_label = {int(key): value[1] for key, value in imagenet_class_index.items()}

    # Load the new ground truth labels file for ImageNet Mini
    with open(ground_truth_file, 'r') as f:
        ground_truth_labels = f.readlines()
        ground_truth_labels = [int(label.strip()) for label in ground_truth_labels]

    # Prepare a list of all image paths in the val directory along with their indices
    image_paths = []
    total_labels = len(ground_truth_labels)
    image_index = 0

    for folder in sorted(os.listdir(val_dir)):
        folder_path = os.path.join(val_dir, folder)
        if os.path.isdir(folder_path):
            for img_name in sorted(os.listdir(folder_path)):
                img_path = os.path.join(folder_path, img_name)
                image_paths.append((img_path, ground_truth_labels[image_index], image_index))
                image_index += 1

    # Ensure the number of images matches the ground truth labels
    assert len(image_paths) == total_labels, f"Image paths ({len(image_paths)}) and ground truth labels ({total_labels}) mismatch."

    # Use multiprocessing to parallelize the evaluation across multiple CPU cores
    num_cores = cpu_count()
    print(f"Using {num_cores} cores for parallel processing.")

    with Pool(num_cores) as pool:
        results = pool.map(process_image, image_paths)

    # Calculate the overall Top-1 and Top-5 accuracy
    top1_correct = sum([result[0] for result in results])
    top5_correct = sum([result[1] for result in results])

    # Print debugging information for the first few images
    for res in results[:10]:
        img_path, top1_pred, ground_truth_label = res[2], res[3], res[4]
        print(f"Image: {img_path}, Top-1 Prediction: {top1_pred}, Ground Truth: {ground_truth_label}")

    # Calculate accuracy metrics
    top1_accuracy = top1_correct / total_labels
    top5_accuracy = top5_correct / total_labels

    # Print the evaluation results
    print(f"Total Images Evaluated: {total_labels}")
    print(f"Top-1 Accuracy: {top1_accuracy:.4f}")
    print(f"Top-5 Accuracy: {top5_accuracy:.4f}")