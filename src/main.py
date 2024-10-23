from utils.register import Register
from recognition.FullFaceRecognition import captureFullFace
from recognition.EyeRecognition import captureEyes
from recognition.NoseRecognition import captureNose
from recognition.MouthRecognition import captureMouth
from training import train

import sys 

def main():
    # add a new user (name + images)
    user_name, user_folder = Register()
    captureFullFace(user_name, user_folder)
    # captureEyes(user_name, user_folder)
    # captureNose(user_name, user_folder)
    # captureMouth(user_name, user_folder)

    # train() #trains the model after adding a new user 

if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     print("Usage: python3 main.py <username> <user_folder>")
    #     sys.exit(1)
    
    # user_name = sys.argv[1]
    # user_folder = sys.argv[2]
    
    # main(user_name, user_folder)
    main()