import cv2
import numpy as np
from imutils import paths
import os

i = 0
ids = 0
face = []
id = 0
dir = []
label = []
for imagePath in paths.list_images('dataBase'):
            if i==0:
                
                dir.append(imagePath.split(os.path.sep)[-2])
                id +=1
                if id == ids:
                    print('dataBase'+'/'+str(imagePath.split(os.path.sep)[-2]))
            else:
                if dir[i]!=imagePath.split(os.path.sep)[-2]:
                  id+=1

            dir.append(imagePath.split(os.path.sep)[-2])
            if id == ids:
                    print('dataBase'+'/'+str(imagePath.split(os.path.sep)[-2]),id)
            i+=1
