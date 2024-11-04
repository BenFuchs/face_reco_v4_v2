import os
import requests

def Register():
    # Set the base path to where `frames` should be created, using an absolute path to the face recognition project.
    base_dir = '/Users/benayah/Desktop/Code/Sec_camera_project/face_reco_v4/face_reco_v4_v2/src/'
    frames_dir = os.path.join(base_dir, 'frames')

    # Ensure `frames` exists
    os.makedirs(frames_dir, exist_ok=True)
    
    # Create user folder within `frames`
    user_name = input("Please enter username: ")
    userFolder = os.path.join(frames_dir, user_name)
    os.makedirs(userFolder, exist_ok=True)  # Create user folder if it doesn't exist

    #register user in the server -> activating register function now registers in the backend with the request
    password = input("Please input your password: ")
    email = input("Please input your email: ")
    url = 'http://localhost:5000/register'  # Update with your backend URL if different
    payload = {"username": user_name, "password": password, "email": email}
    response = requests.post(url, json=payload)


    if response.status_code == 201:
        print(f"User {user_name} registered successfully.")
    elif response.status_code == 200:
        print(f"User {user_name} was already registered.")
    else:
        print(f"Error registering user {user_name}: {response.json().get('error')}")

    return userFolder, user_name
