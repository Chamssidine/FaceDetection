from imutils import paths
import os
import cv2
import numpy as np
from recongnizer import Recognizer
import threading

face = []
label = []
def fetch():
        dir = []
        name = []
        i = 0 
        for imagePath in paths.list_images('dataBase'):
            if i==0:
                dir.append(imagePath.split(os.path.sep)[-2])
                name.append(imagePath.split(os.path.sep)[-2])
            else:
                if dir[i]!=imagePath.split(os.path.sep)[-2]:
                  name.append(imagePath.split(os.path.sep)[-2])
            dir.append(imagePath.split(os.path.sep)[-2])
            i+=1
        return(name)

name = fetch()
print(name)
for i in range(len(name)):
    for img in paths.list_images('dataBase/'+name[i]):
        image=cv2.imread(img,cv2.IMREAD_GRAYSCALE)
        face.append(image)
        label.append(0)
    recognizer = cv2.face.LBPHFaceRecognizer_create(3,8)
    recognizer.train(face,np.array(label))
    recognizer.save('dataBase/test.yml')


