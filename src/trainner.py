import numpy as np
import cv2
from PyQt5.QtCore import QObject, QThread, Qt, pyqtSignal
from imutils import paths
from PIL import Image
import os
import pickle

class Train(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    recognizer = cv2.face.LBPHFaceRecognizer_create(3,8)
    faces_data = []
    labels = []
    db_directory = 'dataBase/chams'
    current_label_num = 2
    label = ""
    i = 0 
    dir = []
    def run(self):
        
        try:
            for imagePath in paths.list_images(self.db_directory):
                    if self.i == 0:
                        gamma = 0.2
                        alpha = 0.1
                        tau = 3.0

                        #gamma correction
                        image = cv2.imread(imagePath)
                        imagenp = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                        image = cv2.resize(imagenp,(42,60))
                        #gamma correction

                        img_gamma = np.power(image,gamma)
                        
                        #DOG

                        imagenp1 = cv2.GaussianBlur(img_gamma,(0,0),1, borderType=cv2.BORDER_REPLICATE)
                        imagenp2 = cv2.GaussianBlur(img_gamma,(0,0),2, borderType=cv2.BORDER_REPLICATE)
                        
                        img_dog = imagenp1 - imagenp2
                        img_dog = img_dog / np.amax(np.abs(img_dog))
                       

                        #contrast equalisation
                        img_contrast1 = np.abs(img_dog)
                        img_contrast1 = np.power(img_contrast1, alpha)
                        img_contrast1 = np.mean(img_contrast1)
                        img_contrast1 = np.power(img_contrast1,1.0/alpha)
                        img_contrast1 = img_dog/img_contrast1
                        img_contrast2 = np.abs(img_contrast1)
                        img_contrast2 = img_contrast2.clip(0,tau)
                        img_contrast2 = np.mean(img_contrast2)
                        img_contrast2 = np.power(img_contrast2,1.0/alpha)
                        img_contrast2 = img_contrast1/img_contrast2
                        img_contrast = tau*np.tanh((img_contrast2/tau))
                        img_contrast1 = (255.0*(img_contrast+0.5)).clip(0,255).astype(np.uint8)
                        self.faces_data.append(img_contrast1)
                        self.labels.append(self.current_label_num)
                        self.dir.append(imagePath.split(os.path.sep)[-2])
                    else:
                        if (self.dir[self.i]!=imagePath.split(os.path.sep)[-2]):
                            # self.current_label_num+=1
                            continue;
                          
                    image = cv2.imread(imagePath)
                    imagenp = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                    imagenp = cv2.resize(imagenp,(42,60))
                    gamma = 0.2
                    alpha = 0.1
                    tau = 3.0

                        #gamma correction
                    image = cv2.imread(imagePath)
                    imagenp = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                    image = cv2.resize(imagenp,(42,60))
                        #gamma correction

                    img_gamma = np.power(image,gamma)
                        
                        #DOG

                    imagenp1 = cv2.GaussianBlur(img_gamma,(0,0),1, borderType=cv2.BORDER_REPLICATE)
                    imagenp2 = cv2.GaussianBlur(img_gamma,(0,0),2, borderType=cv2.BORDER_REPLICATE)
                        
                    img_dog = imagenp1 - imagenp2
                    img_dog = img_dog / np.amax(np.abs(img_dog))
                       

                    img_contrast1 = np.abs(img_dog)
                    img_contrast1 = np.power(img_contrast1, alpha)
                    img_contrast1 = np.mean(img_contrast1)
                    img_contrast1 = np.power(img_contrast1,1.0/alpha)
                    img_contrast1 = img_dog/img_contrast1
                    img_contrast2 = np.abs(img_contrast1)
                    img_contrast2 = img_contrast2.clip(0,tau)
                    img_contrast2 = np.mean(img_contrast2)
                    img_contrast2 = np.power(img_contrast2,1.0/alpha)
                    img_contrast2 = img_contrast1/img_contrast2
                    img_contrast = tau*np.tanh((img_contrast2/tau))
                    img_contrast1 = (255.0*(img_contrast+0.5)).clip(0,255).astype(np.uint8)
                    self.faces_data.append(img_contrast1)
                    self.labels.append(self.current_label_num)
                    self.dir.append(imagePath.split(os.path.sep)[-2])
                    print(self.labels)
                    self.i+=1
                    cv2.imshow("x",img_contrast1)
                    cv2.waitKey(100)
            self.recognizer.train(self.faces_data,np.array(self.labels))
            with open('labelData.pickle','wb') as f:
                pickle.dump(self.labels,f)
            x = self.recognizer.write(self.db_directory+"/model.yml")
            self.progress.emit(self.i + 1)
            print('progrss',{self.i})
                    
            self.finished.emit()
        except Exception as e:
            self.progress.emit(e)
            print(e)
            self.finished.emit()
