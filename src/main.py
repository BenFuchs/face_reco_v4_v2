from utils.register import Register
from recognition.FullFaceRecognition import captureFullFace
from recognition.EyeRecognition import captureEyes
from recognition.NoseRecognition import captureNose
from recognition.MouthRecognition import captureMouth

def main():
    user_name, user_folder = Register()
    captureFullFace(user_name, user_folder)
    captureEyes(user_name, user_folder)
    captureNose(user_name, user_folder)
    captureMouth(user_name, user_folder)

if __name__ == '__main__':
    main()