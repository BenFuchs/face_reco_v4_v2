import time
import os
import cv2 as cv
import numpy as np
from keras._tf_keras.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import requests


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



def recognize_and_log_user(user_id):
    url = 'http://localhost:5000/recognize_user'  # Update with your backend URL if different
    payload = {"user_id": user_id}
    response = requests.post(url, json=payload)
    
    if response.status_code == 201:
        print(f"User {user_id} recognized and logged successfully.")
    elif response.status_code == 200:
        print(f"User {user_id} was already logged.")
    else:
        print(f"Error logging user {user_id}: {response.json().get('error')}")

def testRecognize():
    if model is None:
        print("Model not loaded. Please ensure a model is trained and available.")
        return
    
    cap = cv.VideoCapture(0)
    last_recognized_user = None  # Track the last recognized username
    unknown_folder = '/Users/benayah/Desktop/Code/Sec_camera_project/face_reco_v4/face_reco_v4_v2/src/unknown'

    os.makedirs(unknown_folder, exist_ok=True)


    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to capture image")
            break

        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=15)
        
        if len(faces) > 0:
            # Process each detected face
            for (x, y, w, h) in faces:
                face_region = frame[y:y + h, x:x + w]  # Crop the face region
                preprocessed_face = preprocess_frame(face_region)
                predictions = model.predict(preprocessed_face)
                confidence = np.max(predictions)
                predicted_label = np.argmax(predictions)
                username = label_encoder.inverse_transform([predicted_label])[0]

                # Draw the rectangle around the detected face
                cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # Display username if confidence is high enough
                if confidence > 0.9:
                    if username != last_recognized_user:
                        print(f"Recognized new user: {username} with confidence {confidence:.2f}")
                        last_recognized_user = username
                        recognize_and_log_user(user_id=username)

                    else:
                        print(f"Recognized same user again: {username}")

                    # Display the recognized username and confidence on the frame
                    cv.putText(frame, f"{username} ({confidence:.2f})", (x, y - 10),
                               cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                else :
                    print("Unknown user in front of camera")
                    username = "Unknown"
                    cv.putText(frame, f"{username}", (x, y - 10),
                               cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    # Save the snapshot of the unknown face
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    unknown_image_path = os.path.join(unknown_folder, f"unknown_{timestamp}.jpg")
                    cv.imwrite(unknown_image_path, face_region)
                    print(f"Snapshot saved to {unknown_image_path}")


        # Show the frame with the drawn rectangles and labels
        cv.imshow("User Capture", frame)

        # Break the loop when 'q' is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

# Call the function to start recognition
if __name__ == '__main__':
    testRecognize()

