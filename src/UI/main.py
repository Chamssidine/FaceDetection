from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QGraphicsView, QInputDialog, QMessageBox, QMainWindow, QSizePolicy
from PyQt5.QtCore	import 	QThread, pyqtSlot
from Ui_new_update import Ui_MainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from UI.uiManager import UIManager  
from RetinaFace.dataBaseManager import DataBaseManager
import os


class Main(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)
        self.pushButton_ouvrir_Image.clicked.connect(self.pushButton_source_image_clicked)
        self.pushButton_Enregistrer.clicked.connect(self.showDialog)
        self.pushButton_Demarrer.clicked.connect(self.recognize)
        self.pushButton_authentifier.clicked.connect(self.pushButton_authentifier_clicked)
        self.pushButton_ouvrir_Dossier.clicked.connect(self.select_source_folder)
        self.pushButton_2.clicked.connect(self.addFolder)
        self.pix = QPixmap
        self.scene = QtWidgets.QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.uiManager = UIManager()
        self.dataBaseManager = DataBaseManager("database")
    
    @pyqtSlot()
    def pushButton_source_image_clicked(self):
        print("")
        
    def select_source_folder(self):
        (folder) = QFileDialog.getExistingDirectory(self,'choisir le dossier', os.path.curdir) 
        if folder:
            self.lineEdit_ouvrir_Dossier.setText(folder)
    
    def pushButton_authentifier_clicked(self):
        if(self.pushButton_authentifier.text()!='Stop'):
            input, ok = QInputDialog.getText(self,'Saisir votre id','%s'%'Veuillez entrer votre id')
            if ok:
                if input !="":
                        self.id = int(input)
                        try:
                            self.model = 'RetinaFace/dataBase/'+self.names[int(self.id)]+'/model.yml'
                            self.rec.read(self.model)
                        except Exception as e:
                            print(e)
                else:
                    QMessageBox.warning(self,'Attention','%s'%'Id requis!')
        self.param = 'none'
        self.timer_1.timeout.connect(self.recognize)
        self.controlTimer()
    
    def recognize(self):
        print("recognition")
    @pyqtSlot()
    def	on_actionQuitter_triggered(self):
        self.close()
    
    def addFolder(self):
        src_folder = self.lineEdit_ouvrir_Dossier.text()
        if src_folder=='':
            print("empty folder")
        else:
            (success,name) = self.getUsername()
            if(success):
                name =  str(self.ROOT_DIR)+"/"+str(self.db_directory)+"/"+str(name)
                self.uiManager.show_info_dialog(self,'Info','%s'%'Opération terminée avec succès')    
            else:
                print("could not get the name")            
    def getUsername(self):  
        return self.uiManager.input_name_dialog()
            
            
            
    def convert_to_QPixmap(self,image):
        w,h,ch = image.shape
        if image.ndim == 1:
            img = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        qimage = QImage(image.data, h, w, 3*h, QImage.Format_RGB888)
        qpixmap = QPixmap.fromImage(qimage)
        self.pix=QPixmap(qpixmap)
        
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