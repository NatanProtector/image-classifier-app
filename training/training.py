import os
from model_utils import CreateBinaryModel
import numpy as np

image_shape = (256, 256, 3)

print("Loading data for binary classification models...")

# Load all image data
cat_images = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "cat_images.npy"))
dog_images = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "dog_images.npy"))
not_cats_images = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "not_cats_images.npy"))
not_dogs_images = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "not_dogs_images.npy"))

print(f"Loaded {len(cat_images)} cat images, shape: {cat_images.shape}")
print(f"Loaded {len(dog_images)} dog images, shape: {dog_images.shape}")
print(f"Loaded {len(not_cats_images)} not-cat images, shape: {not_cats_images.shape}")
print(f"Loaded {len(not_dogs_images)} not-dog images, shape: {not_dogs_images.shape}")

# Prepare data for IsDog model (dog vs not-dog)
print("\nPreparing data for IsDog model...")
is_dog_images = np.concatenate((dog_images, not_dogs_images))
is_dog_labels = np.concatenate((np.ones(len(dog_images)), np.zeros(len(not_dogs_images))))

# Prepare data for IsCat model (cat vs not-cat)
print("Preparing data for IsCat model...")
is_cat_images = np.concatenate((cat_images, not_cats_images))
is_cat_labels = np.concatenate((np.ones(len(cat_images)), np.zeros(len(not_cats_images))))

print(f"IsDog dataset: {len(is_dog_images)} images, {np.sum(is_dog_labels)} dogs, {len(is_dog_labels) - np.sum(is_dog_labels)} not-dogs")
print(f"IsCat dataset: {len(is_cat_images)} images, {np.sum(is_cat_labels)} cats, {len(is_cat_labels) - np.sum(is_cat_labels)} not-cats")

# Shuffle data
np.random.seed(42)  # For reproducibility
np.random.shuffle(is_dog_images)
np.random.shuffle(is_dog_labels)
np.random.shuffle(is_cat_images)
np.random.shuffle(is_cat_labels)

split_ratio = 0.15

epochs = 1

# Train-test split for IsDog model
dog_test_size = int(len(is_dog_images) * split_ratio)
is_dog_test_images = is_dog_images[:dog_test_size]
is_dog_test_labels = is_dog_labels[:dog_test_size]
is_dog_train_images = is_dog_images[dog_test_size:]
is_dog_train_labels = is_dog_labels[dog_test_size:]

# Train-test split for IsCat model
cat_test_size = int(len(is_cat_images) * split_ratio)
is_cat_test_images = is_cat_images[:cat_test_size]
is_cat_test_labels = is_cat_labels[:cat_test_size]
is_cat_train_images = is_cat_images[cat_test_size:]
is_cat_train_labels = is_cat_labels[cat_test_size:]

print(f"\nIsDog train/test split: {len(is_dog_train_images)}/{len(is_dog_test_images)}")
print(f"IsCat train/test split: {len(is_cat_train_images)}/{len(is_cat_test_images)}")

# Create and train IsDog model
print("\n=== Training IsDog Model ===")
is_dog_model = CreateBinaryModel(image_shape)
is_dog_model.fit(is_dog_train_images, is_dog_train_labels, epochs=epochs, validation_split=0.2)

# Create and train IsCat model
print("\n=== Training IsCat Model ===")
is_cat_model = CreateBinaryModel(image_shape)
is_cat_model.fit(is_cat_train_images, is_cat_train_labels, epochs=epochs, validation_split=0.2)

# Evaluate IsDog model
print("\n=== Evaluating IsDog Model ===")
dog_loss, dog_accuracy = is_dog_model.evaluate(is_dog_test_images, is_dog_test_labels)
print(f"IsDog model - Test Loss: {dog_loss:.4f}, Test Accuracy: {dog_accuracy:.4f}")

# Evaluate IsCat model
print("\n=== Evaluating IsCat Model ===")
cat_loss, cat_accuracy = is_cat_model.evaluate(is_cat_test_images, is_cat_test_labels)
print(f"IsCat model - Test Loss: {cat_loss:.4f}, Test Accuracy: {cat_accuracy:.4f}")

# Save results
results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

# Create directories if they don't exist
os.makedirs(results_dir, exist_ok=True)
os.makedirs(models_dir, exist_ok=True)

# Save results
with open(os.path.join(results_dir, "results_binary_models.txt"), "w") as f:
    f.write("Binary Classification Models Results\n")
    f.write("=" * 40 + "\n\n")
    f.write(f"IsDog Model:\n")
    f.write(f"  Test Loss: {dog_loss:.4f}\n")
    f.write(f"  Test Accuracy: {dog_accuracy:.4f}\n\n")
    f.write(f"IsCat Model:\n")
    f.write(f"  Test Loss: {cat_loss:.4f}\n")
    f.write(f"  Test Accuracy: {cat_accuracy:.4f}\n")

# Save models
is_dog_model.save(os.path.join(models_dir, "IsDog_model.keras"))
is_cat_model.save(os.path.join(models_dir, "IsCat_model.keras"))

print(f"\nModels saved to {models_dir}/")
print(f"Results saved to {results_dir}/results_binary_models.txt")
print("\nTraining completed successfully!")