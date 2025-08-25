from utils import load_image_as_matrix, resize_image_matrix, display_image_matrix, rotate_image_matrix
import os
from model_utils import CreateCNNModel
import numpy as np
from sklearn.utils import shuffle

# Preprocessing
image_shape = (256, 256, 3)

def check_correct_shape(image_matrix, image_shape):
    if image_matrix.shape != image_shape:
        display_image_matrix(image_matrix)
        raise Exception("Image shape is not correct")

all_images = []
all_labels = []

# Cat data directory
cat_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "Cat")

# Dog data directory
dog_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "Dog")

# Other images directory
other_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "other")

num_other_images = len([f for f in os.listdir(cat_data_dir) if os.path.isfile(os.path.join(other_data_dir, f))])
num_cat_images = len([f for f in os.listdir(cat_data_dir) if os.path.isfile(os.path.join(cat_data_dir, f))])
num_dog_images = len([f for f in os.listdir(dog_data_dir) if os.path.isfile(os.path.join(dog_data_dir, f))])

# Load cat images
for image_path in os.listdir(cat_data_dir):
    image_path = os.path.join(cat_data_dir, image_path)
    image_matrix = load_image_as_matrix(image_path)
    image_matrix = resize_image_matrix(image_matrix, image_shape)
    check_correct_shape(image_matrix, image_shape)
    all_images.append(image_matrix)
    all_labels.append([1, 0, 0])
        
print(f"Loaded {num_cat_images} cat images")
    
# Load dog images
for image_path in os.listdir(dog_data_dir):
    image_path = os.path.join(dog_data_dir, image_path)
    image_matrix = load_image_as_matrix(image_path)
    image_matrix = resize_image_matrix(image_matrix, image_shape)
    check_correct_shape(image_matrix, image_shape)
    all_images.append(image_matrix)
    all_labels.append([0, 1, 0])

print(f"Loaded {num_dog_images} dog images")

# Load other images
for image_path in os.listdir(other_data_dir):
    image_matrix = load_image_as_matrix(os.path.join(other_data_dir, image_path))
    image_matrix = resize_image_matrix(image_matrix, image_shape)
    
    check_correct_shape(image_matrix, image_shape)
    
    image_matrix = rotate_image_matrix(image_matrix, 90)
    all_images.append(image_matrix)
    all_labels.append([0, 0, 1])
    
    image_matrix = rotate_image_matrix(image_matrix, 90)
    all_images.append(image_matrix)
    all_labels.append([0, 0, 1])
    
    image_matrix = rotate_image_matrix(image_matrix, 90)
    all_images.append(image_matrix)
    all_labels.append([0, 0, 1])
    
    image_matrix = rotate_image_matrix(image_matrix, 90)
    all_images.append(image_matrix)        
    all_labels.append([0, 0, 1])

print(f"Loaded {4*len(os.listdir(other_data_dir))} other images")
    
all_images = np.array(all_images)
all_labels = np.array(all_labels)
    
# Shuffle data
all_images, all_labels = shuffle(all_images, all_labels)
    
# Split data into training and testing sets
train_images = all_images[:int(len(all_images) * 0.8)]
train_labels = all_labels[:int(len(all_labels) * 0.8)]
test_images = all_images[int(len(all_images) * 0.8):]
test_labels = all_labels[int(len(all_labels) * 0.8):]
    
# Create model
model = CreateCNNModel(image_shape)

# Train model
model.fit(train_images, train_labels, epochs=1)

# evaluate
result = model.evaluate(test_images, test_labels)

print(result)

# save
model.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "model.keras"))