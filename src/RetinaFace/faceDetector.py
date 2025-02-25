from retinaface import RetinaFace
from imutils import paths
from userData import UserData
from fileManager import FileManager

class FaceDetector():
    data = UserData()
    def __init__(self):
        self.fileManager = FileManager()

    def detect_faces_in(self, path):
        
        if not self.fileManager.checkExistence(path):
            print("Folder does not exist")
            return (False, None)
        else:
            #user_dataList = []
            for imagePath in paths.list_images(path):
                data = UserData()
                data.faces = RetinaFace.extract_faces(imagePath,align = True)
            data.id = 0
            data.name = "chams"
            #user_dataList.append(data)    
            return (True,data)   
    
