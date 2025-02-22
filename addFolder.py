import numpy as np
import cv2
from PyQt5.QtCore import QMessageLogContext, QMessageLogger, QObject, QThread, Qt, pyqtSignal
from imutils import paths
from PIL import Image
import os
import pickle
from PyQt5.QtWidgets import (
    QApplication,
    QInputDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

class AddFolder(QWidget,QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces_data = []
    labels = []
    face_cascade = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    db_directory = 'dataBase'
    i = 0 
    admin_code ='admin'
    param = ''
    def add(self,src_folder):

        if src_folder=='':
            QMessageLogContext.warning(self,'Erreur','%s'%'Veuillez spécifier le dossier')
        else:
            name = self.getUsername()
            name =  str(self.ROOT_DIR)+"/"+str(self.db_directory)+"/"+str(name)
            self.on_action_create_folder(str(name))
            
            if self.path!='':
                for image in paths.list_images(src_folder):
                    image=cv2.imread(image)
                    frame_ = cv2.resize(image, None, fx=0.8, fy=0.8, interpolation=cv2.INTER_AREA)

                    # convert frame to GRAY format
                    gray = cv2.cvtColor(frame_, cv2.COLOR_BGR2GRAY)

                     # detect rect faces
                    face_rects = self.face_cascade.detectMultiScale(gray, 1.3, 5)

                    # for all detected faces
                    for (x, y, w, h) in face_rects:
                        roi_img = gray[y:y+h,x:x+w]
                        cv2.imwrite(str(self.path)+"/"+str(self.i)+".jpg",roi_img)
                    self.i+=1
            QMessageBox.information(self,'Info','%s'%'Opération terminée avec succès')                
            self.path=''
        self.progress.emit(self.i + 1)
        self.finished.emit()
    def getUsername(self):  
        input, ok = QInputDialog.getText(self,'Nom:', '%s'%'Saisir le  nom de la personne sur ces photos:')
        if ok:
            if input == '':
                QMessageBox.warning(self,'Attention','%s'%'merci de saisir le nom')
                self.showDialog()
            else:
                self.param=str(input)
                return self.param        
    #creation de dossier pour la personne
    def on_action_create_folder(self,dir_name):
        
        if os.path.exists(dir_name):
            rep = self.alert_Dialog()
            if rep:
                if(self.request_passwd()):
                    self.path = dir_name+'/'
                    
            else:
                    
                self.path = dir_name+'/'
                
                
            
        else:  
                os.makedirs(dir_name,777)
                self.path = dir_name+'/'
        
    def alert_Dialog(self):
        messageConfirmation = "%s"%str("Non existe deja, OUI pour ecrasé \n NON pour ajouter ")
        reponse = QMessageBox.question(self,"Confirmation",messageConfirmation,QMessageBox.Yes,QMessageBox.No)
        if reponse == QMessageBox.Yes:
            return True
        else:
            self.showDialog()
    def request_passwd(self):   
        input, ok = QInputDialog.getText(self,'Nom:',"%s" %'Entrer le code secret  avant de proceder à cette operation :')
        if ok:
            if input  != self.admin_code:
                QMessageBox.critical(self,'Erreur','%s'%'code erroné')
                return False
            else:
                return True