from utils.register import Register
from recognition.FullFaceRecognition import captureFullFace
from recognition.EyeRecognition import captureEyes
from recognition.NoseRecognition import captureNose
from recognition.MouthRecognition import captureMouth

def face_capture(user_name):
    user_folder = Register(user_name)
    # print(user_name, user_folder) debugging
    captureFullFace(user_name, user_folder)
    captureEyes(user_name, user_folder)
    captureNose(user_name, user_folder)
    captureMouth(user_name, user_folder)

if __name__ == '__main__':
    # face_capture(user_name="local_test") locally testing the code 
    face_capture()