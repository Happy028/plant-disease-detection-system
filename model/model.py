import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "plant_disease_model.h5")

# -----------------------------
# Class Names
# IMPORTANT:
# Ye class names tumhare training dataset folders ke order ke according hone chahiye.
# Agar tumhare paas 38 classes hain, yaha 38 names hone chahiye.
# -----------------------------
CLASS_NAMES = [
    "Apple - Apple Scab",
    "Apple - Black Rot",
    "Apple - Cedar Apple Rust",
    "Apple - Healthy",
    "Blueberry - Healthy",
    "Cherry - Powdery Mildew",
    "Cherry - Healthy",
    "Corn - Cercospora Leaf Spot",
    "Corn - Common Rust",
    "Corn - Northern Leaf Blight",
    "Corn - Healthy",
    "Grape - Black Rot",
    "Grape - Esca Black Measles",
    "Grape - Leaf Blight",
    "Grape - Healthy",
    "Orange - Huanglongbing",
    "Peach - Bacterial Spot",
    "Peach - Healthy",
    "Pepper Bell - Bacterial Spot",
    "Pepper Bell - Healthy",
    "Potato - Early Blight",
    "Potato - Late Blight",
    "Potato - Healthy",
    "Raspberry - Healthy",
    "Soybean - Healthy",
    "Squash - Powdery Mildew",
    "Strawberry - Leaf Scorch",
    "Strawberry - Healthy",
    "Tomato - Bacterial Spot",
    "Tomato - Early Blight",
    "Tomato - Late Blight",
    "Tomato - Leaf Mold",
    "Tomato - Septoria Leaf Spot",
    "Tomato - Spider Mites",
    "Tomato - Target Spot",
    "Tomato - Yellow Leaf Curl Virus",
    "Tomato - Mosaic Virus",
    "Tomato - Healthy"
]

# -----------------------------
# Load Model
# -----------------------------
@tf.keras.utils.register_keras_serializable()
def load_trained_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")
    return load_model(MODEL_PATH, compile=False)

model = load_trained_model()

# -----------------------------
# Preprocess Image
# -----------------------------
def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((150, 150))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# -----------------------------
# Predict Function
# -----------------------------
def predict(image_path):
    img_array = preprocess_image(image_path)
    prediction = model.predict(img_array, verbose=0)[0]

    predicted_index = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    if predicted_index >= len(CLASS_NAMES):
        return "Unknown Disease", confidence

    result = CLASS_NAMES[predicted_index]
    return result, confidence