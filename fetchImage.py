from imutils import paths
import os
import cv2
class Uimage():
    
    dir = []
    name = []
    i = 0 
    l_img = []
    def fetch(self):
        for imagePath in paths.list_images('dataBase'):
            if self.i==0:
                
                self.dir.append(imagePath.split(os.path.sep)[-2])
                self.name.append(imagePath.split(os.path.sep)[-2])
                x = cv2.imread(imagePath)
                self.l_img.append(x)
            else:
                if self.dir[self.i]!=imagePath.split(os.path.sep)[-2]:
                    self.name.append(imagePath.split(os.path.sep)[-2])
                    x = cv2.imread(imagePath)
                    self.l_img.append(x)
            self.dir.append(imagePath.split(os.path.sep)[-2])
            self.i+=1
        return self.l_img
