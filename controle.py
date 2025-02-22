import sys
from PyQt5.QtWidgets import  QApplication
from controle_acces import Main_control_access 
app = QApplication(sys.argv)
mainWindow = Main_control_access()
mainWindow.show()
rc = app.exec_()
sys.exit(rc)  