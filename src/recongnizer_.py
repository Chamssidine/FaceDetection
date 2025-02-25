import os
from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np
import cv2
from imutils import paths
from tets import Uname
from PyQt5.QtWidgets import  QSizePolicy
from PyQt5.QtGui import QImage, QPixmap
from fetchImage import Uimage
from tets import Uname
class Recognizer_(QObject):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    mdel = ''
    current_label_num = 0
    i = 0 
    dir = []
    name = Uname()
    stroke = 2
    fontSize = 1
    font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
    green = (0,255,0)
    white = (255,255,255)
    red = (0,0,255)
    face_cascade = cv2.CascadeClassifier("classifiers/haarcascade_frontalface_default.xml")
    cap = ''
    bd_dir = ''
    label1 = 'label1'
    label2 = 'label2'
    label3 = 'label3'
    label4 = 'label4'
    label5 = ''
    input_image = 'input'
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    uimg = Uimage()
    def normalize(self,imagPath):
                    gamma = 0.2
                    alpha = 0.1
                    tau = 3.0
                        #gamma correction
                    # imagenp = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                    # image = cv2.resize(imagenp,(135,156))
                        #gamma correction

                    img_gamma = np.power(imagPath,gamma)
                        
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
                    return img_contrast1

    def recognize(self):
        
        try:
            self.recognizer.read("model.yml")
            self.name = self.name.fetch()
            self.uimage = self.uimg.fetch()
            print({len(self.name)})
            j = 0
            input = self.input_image
            frame = cv2.imread(input)
            frame = cv2.resize(frame, None, fx=0.8, fy=0.8, interpolation=cv2.INTER_AREA)
            img_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(img_gray,1.3,5)
            for(x,y,h,w) in faces:

                roi_img = img_gray[y:y+h,x:x+w]
                img = frame[y:y+h,x:x+w]
                
                print("taille:",frame.shape[1],"x",frame.shape[0])
                print('[INFO:]')
                #raha tsy vide ilay region d'interet (ilay region misy visage)
                #fatarina @zay ilay tarehy hoe an'iza (miantson ny fonction  ^lbph.predict()^)
                if roi_img is not None:
                    roi_img = cv2.resize(roi_img,(42,60))
                    roi_img = self.normalize(roi_img)
                    id, conf = self.recognizer.predict(roi_img)
                    if frame.shape[1] > 800:
                        self.stroke = 6
                        self.fontSize = 7
                        self.font = cv2.FONT_HERSHEY_SIMPLEX
                    if conf>=0 and conf<=45:

                        cv2.rectangle(frame,(x,y),(x+w,y+h),self.green,self.stroke) 
                        self.label1.setText("ST:"+str(' visage reconnu : '+self.name[id]))
                        self.label2.setText("Conf:"+str(int(conf)))
                        self.label3.setText("id:"+str(int(id)))
                        self.label4.setStyleSheet("border: 2px solid green")
                        frame_ = cv2.resize(self.uimage[id],(127,90),cv2.INTER_AREA)
                        frame_ = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
                    # get frame infos
                        height, width, channel = frame_.shape
                        step = channel * width
                    # create QImage from RGB frame
                        qImg_ = QImage(frame_.data, width, height, step, QImage.Format_RGB888)
                    # show frame in img_label

                        self.label5.setPixmap(QPixmap.fromImage(qImg_))
                        self.label5.setScaledContents(True)
                        self.label5.setStyleSheet("border: 2px solid green;")
                    else:
                        print("id",len(self.name),"pred:",{int(conf)})

                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                        self.label1.setText("ST:"+str(' Visage non reconnu'))
                        self.label2.setText("Conf:"+str(int(conf)))
                        self.label3.setText("id:"+str(int(id)))
                        self.label4.setStyleSheet("border: 2px solid red;")
                        self.label5.setStyleSheet("border: 2px solid red;")
                        self.label5.setStyleSheet("text-align: center;")
                        self.label5.setText("%s"%"Aucun visage similaire")
                        
                try:
                    frame = cv2.resize(img,(127,90),cv2.INTER_AREA)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # get frame infos
                    height, width, channel = frame.shape
                    step = channel * width
                # create QImage from RGB frame
                    qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
                # show frame in img_label
                   
                    self.label4.setPixmap(QPixmap.fromImage(qImg))
                   
                    self.label4.setScaledContents(True)
                except Exception as e:
                    print(e)
                
                j+=1
                self.progress.emit(j)
        except Exception as e:
            print(e)
        self.finished.emit()

        