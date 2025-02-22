import os
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal
from PyQt5.QtWidgets import *
import numpy as np
import cv2
from imutils import paths
from PIL import Image
import pickle
from terminated import Dialog

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces_data = []
    labels = []
    db_directory = 'dataBase'
    current_label_num = 0
    label = ""
    i = 0 
    operation = Dialog()
    dir = []
    
    def run(self):
            for imagePath in paths.list_images(self.db_directory):
                if self.i == 0:
                    self.dir.append(imagePath.split(os.path.sep)[-2])
                else:
                    if (self.dir[self.i]!=imagePath.split(os.path.sep)[-2]):
                        self.current_label_num+=1
                image = Image.open(imagePath).convert('L')
                imagenp = np.array(image,'uint8')
                self.faces_data.append(imagenp)
                self.labels.append(self.current_label_num)
                self.dir.append(imagePath.split(os.path.sep)[-2])
                self.i+=1
            
    
            self.recognizer.train(np.array(self.faces_data,dtype='object'),np.array(self.labels))
            with open('labelData.pickle','wb') as f:
                pickle.dump(self.labels,f)
            self.recognizer.save("model.yml")


    


