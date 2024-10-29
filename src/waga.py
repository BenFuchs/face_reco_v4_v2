import os
import cv2 as cv
import numpy as np
from keras._tf_keras.keras.models import load_model
from sklearn.preprocessing import LabelEncoder

# Load the trained model
model_path = '/Users/benayah/Desktop/Code/Sec_camera_project/face_reco_v4/face_reco_v4_v2/src/face_recognition_model.h5'
label_class_path = '/Users/benayah/Desktop/Code/Sec_camera_project/face_reco_v4/face_reco_v4_v2/src/classes.npy'

model = None
if os.path.exists(model_path):
    model = load_model(model_path)
    print(f"Loaded model from: {model_path}")
else:
    print(f"Model file does not exist: {model_path}. Please register a user to create the model.")

label_encoder = LabelEncoder()
if os.path.exists(label_class_path):
    label_encoder.classes_ = np.load(label_class_path)
    print(f"Loaded label classes from: {label_class_path}")
else:
    print(f"Classes file does not exist: {label_class_path}. Please ensure training has been performed.")

# Function to preprocess the frame before making predictions
def preprocess_frame(frame):
    face = cv.resize(frame, (128, 128))  # Resize the frame to the model's expected input size
    face = face.astype('float32') / 255.0  # Normalize the pixel values
    face = np.expand_dims(face, axis=0)  # Add a batch dimension
    return face

# Load custom Haar Cascade for full face detection
haar_cascade_path = "/Users/benayah/Desktop/Code/Sec_camera_project/face_reco_v4/face_reco_v4_v2/src/haarcascades/haar_full_face.xml"
face_cascade = cv.CascadeClassifier(haar_cascade_path)

if face_cascade.empty():
    raise FileNotFoundError(f"Haar cascade file not found at {haar_cascade_path}")

def testRecognize():
    if model is None:
        print("Model not loaded. Please ensure a model is trained and available.")
        return
    
    cap = cv.VideoCapture(0)
    last_recognized_user = None  # Track the last recognized username

    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to capture image")
            break

        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=12)
        
        preprocessed_face = preprocess_frame(frame)
        predictions = model.predict(preprocessed_face)
        confidence = np.max(predictions)
        predicted_label = np.argmax(predictions)
        username = label_encoder.inverse_transform([predicted_label])[0]

        # Check confidence threshold and if user is different from last recognized
        if confidence > 0.9:
            if username != last_recognized_user:
                print(f"Recognized new user: {username} with confidence {confidence:.2f}")
                last_recognized_user = username
                yield username  # Yielding only when a new unique username is detected
            elif last_recognized_user == username:
                print(f"Recognized same user again: {username}")
                yield username  # Yield again if the same user is repeatedly detected

        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # cap.release()
    # cv.destroyAllWindows()

# testRecognize()