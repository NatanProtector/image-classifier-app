import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
import cv2
# Image matrix operations

def load_image_as_matrix(image_path):
    """
    Load an image from a file path and return it as a numpy matrix.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        numpy.ndarray: Image as a numpy matrix with shape (height, width, channels)
        
    Raises:
        FileNotFoundError: If the image file doesn't exist
        ValueError: If the file is not a valid image
    """
    # Check if file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    try:
        # Open image using PIL
        image = Image.open(image_path)
        
        # Convert to RGB if image is in RGBA mode (to ensure consistent format)
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        # Convert PIL image to numpy array
        image_matrix = np.array(image)
        
        return image_matrix
        
    except Exception as e:
        raise ValueError(f"Failed to load image from {image_path}: {str(e)}")


def resize_image_matrix(image_matrix, target_shape):
    """
    Resize image while preserving quality using better algorithms
    """
    # Convert back to PIL for better resizing
    image = Image.fromarray(image_matrix)
    
    # Use high-quality resampling
    resized_image = image.resize(target_shape[:2], Image.LANCZOS)
    
    # Convert back to numpy array
    resized_image = np.array(resized_image)
    
    # Ensure correct shape - convert grayscale to RGB
    if len(resized_image.shape) == 2:  # Grayscale (256, 256)
        # Convert to RGB by repeating the grayscale channel 3 times
        resized_image = np.stack([resized_image] * 3, axis=-1)
    elif resized_image.shape[2] == 4:  # RGBA (256, 256, 4)
        # Remove alpha channel to get RGB
        resized_image = resized_image[:, :, :3]

    return np.array(resized_image)

def rotate_image_matrix(image_matrix, angle):
    """
    Rotate an image matrix by a given angle.
    """
    image = Image.fromarray(image_matrix)
    rotated_image = image.rotate(angle)
    return np.array(rotated_image)

def display_image_matrix(image_matrix):
    """
    Display an image matrix.
    
    Args:
        image_matrix (numpy.ndarray): The image matrix to display
    """
    cv2.imshow("Image", image_matrix)
    cv2.waitKey(0)
    cv2.destroyAllWindows()