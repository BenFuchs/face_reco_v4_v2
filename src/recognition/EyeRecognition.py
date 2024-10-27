import os 
import cv2 as cv 
import mediapipe as mp 

from utils.saveFrame import save_frame

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

# Load custom Haar Cascade for eye detection (optional if using MediaPipe for eyes)
haar_cascade_path = "/Users/benayah/Desktop/Code/Sec_camera_project/face_reco_v4/face_reco/face_reco_v4_v2/src/haarcascades/haar_eye.xml"
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

def captureEyes(user_name, user_folder, frame_max=50):
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    os.makedirs(user_folder, exist_ok=True)  # Checks if the folder for the user exists; if not, creates it

    # Get the existing frame count separately for left and right eyes
    left_eye_frame_count = get_existing_frame_count(user_folder, "LEFT_EYE")
    right_eye_frame_count = get_existing_frame_count(user_folder, "RIGHT_EYE")

    left_eye_indices = [
                            31,  # left eye outer corner
                            30,  # left eye upper left corner
                            56,  # left eye upper right corner
                            26,  # left eye lower right corner
                            110,  # left eye lower left corner
                            25,  # left eye inner corner
                            159,  # left eye upper middle
                            143,  # left eye lower middle
                            46,    # left eyebrow outer corner (for height)
                            55   # left eyebrow inner corner (for height)
                        ]

 
    right_eye_indices = [
                        446,  # right eye outer corner
                        286,  # right eye upper left corner
                        467,  # right eye upper right corner
                        448,  # right eye lower right corner
                        453,  # right eye lower left corner
                        249,  # right eye inner corner
                        473,  # right eye upper middle
                        374,  # right eye lower middle
                        285,  # right eyebrow inner corner (for height)
                        300   # right eyebrow outer corner (for height)
                    ]

    try:
        while cap.isOpened() and (left_eye_frame_count < frame_max or right_eye_frame_count < frame_max):
            ret, frame = cap.read()
            if not ret:
                print("Image was not captured properly, ERROR!")
                break

            # Convert to grayscale for Haar cascade processing
            gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.05, minNeighbors=10)

            # Convert frame to RGB for MediaPipe processing
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            # Draw rectangles around detected eyes if landmarks are found
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Get coordinates for left and right eyes with updated indices
                    left_eye = [face_landmarks.landmark[i] for i in left_eye_indices]
                    right_eye = [face_landmarks.landmark[i] for i in right_eye_indices]

                    def get_bounding_box(eye_landmarks, image_width, image_height):
                        """Calculate the bounding box for the given eye landmarks."""
                        x_coords = [int(landmark.x * image_width) for landmark in eye_landmarks]
                        y_coords = [int(landmark.y * image_height) for landmark in eye_landmarks]
                        return min(x_coords), min(y_coords), max(x_coords), max(y_coords)

                    # Get bounding boxes for each eye
                    h, w, _ = frame.shape
                    left_x1, left_y1, left_x2, left_y2 = get_bounding_box(left_eye, w, h)
                    right_x1, right_y1, right_x2, right_y2 = get_bounding_box(right_eye, w, h)

                    # Crop the eye regions
                    left_eye_crop = crop_region(frame, left_x1, left_y1, left_x2, left_y2)
                    right_eye_crop = crop_region(frame, right_x1, right_y1, right_x2, right_y2)

                    # Save the cropped images if eyes are detected and within the max limit
                    if left_eye_crop.size > 0 and left_eye_frame_count < frame_max and len(faces) > 0:
                        save_frame(left_eye_crop, user_name, user_folder, "LEFT_EYE")
                        left_eye_frame_count += 1

                    if right_eye_crop.size > 0 and right_eye_frame_count < frame_max and len(faces) > 0:
                        save_frame(right_eye_crop, user_name, user_folder, "RIGHT_EYE")
                        right_eye_frame_count += 1

                    # Draw rectangles around the eyes on the original frame for visualization
                    cv.rectangle(frame, (left_x1, left_y1), (left_x2, left_y2), (0, 255, 0), 2)
                    cv.rectangle(frame, (right_x1, right_y1), (right_x2, right_y2), (0, 255, 0), 2)

            cv.putText(frame, f"Left Eye: {left_eye_frame_count}/50", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv.putText(frame, f"Right Eye: {right_eye_frame_count}/50", (10, 60), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            # cv.imshow("Eye Capture", frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cap.release()
        cv.destroyAllWindows()
