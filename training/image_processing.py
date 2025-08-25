from utils import load_image_as_matrix, resize_image_matrix, display_image_matrix, rotate_image_matrix
import os
import numpy as np
import cv2

# Preprocessing
image_shape = (256, 256, 3)

def check_correct_shape(image_matrix, image_shape):
    if image_matrix.shape != image_shape:
        display_image_matrix(image_matrix)
        raise Exception("Image shape is not correct")

all_images = []
all_labels = []

# Cat data directory
cat_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "cat")

# Dog data directory
dog_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "dog")

# Other images directory
other_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "other")

num_other_images = len([f for f in os.listdir(cat_data_dir) if os.path.isfile(os.path.join(other_data_dir, f))])
num_cat_images = len([f for f in os.listdir(cat_data_dir) if os.path.isfile(os.path.join(cat_data_dir, f))])
num_dog_images = len([f for f in os.listdir(dog_data_dir) if os.path.isfile(os.path.join(dog_data_dir, f))])

# # Load cat images
# for image_path in os.listdir(cat_data_dir):
#     image_path = os.path.join(cat_data_dir, image_path)
#     file_name = image_path.split("\\")[-1]
#     image_matrix = load_image_as_matrix(image_path)
#     image_matrix = resize_image_matrix(image_matrix, image_shape)
#     check_correct_shape(image_matrix, image_shape)
#     all_images.append(image_matrix)
#     all_labels.append([1, 0, 0])
    
#     # save image in data/processed/cat/
#     cv2.imwrite(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "Cat", file_name), image_matrix)
        
print(f"Proccessed {num_cat_images} cat images")
    
# # Load dog images
# for image_path in os.listdir(dog_data_dir):
#     image_path = os.path.join(dog_data_dir, image_path)
#     file_name = image_path.split("\\")[-1]
#     image_matrix = load_image_as_matrix(image_path)
#     image_matrix = resize_image_matrix(image_matrix, image_shape)
#     check_correct_shape(image_matrix, image_shape)
#     all_images.append(image_matrix)
#     all_labels.append([0, 1, 0])

#     # save image in data/processed/dog/
#     cv2.imwrite(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "Dog", file_name), image_matrix)

print(f"Proccessed {num_dog_images} dog images")

# Load other images
for image_path in os.listdir(other_data_dir):
    image_matrix = load_image_as_matrix(os.path.join(other_data_dir, image_path))
    image_matrix = resize_image_matrix(image_matrix, image_shape)
    
    image_name = image_path.split("\\")[-1]    
    
    image_name = image_name.split(".")[0]
    
    check_correct_shape(image_matrix, image_shape)
    
    # image_matrix = rotate_image_matrix(image_matrix, 90)
    all_images.append(image_matrix)
    all_labels.append([0, 0, 1])
    # save image in data/processed/other/
    cv2.imwrite(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "Other", f"{image_name}.jpg"), image_matrix)

print(f"proccessed {len(os.listdir(other_data_dir))} other images")

print("All images saved")