# Plant Disease Detection System

This project provides a full-stack solution for detecting plant diseases using machine learning. It includes a Python-based model for disease classification, a Node.js backend to handle requests, and a frontend built in HTML and JavaScript for user interaction.

## Project Structure
```
plant-disease-detector/
│── backend/      # Node.js server handling image uploads and model inference
│── frontend/     # HTML frontend for user interface
│── model/        # Python machine learning model and dataset
│── README.md     # Instructions for setup and usage
```

## Prerequisites
Before running the project, ensure you have the following installed:
- [Node.js](https://nodejs.org/en/) (for the backend)
- [Python 3.x](https://www.python.org/downloads/) (for the machine learning model)
- [npm](https://www.npmjs.com/) (for Node.js dependencies)

## Setup Instructions

### 1. Clone the repository
Clone this repository to your local machine:
```bash
git clone https://github.com/SakUp004/plant-disease-detection.git
cd plant-disease-detection
```

### 2. Set up the Python Environment
1. Navigate to the `model/` directory.
2. Install required Python libraries:
    ```bash
    pip install tensorflow numpy
    ```
3. Ensure the trained model file `plant_disease_model.h5` is in the `model/` directory.
4. The `model/predict.py` script will use the trained model to make predictions based on uploaded images.

### 3. Set up the Backend (Node.js)
1. Navigate to the `backend/` directory.
2. Install the Node.js dependencies:
    ```bash
    npm install
    ```
3. Start the backend server:
    ```bash
    npm start
    ```
    The backend server will run on [http://localhost:5000](http://localhost:5000).

### 4. Set up the Frontend
1. Open the `frontend/` directory and open the HTML file in a web browser.
2. The interface will allow users to upload images of plant leaves for disease detection.
3. Once an image is uploaded, the backend will process the image and return the disease prediction.

## Usage
1. Upload a plant leaf image via the frontend.
2. The backend server processes the image and runs the Python model to predict the disease.
3. The result is displayed on the frontend with the predicted disease.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
