import sys

from PyQt5.QtWidgets import QApplication, QInputDialog, QLineEdit, QMessageBox, QPushButton, QWidget
class Dialog(QWidget):

    def __init__(self):
        super().__init__()

        self.terminated()
    def terminated(self):

        ret = QMessageBox.information(self,'Info','%s'%'Opération terminée',QMessageBox.Ok)
        
        if ret:
            sys.exit(self)
def main():
    app = QApplication(sys.argv)
    ex = Dialog()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()