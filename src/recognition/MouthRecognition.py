import os 
import cv2 as cv 
import mediapipe as mp 

from utils.saveFrame import save_frame

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)



# Load custom Haar Cascade for eye detection (optional if using MediaPipe for eyes)
haar_cascade_path = "/Users/benayah/Desktop/Code/Sec_camera_project/face_reco_v4/face_reco/face_reco_v4_v2/src/haarcascades/haar_mouth.xml"
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

def captureMouth(user_name, user_folder, frame_max=50):
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    os.makedirs(user_folder, exist_ok=True)  # Checks if the folder for the user exists; if not, creates it

    current_frame_count = get_existing_frame_count(user_folder, "MOUTH")

    try:
        while cap.isOpened() and current_frame_count < frame_max:
            ret, frame = cap.read()
            if not ret:
                print("Image was not captured properly, ERROR!")
                break

            #convert to grayscale for haar cascade processing
            gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.05, minNeighbors=10)

            # Convert frame to RGB for MediaPipe processing
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            # Draw rectangles around detected mouth if landmarks are found
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Mouth landmarks indices based on MediaPipe
                    mouth_indices = [
                                        61, 146, 91, 181,  # corners of the mouth
                                        84, 17,           # top of the upper lip
                                        314, 405,        # corners of the lips
                                        321, 375,        # lower lip
                                        291, 308,        # bottom corners of the mouth
                                        78, 95, 88, 178,  # upper lip and surrounding area
                                        77, 79, 80, 81,  # additional upper lip landmarks
                                        82, 83           # more upper lip landmarks
                                    ]


                    def get_bounding_box(mouth_landmarks, image_width, image_height):
                        """Calculate the bounding box for the given mouth landmarks."""
                        x_coords = [int(landmark.x * image_width) for landmark in mouth_landmarks]
                        y_coords = [int(landmark.y * image_height) for landmark in mouth_landmarks]
                        return min(x_coords), min(y_coords), max(x_coords), max(y_coords)

                    # Get bounding box
                    h, w, _ = frame.shape
                    x1, y1, x2, y2 = get_bounding_box(
                        [face_landmarks.landmark[i] for i in mouth_indices], w, h
                    )

                    # Crop the mouth region
                    mouth_crop = crop_region(frame, x1, y1, x2, y2)

                    # Save the cropped image if the mouth is detected and within the max limit
                    if mouth_crop.size > 0 and current_frame_count < frame_max and len(faces) > 0:
                        save_frame(mouth_crop, user_name, user_folder, "MOUTH")
                        current_frame_count += 1

                    # Draw rectangle around the mouth on the original frame for visualization
                    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv.putText(frame, f"Mouth: {current_frame_count}/50", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            # cv.imshow("Mouth Capture", frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cap.release()
        cv.destroyAllWindows()

