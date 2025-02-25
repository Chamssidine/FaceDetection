import sys
from PyQt5.QtWidgets import  QApplication
from UI.main import Main  
app = QApplication(sys.argv)
mainWindow = Main()
mainWindow.show()
rc = app.exec_()
sys.exit(rc)  