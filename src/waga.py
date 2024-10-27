import cv2 as cv
import numpy as np
from keras._tf_keras.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
from keras._tf_keras.keras.utils import to_categorical

# Load the trained model
model_path = '/Users/benayah/Desktop/Code/Sec_camera_project/face_reco_v4/face_reco_v4_v2/src/face_recognition_model.h5'
model = load_model(model_path)

# Assume the label encoder used during training is saved or recreated
label_class_path = '/Users/benayah/Desktop/Code/Sec_camera_project/face_reco_v4/face_reco_v4_v2/src/classes.npy'
label_encoder = LabelEncoder()
label_encoder.classes_ = np.load(label_class_path)  # Load the classes if saved during training

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
    # Initialize the webcam
    cap = cv.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to capture image")
            break

        # Change image to greyscale for the Haar cascade recognition 
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=12)
        
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
        # cv.putText(frame, text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
        print(text)
        
        # Frame the face of current user 
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Show the frame with the prediction
        # cv.imshow('Face Recognition', frame)
        
        # # Exit on 'q' key
        # if cv.waitKey(1) & 0xFF == ord('q'):
        #     break

    # Release the webcam and close windows
    cap.release()
    cv.destroyAllWindows()
