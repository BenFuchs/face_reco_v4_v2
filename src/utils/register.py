import os

def Register():
    # User registration and folder creation 
    user_name = input("Please input your name: ")  # Input name 
    if user_name:
        userFolder = os.path.join('frames', user_name)  # Create folder name for user 
        os.makedirs(userFolder, exist_ok=True)  # Create folder 

    return user_name, userFolder

Register()