import os

def Register(user_name):
    # Set the base path to where `frames` should be created, using an absolute path to the face recognition project.
    base_dir = '/Users/benayah/Desktop/Code/Sec_camera_project/face_reco_v4/face_reco_v4_v2/src/'
    frames_dir = os.path.join(base_dir, 'frames')

    # Ensure `frames` exists
    os.makedirs(frames_dir, exist_ok=True)
    
    # Create user folder within `frames`
    userFolder = os.path.join(frames_dir, user_name)
    os.makedirs(userFolder, exist_ok=True)  # Create user folder if it doesn't exist

    return userFolder
