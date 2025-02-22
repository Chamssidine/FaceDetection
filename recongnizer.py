import os
import numpy as np
import cv2
from imutils import paths
from PyQt5.QtWidgets import  QSizePolicy
from PyQt5.QtGui import QImage, QPixmap
from tets import Uname
import pyfirmata
class Recognizer():
    def __init__(self,label,label1,label2,label3,model,recognizer):
        self.recognizer =recognizer
        self.label_id = label1
        self.label_nom = label2
        self.label_conf = label3
        self.recognizer.read(model)
        self.current_label_num = 0
        self.label = ""
        self.i = 0 
        self.dir = []
        self.name = []
        self.stroke = 2
        self.fontSize = 1
        self.font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        self.green = (0,255,0)
        self.white = (255,255,255)
        self.red = (0,0,255)
        self.face_cascade = cv2.CascadeClassifier("classifiers/haarcascade_frontalface_default.xml")
        self.bd_dir = ''
        self.label = label
        self.name1 = Uname()
        self.cap = ''

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

    def red_led(self):
        self.LED_red.write(self.HIGH)
        self.LED_pin.write(self.LOW)
    def moteur(self,rec):
        if rec is True:
            self.LED_red.write(self.LOW)
            self.LED_pin.write(self.HIGH)
        else:
            self.LED_pin.write(self.LOW)
            
    def recognize(self,cap):
        
        self.name = self.name1.fetch() 
        self.cap = cap
        ret, frame = self.cap.read()
        frame = cv2.flip(frame,1)
        img_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(img_gray,1.3,5)
        for(x,y,h,w) in faces:
            roi_img = img_gray[y:y+h,x:x+w]
            #raha tsy vide ilay region d'interet (ilay region misy visage)
            #fatarina @zay ilay tarehy hoe an'iza (miantson ny fonctio  ^lbph.predict()^)
            if roi_img is not None:
                roi_img = cv2.resize(roi_img,(42,60))
                roi_img = self.normalize(roi_img)
                id, conf = self.recognizer.predict(roi_img)
                if frame.shape[1] > 800:
                    self.stroke = 6
                    self.fontSize = 7
                    self.font = cv2.FONT_HERSHEY_COMPLEX
                if conf>=0 and conf<=170:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),self.green,self.stroke) 
                    cv2.putText(frame,str(self.name[id]),(x,y+20),self.font,self.fontSize,self.white,self.stroke)
                    self.label_id.setText("id: "+str(id))
                    self.label_nom.setText("Nom:"+str(self.name[id]))
                    self.label_conf.setText("Confidence:"+str(int(conf)))
                    self.label.setStyleSheet("border: 3px solid green;")
                    # self.moteur(True)
                
                else:
                    print("id",id,"pred:",{int(conf)})
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                    cv2.putText(frame,"visage non reconnu",(x-10,y-10),self.font,self.fontSize,self.red,self.stroke)
                    self.label.setStyleSheet("border: 3px solid red;")
                    # self.moteur(False)
                    # self.red_led()
                    # self.label_conf.setText("Confidence:"+str(int(conf)))
            
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame,(200,180),cv2.INTER_AREA)
        # get frame infos
        height, width, channel = frame.shape
        step = channel * width
        # create QImage from RGB frame
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        # show frame in img_label
        
        self.label.setPixmap(QPixmap.fromImage(qImg))
        self.label.setScaledContents(True)
        
        