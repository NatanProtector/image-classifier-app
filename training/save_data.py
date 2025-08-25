import os
import numpy as np
from sklearn.utils import shuffle
from utils import load_image_as_matrix, display_image_matrix


# Saves the processed images to the data/processed folder in a numpy object

# Preprocessing
image_shape = (256, 256, 3)

def check_correct_shape(image_matrix, image_shape):
    if image_matrix.shape != image_shape:
        display_image_matrix(image_matrix)
        raise Exception("Image shape is not correct")
    
    
dog_images = []
dog_labels = []
cat_images = []
cat_labels = []
other_images = []
other_labels = []

# Cat data directory
cat_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "Cat")

# Dog data directory
dog_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "Dog")

# Other images directory
other_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "other")

num_other_images = len([f for f in os.listdir(cat_data_dir) if os.path.isfile(os.path.join(other_data_dir, f))])
num_cat_images = len([f for f in os.listdir(cat_data_dir) if os.path.isfile(os.path.join(cat_data_dir, f))])
num_dog_images = len([f for f in os.listdir(dog_data_dir) if os.path.isfile(os.path.join(dog_data_dir, f))])

# # Load cat images
# for image_path in os.listdir(cat_data_dir):
#     image_path = os.path.join(cat_data_dir, image_path)
#     image_matrix = load_image_as_matrix(image_path)

#     check_correct_shape(image_matrix, image_shape)
#     cat_images.append(image_matrix)
#     cat_labels.append([1, 0, 0])
    
# print(f"Loaded {num_cat_images} cat images")

# # Save cat images
# np.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "cat_images.npy"), cat_images)
    
# # Load dog images
# for image_path in os.listdir(dog_data_dir):
#     image_path = os.path.join(dog_data_dir, image_path)
#     image_matrix = load_image_as_matrix(image_path)
#     check_correct_shape(image_matrix, image_shape)
#     dog_images.append(image_matrix)
#     dog_labels.append([0, 1, 0])

# print(f"Loaded {num_dog_images} dog images")

# # Save dog images
# np.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "dog_images.npy"), dog_images)

# Load other images
for image_path in os.listdir(other_data_dir):
    image_matrix = load_image_as_matrix(os.path.join(other_data_dir, image_path))
    
    check_correct_shape(image_matrix, image_shape)
    
    other_images.append(image_matrix)
    other_labels.append([0, 0, 1])
    
print(f"Loaded {num_other_images} other images")

np.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "other_images.npy"), other_images)