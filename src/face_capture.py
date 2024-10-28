from utils.register import Register
from recognition.FullFaceRecognition import captureFullFace
from recognition.EyeRecognition import captureEyes
from recognition.NoseRecognition import captureNose
from recognition.MouthRecognition import captureMouth
from training import train

import cv2 as cv 

def face_capture(user_name):
    user_folder = Register(user_name)
    # print(user_name, user_folder) debugging

    cap = cv.VideoCapture(0)
    counter = 0
    
    print("Capturing face: ")
    captureFullFace(user_name, user_folder, cap)
    print("Capturing eyes: ")
    captureEyes(user_name, user_folder, cap)
    print("Capturing nose: ")
    captureNose(user_name, user_folder, cap)
    print("Capturing mouth: ")
    captureMouth(user_name, user_folder, cap)

    cap.release()

    train()

if __name__ == '__main__':
    # face_capture(user_name="local_test") #locally testing the code 
    face_capture()