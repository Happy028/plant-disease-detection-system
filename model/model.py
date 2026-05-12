import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'plant_disease_model.h5')
model = load_model(model_path)

# Load class names safely
dataset_path = r"D:\downloads\plant-disease-detection-main\plant-disease-detection-main\dataset\train"

class_names = [d for d in sorted(os.listdir(dataset_path)) 
               if os.path.isdir(os.path.join(dataset_path, d))]

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(150,150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

def predict(img_path):
    img_array = preprocess_image(img_path)
    prediction = model.predict(img_array)

    index = np.argmax(prediction)

    if index >= len(class_names):
        return "Unknown", 0.0

    predicted_class = class_names[index]
    confidence = float(np.max(prediction))

    return predicted_class, confidence