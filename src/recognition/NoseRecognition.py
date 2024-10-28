import os 
import cv2 as cv 
import mediapipe as mp 

from utils.saveFrame import save_frame

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

# Load custom Haar Cascade for eye detection (optional if using MediaPipe for eyes)
haar_cascade_path = "/Users/benayah/Desktop/Code/Sec_camera_project/face_reco_v4/face_reco_v4_v2/src/haarcascades/haar_nose.xml"
face_cascade = cv.CascadeClassifier(haar_cascade_path)

if face_cascade.empty():
    raise FileNotFoundError(f"Haar cascade file not found at {haar_cascade_path}")



def get_existing_frame_count(userFolder, frame_type):
    """Ensure the frame type folder exists and return the count of saved frames."""
    frame_path = os.path.join(userFolder, frame_type)
    os.makedirs(frame_path, exist_ok=True)
    return len([f for f in os.listdir(frame_path) if f.endswith(('.jpg', '.png'))])

def crop_region(frame, x1, y1, x2, y2):
    """Crops the specified region from the frame."""
    return frame[y1:y2, x1:x2]

def captureNose(user_name, user_folder, cap, frame_max=50):
    # cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    os.makedirs(user_folder, exist_ok=True)  # Checks if the folder for the user exists; if not, creates it

    current_frame_count = get_existing_frame_count(user_folder, "NOSE")

    try:
        while cap.isOpened() and current_frame_count < frame_max:
            ret, frame = cap.read()
            if not ret:
                print("Image was not captured properly, ERROR!")
                break
            
            #convert to grey-scale for the haar-cascade recognition 
            gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.05, minNeighbors=10)

            # Convert frame to RGB for MediaPipe processing
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            # Process the landmarks for the nose if a face is detected
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    nose_indices = [
                        1,   # Tip of the nose
                        2,   # Nose bottom
                        98,  # Nose left (nostril area)
                        327, # Nose right (nostril area)
                        6,   # Nose bridge (lower part)
                        197, # Nose bridge (middle part)
                        195  # Nose bridge (upper part)
                    ]

                    # Get nose landmark coordinates
                    nose_landmarks = [face_landmarks.landmark[i] for i in nose_indices]

                    def get_bounding_box(landmarks, image_width, image_height):
                        """Calculate the bounding box for the given landmarks."""
                        x_coords = [int(landmark.x * image_width) for landmark in landmarks]
                        y_coords = [int(landmark.y * image_height) for landmark in landmarks]
                        return min(x_coords), min(y_coords), max(x_coords), max(y_coords)

                    # Get bounding box for the nose
                    h, w, _ = frame.shape
                    x1, y1, x2, y2 = get_bounding_box(nose_landmarks, w, h)

                    # Crop the nose region
                    nose_crop = crop_region(frame, x1, y1, x2, y2)

                    # Save the cropped image if the nose is detected and within the max limit
                    if nose_crop.size > 0 and current_frame_count < frame_max and len(faces) > 0:
                        save_frame(nose_crop, user_name, user_folder, "NOSE")
                        current_frame_count += 1

                    # Draw rectangle around the nose on the original frame for visualization
                    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv.putText(frame, f"Nose: {current_frame_count}/{frame_max}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            # cv.imshow("Nose Capture", frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred: {e}")

