import sys
from io import BytesIO
import numpy as np
import cv2
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image

# Only import tf when running the server or tests, otherwise
# we'd have to wait for the model to load when running 
# every other command, for example migrations. 
if 'runserver' or 'test' in sys.argv:
    import tensorflow as tf
    MODEL = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=False, pooling='avg')


# Preprocess function for images
def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Preprocesses an image for model input.
    Args:
        image_bytes (bytes): The image in bytes format.
    Returns:
        np.ndarray: The preprocessed image ready for model input.
    Steps:
        1. Opens the image from bytes.
        2. Converts the image to a numpy array.
        3. Resizes the image to 224x224 pixels to fit the model.
        4. Adds batch dimensions so the image can be processed in batches.
        5. Normalizes the image using MobileNetV2 preprocessing.
    """
    image = Image.open(BytesIO(image_bytes))
    img = np.array(image)

    # Ensure the image has 3 channels (RGB)
    if img.shape[-1] == 4: 
        # Convert RGBA to RGB
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    elif len(img.shape) == 2: 
        # Conert GRAYSCALE to RGB
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    # Resize to fit the model
    img = cv2.resize(img, (224, 224)) 
    # Add batch dimensions so 
    img = np.expand_dims(img, axis=0)  
    # Normalize image
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)  
    return img


def extract_features(img) -> np.ndarray:
    """
    Extracts features from the preprocessed image using the set model.
    Args:
        img (np.ndarray): The preprocessed image.
    Returns:
        np.ndarray: The extracted features from the image.
    """
    return MODEL.predict(img)


def compare_features(features1: np.ndarray, features2: np.ndarray) -> float:
    """
        Compares the features of two images using cosine similarity.
        Args:
            img1 (np.ndarray): The features of the first image.
            img2 (np.ndarray): The features of the second image.
        Returns:
            float: The cosine similarity between the two images.
    """
    return cosine_similarity(features1, features2)
