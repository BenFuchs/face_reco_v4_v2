import os 
import cv2 as cv 
import mediapipe as mp 

from utils.saveFrame import save_frame


# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

# Load custom Haar Cascade for full face detection
haar_cascade_path = "/Users/benayah/Desktop/Code/OpenCV/face_reco_v4/face_recognition_project/config/haarcascades/haar_full_face.xml"
face_cascade = cv.CascadeClassifier(haar_cascade_path)

if face_cascade.empty():
    raise FileNotFoundError(f"Haar cascade file not found at {haar_cascade_path}")

cap = cv.VideoCapture(0)

def get_existing_frame_count(userFolder, frame_type):
    """Ensure the frame type folder exists and return the count of saved frames."""
    frame_path = os.path.join(userFolder, frame_type)
    os.makedirs(frame_path, exist_ok=True)
    return len([f for f in os.listdir(frame_path) if f.endswith(('.jpg', '.png'))])

def captureFullFace(user_name, user_folder,frame_max = 50):

    os.makedirs(user_folder, exist_ok=True) #checks if the folder for the user exists, if not creates it

    current_frame_number = get_existing_frame_count(user_folder, "Full_Face")

    try:
        while cap.isOpened() and current_frame_number < frame_max:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("Failed to capture frame")
                break
            
            # Ensure the frame has the right number of channels
            if frame.shape[2] != 3:
                print("Captured frame does not have 3 channels!")
                continue

            # Change image to greyscale for the Haar cascade recognition 
            gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=12)

            # Convert frame to RGB for MediaPipe processing
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            # Check if any faces are detected using Haar Cascade
            if len(faces) > 0 and results.multi_face_landmarks:
                # Draw rectangles around detected faces
                for (x, y, w, h) in faces:
                    cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # Save the frame only if a face is detected
                save_frame(frame, user_name, user_folder, "FULL_FACE")
                current_frame_number += 1

            # Display current frame count
            cv.putText(frame, f"{current_frame_number}/50", (10, 30), cv.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 255, 0), 2)
            cv.imshow("Full Face Capture", frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cap.release()  # Release the camera
        cv.destroyAllWindows()