import os
from model_utils import CreateCNNModel
import numpy as np

image_shape = (256, 256, 3)

print("Loading data")

cat_images = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "cat_images.npy"))
dog_images = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "dog_images.npy"))
other_images = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "other_images.npy"))

print(f"Loaded {len(cat_images)} cat images, shape: {cat_images.shape}")
print(f"Loaded {len(dog_images)} dog images, shape: {dog_images.shape}")
print(f"Loaded {len(other_images)} other images, shape: {other_images.shape}")

cat_labels = np.array([[1, 0, 0] for _ in range(len(cat_images))])
dog_labels = np.array([[0, 1, 0] for _ in range(len(dog_images))])
other_labels = np.array([[0, 0, 1] for _ in range(len(other_images))])

print(f"Cat labels: {cat_labels}, shape: {cat_labels.shape}")
print(f"Dog labels: {dog_labels}, shape: {dog_labels.shape}")
print(f"Other labels: {other_labels}, shape: {other_labels.shape}")

# Shuffle data
np.random.shuffle(cat_images)
np.random.shuffle(dog_images)
np.random.shuffle(other_images)

split_ratio = 0.15
    
# train test split
cat_test_images = cat_images[:int(cat_images.shape[0] * split_ratio)]
cat_test_labels = cat_labels[:int(cat_labels.shape[0] * split_ratio)]
cat_train_images = cat_images[int(cat_images.shape[0] * split_ratio):]
cat_train_labels = cat_labels[int(cat_labels.shape[0] * split_ratio):]
dog_test_images = dog_images[:int(dog_images.shape[0] * split_ratio)]
dog_test_labels = dog_labels[:int(dog_labels.shape[0] * split_ratio)]
dog_train_images = dog_images[int(dog_images.shape[0] * split_ratio):]
dog_train_labels = dog_labels[int(dog_labels.shape[0] * split_ratio):]
other_test_images = other_images[:int(other_images.shape[0] * split_ratio)]
other_test_labels = other_labels[:int(other_labels.shape[0] * split_ratio)]
other_train_images = other_images[int(other_images.shape[0] * split_ratio):]
other_train_labels = other_labels[int(other_labels.shape[0] * split_ratio):]

# Split data into training and testing sets
train_images = np.concatenate((cat_train_images, dog_train_images, other_train_images))
train_labels = np.concatenate((cat_train_labels, dog_train_labels, other_train_labels))
    
# Create model
model = CreateCNNModel(image_shape)

# Train model
model.fit(train_images, train_labels, epochs=10)

# evaluate
result_cat = model.evaluate(np.array(cat_test_images), np.array(cat_test_labels))
print(f"Cat accuracy: {result_cat[1]}")
result_dog = model.evaluate(np.array(dog_test_images), np.array(dog_test_labels))
print(f"Dog accuracy: {result_dog[1]}")
result_other = model.evaluate(np.array(other_test_images), np.array(other_test_labels))
print(f"Other accuracy: {result_other[1]}")

model_name = "model_CNN_1epoch"

# save results
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", f"results_{model_name}.txt"), "w") as f:
    f.write(f"Cat accuracy: {result_cat[1]}\n")
    f.write(f"Dog accuracy: {result_dog[1]}\n")
    f.write(f"Other accuracy: {result_other[1]}\n")

# save
model.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", f"{model_name}.keras"))