from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QGraphicsView, QInputDialog, QMessageBox, QMainWindow, QSizePolicy
from	PyQt5.QtCore	import 	QThread, pyqtSlot
from Ui_new_update import Ui_MainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import pyfirmata
import cv2
import os
from imutils import paths
# from recongnizer import Recognizer
# from recongnizer_ import Recognizer_
# from trainner import Train
class Main_control_access(QMainWindow,Ui_MainWindow):
    
    def __init__(self,parent=None):
        super(Main_control_access,self).__init__(parent)
        self.setupUi(self)
        self.pushButton_ouvrir_Image.clicked.connect(self.pushButton_source_image_clicked)
        self.pushButton_Enregistrer.clicked.connect(self.showDialog)
        self.pushButton_Demarrer.clicked.connect(self.recognize_)
        self.pushButton_authentifier.clicked.connect(self.pushButton_authentifier_clicked)
        self.pushButton_ouvrir_Dossier.clicked.connect(self.pushButton_source_folder_clicked)
        self.pushButton_2.clicked.connect(self.addFolder)
        self.pix = QPixmap
        self.scene = QtWidgets.QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.face_cascade = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')
        self.db_directory = 'dataBase'
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.param = 'none'
        self.rec = ''
        self.path =''
        self.i = 0
        self.id = 0
        self.names = []
        self.limit_raw = 50
        self.admin_code = 'admin'
        # self.port = 'COM7'
        # try:
        #     self.board=pyfirmata.Arduino(self.port)
        #     self.vert = self.board.get_pin('d:13:o')
        #     self.rouge = self.board.get_pin('d:12:o')
        # except Exception as e:
        #     print(e)

        self.timer_1 = QTimer()
        self.model = ''


    def recognize_(self):
        if self.lineEdit_ouvrir_Image.text()=='':
            QMessageBox.warning(self,'Attention','%s'%'merci spécifier l''image')
            
        else:
            self.thread = QThread()
            self.worker = Recognizer_()
            self.worker.input_image = self.lineEdit_ouvrir_Image.text()
            self.worker.label1 = self.label_7
            self.worker.label2 = self.label_8
            self.worker.label3 = self.label_3
            self.worker.label4 = self.label_2
            self.worker.label5 = self.label_6
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.recognize)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            # self.worker.progress.connect(self.reportProgress)
            self.thread.start()
            self.pushButton_Demarrer.setEnabled(False)
            self.thread.finished.connect(
                lambda: self.pushButton_Demarrer.setEnabled(True)
            )
            self.thread.finished.connect(
                lambda: QMessageBox.information(self,'Info','%s'%'Opération terminée')
            )
    def recognize(self):
                self.recognizer.bd_dir = self.db_directory
                self.recognizer.recognize(self.capo)
            
           
        
    
    def request_passwd(self):   
        input, ok = QInputDialog.getText(self,'Nom:',"%s" %'Entrer le code secret  avant de proceder à cette operation :')
        if ok:
            if input  != self.admin_code:
                QMessageBox.critical(self,'Erreur','%s'%'code erroné')
                return False
            else:
                return True
    #AJOUT DE DOSSIER DANS LA BASE
    def addFolder(self):
        src_folder = self.lineEdit_ouvrir_Dossier.text()
        if src_folder=='':
            self.trainning()
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
                    face_rects = self.face_cascade .detectMultiScale(gray, 1.3, 5)

                    # for all detected faces
                    for (x, y, w, h) in face_rects:
                        roi_img = gray[y:y+h,x:x+w]
                        cv2.imwrite(str(self.path)+"/"+str(self.i)+".jpg",roi_img)
                    self.i+=1
            QMessageBox.information(self,'Info','%s'%'Opération terminée avec succès')                
            self.path=''
            self.i=0
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
    #ENREGISTRER
    def showDialog(self):  
        input, ok = QInputDialog.getText(self,'Nom:', 'Saisir votre nom:')
        if ok:
            if input == '':
                QMessageBox.warning(self,'Attention','%s'%'merci de saisir le nom')
                self.showDialog()
            else:
                self.param=str(input)
                self.param = self.ROOT_DIR+"/"+self.db_directory+"/"+input
                self.timer = QTimer()
                self.timer.timeout.connect(self.detect_face)
                self.on_action_create_user(self.param)
    def getUsername(self):  
        input, ok = QInputDialog.getText(self,'Nom:', '%s'%'Saisir le  nom de la personne sur ces photos:')
        if ok:
            if input == '':
                QMessageBox.warning(self,'Attention','%s'%'merci de saisir le nom')
                self.showDialog()
            else:
                self.param=str(input)
                return self.param
            
    @pyqtSlot()
    def pushButton_source_image_clicked(self):
        (nomImage,filtre)=QFileDialog.getOpenFileName(self,"Selectionner une image",filter="(*.*)")
        if nomImage: 
            if not nomImage.endswith('g'):
                QMessageBox.critical(self,"Error","fichiers image uniquement!")
            else:
                QMessageBox.information(self,"INFO","Fichier à ouvrir:\n\n%s"%nomImage)
                # image = cv2.imread(nomImage)
                self.convert_to_QPixmap(image)
                self.lineEdit_ouvrir_Image.setText(nomImage)
                  
    def check_Base(self):
        
        for dir in self.ROOT_DIR:
            if os.path.exists(self.db_directory):    
                print
                    
            else:
                os.makedirs(self.db_directory,777)
                
    def alert_Dialog(self):
        messageConfirmation = "%s"%str("Nom existe deja, OUI pour ecrasé \n NON pour ajouter ")
        reponse = QMessageBox.question(self,"Confirmation",messageConfirmation,QMessageBox.Yes,QMessageBox.No)
        if reponse == QMessageBox.Yes:
            return True
        else:
            self.showDialog()
       
#creation de dossier pour la personne
    def on_action_create_user(self,dir_name):
        
        if os.path.exists(dir_name):
            rep = self.alert_Dialog()
            if rep:
                if(self.request_passwd()):
                    self.path = dir_name+'/'
                    self.controlTimer_()
                    QMessageBox.information(self,'Info','%s'%'données ecrasées avec succès')
            else:
                    
                self.path = dir_name+'/'
                self.controlTimer_()
            
        else:  
                os.makedirs(dir_name,777)
                self.path = dir_name+'/'
                self.controlTimer_()
        
                
#Si le boutton ajout dossier est cliké
    def pushButton_source_folder_clicked(self):
        (folder) = QFileDialog.getExistingDirectory(self,'choisir le dossier', os.path.curdir) 
        if folder:
            self.lineEdit_ouvrir_Dossier.setText(folder)

#RECONNAITRE
    def reconnaitre(self):
        if self.lineEdit_ouvrir_Image!='':
            self.recognize()
#AUTHENTIFICATION
    def pushButton_authentifier_clicked(self):
        if(self.pushButton_authentifier.text()!='Stop'):
            input, ok = QInputDialog.getText(self,'Saisir votre id','%s'%'Veuillez entrer votre id')
            if ok:
                if input !="":
                        self.id = int(input)
                        self.names = self.fetch()
                        try:
                            self.model = 'dataBase/'+self.names[int(self.id)]+'/model.yml'
                            self.rec  = cv2.face.LBPHFaceRecognizer_create()
                            self.rec.read(self.model)
                        except Exception as e:
                            print(e)
                else:
                    QMessageBox.warning(self,'Attention','%s'%'Id requis!')
        self.param = 'none'
        self.timer_1.timeout.connect(self.recognize)
        self.controlTimer()

    def fetch(self):
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

#trainning
    def trainning(self):
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Train()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()
        self.pushButton_Demarrer.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.pushButton_Demarrer.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: QMessageBox.information(self,'Info','%s'%'Opération terminée')
        )

#ACTION QUITTER
    @pyqtSlot()
    def	on_actionQuitter_triggered(self):
        self.close()
        
    def	closeEvent(self,event):

        messageConfirmation = "Voulez-vous vraiment quittez?"
        reponse = QMessageBox.question(self,"Confirmation",messageConfirmation,QMessageBox.Yes,QMessageBox.No)
        if reponse == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
	
   
#conversion de l'image de type nd-array en pixmap
    def convert_to_QPixmap(self,image):
        w,h,ch = image.shape
        if image.ndim == 1:
            img = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        qimage = QImage(image.data, h, w, 3*h, QImage.Format_RGB888)
        qpixmap = QPixmap.fromImage(qimage)
        self.pix=QPixmap(qpixmap)



# #DETECTION
#     def detect_face(self):
#         # read frame from video capture
#         ret, frame = self.cap.read()
#         frame = cv2.flip(frame,1)
        
#         # resize frame image
#         scaling_factor = 0.8
#         frame_ = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

#         # convert frame to GRAY format
#         gray = cv2.cvtColor(frame_, cv2.COLOR_BGR2GRAY)

#         # detect rect faces
#         face_rects = self.face_cascade.detectMultiScale(gray, 1.3, 5)

#         # for all detected faces
#         for (x, y, w, h) in face_rects:
#             # draw green rect on face
#             roi_img = gray[y:y+h,x:x+w]
#             if self.param!='none':
#                 cv2.imwrite(str(self.path)+"/"+str(self.i)+".jpg",roi_img)
#                 if self.i == self.limit_raw:
#                     self.timer.stop()
#                     self.cap.release()
#                     self.label_1.setStyleSheet("border: 2px solid white;")
#                     self.pushButton_authentifier.setText("Authentifier")
#                     self.pushButton_authentifier.setText("Authentifier")
#                     QMessageBox.information(self,"INFO","Opération%s"%str(' terminé'))
#                     self.i = 0
#                     self.limit_raw = 50
#                     self.label_1.clear()
#                 else:
#                     self.i+=1
#                     print(self.i)
#                     cv2.rectangle(frame_, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                     frame = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
#                     frame = cv2.resize(frame,(210,190),cv2.INTER_AREA)
#                     # get frame infos
#                     height, width, channel = frame.shape
#                     step = channel * width
#                     # create QImage from RGB frame
#                     qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
#                     # show frame in img_label
#                     self.label_1.setStyleSheet("border: 1px solid black;")
#                     self.label_1.setPixmap(QPixmap.fromImage(qImg))
#                     self.label_1.setScaledContents(True)
#                     self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
  
    def controlTimer(self):
        self.recognizer = Recognizer(self.label_1,self.label_id_1,self.label_nom_1,self.label_9,self.model,self.rec)
        if not self.timer_1.isActive():
            self.capo = cv2.VideoCapture(0)
            self.timer_1.start(20)
            self.pushButton_authentifier.setText("Stop")
        else:
            self.path =''
            self.timer_1.stop()
            self.capo.release()
            self.label_1.setScaledContents(True)
            self.label_1.setStyleSheet("border: 2px solid white;")
            self.pushButton_authentifier.setText("Authentifier")
            self.label_1.clear()
            return 0
                
    def controlTimer_(self):
        if not self.timer.isActive():
            self.cap = cv2.VideoCapture(0)# 0 io midika hoe camera numero 0 ro ampesaina (webcam intern)
            #self.cap = cv2.VideoCapture(1) ## 1 io midika hoe camera numero 1 ro ampesaina (webcam externe).
            self.timer.start(20)
            self.pushButton_authentifier.setText("Stop")
        else:
            self.path =''
            self.timer.stop()
            self.cap.release()
            self.label_1.setScaledContents(True)
            self.label_1.setStyleSheet("border: 2px solid white;")
            self.pushButton_authentifier.setText("Authentifier")
            self.label_1.clear()
            return 0