
from PyQt5.QtWidgets import  QInputDialog, QMessageBox


class UIManager():
    def __init__(self) -> None:
        pass
    
    def show_warning_dialog(self, message ):
        QMessageBox.warning(self,message)
    
    def show_info_dialog(self,message):
        QMessageBox.information(self,message)   
    def input_name_dialog(self):  
        input, ok = QInputDialog.getText(self,'Nom:', 'Saisir votre nom:')
        if ok:
            if input == '':
                self.show_dialog("'Attention','%s'%'merci de saisir le nom'")
                self.input_name_dialog()
            else:
                return str(True,str(input))
        else:
            return str(False,None)