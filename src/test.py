import cv2 as cv
import numpy as np
from keras._tf_keras.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
from keras._tf_keras.keras.utils import to_categorical

# Load the trained model
model = load_model('face_recognition_model.h5')

# Assume the label encoder used during training is saved or recreated
label_encoder = LabelEncoder()
label_encoder.classes_ = np.load('classes.npy')  # Load the classes if saved during training

# Function to preprocess the frame before making predictions
def preprocess_frame(frame):
    face = cv.resize(frame, (128, 128))  # Resize the frame to the model's expected input size
    face = face.astype('float32') / 255.0  # Normalize the pixel values
    face = np.expand_dims(face, axis=0)  # Add a batch dimension
    return face

# Initialize the webcam
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to capture image")
        break

    # Detect face region (For simplicity, assuming the entire frame is the face)
    # In a real scenario, you would use a face detection algorithm like Haar Cascade or DNN to extract the face region
    
    # Preprocess the frame for the model
    preprocessed_face = preprocess_frame(frame)
    
    # Make a prediction
    predictions = model.predict(preprocessed_face)
    confidence = np.max(predictions)  # Get the highest confidence score
    predicted_label = np.argmax(predictions)  # Get the index of the highest score
    
    # Decode the label back to the username
    username = label_encoder.inverse_transform([predicted_label])[0]
    
    # Display the username and confidence on the frame
    text = f"User: {username}, Confidence: {confidence:.2f}"
    cv.putText(frame, text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
    
    # Show the frame with the prediction
    cv.imshow('Face Recognition', frame)
    
    # Exit on 'q' key
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv.destroyAllWindows()
