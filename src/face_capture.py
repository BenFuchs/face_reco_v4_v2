from utils.register import Register
from recognition.FullFaceRecognition import captureFullFace
from recognition.EyeRecognition import captureEyes
from recognition.NoseRecognition import captureNose
from recognition.MouthRecognition import captureMouth
from training import train

def face_capture(user_name):
    user_folder = Register(user_name)
    # print(user_name, user_folder) debugging
    print("Capturing face: ")
    # captureFullFace(user_name, user_folder)
    print("Capturing eyes: ")
    captureEyes(user_name, user_folder)
    print("Capturing nose: ")
    captureNose(user_name, user_folder)
    print("Capturing mouth: ")
    captureMouth(user_name, user_folder)

    # train()

if __name__ == '__main__':
    # face_capture(user_name="local_test") locally testing the code 
    face_capture()