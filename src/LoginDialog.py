from PySide.QtUiTools import *
from PySide.QtCore import *
from PySide.QtGui import *
import sys

import auth

class LoginDialog(QWidget):
    login = Signal(str, str)

    def __init__(self):
        super(LoginDialog, self).__init__()
        loader = QUiLoader()
        file = QFile("ui/login.ui")
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, self)
        file.close()
        QMetaObject.connectSlotsByName(self)

    @Slot()
    def on_buttonBox_accepted(self):
        username = self.ui.findChild(QLineEdit, 'lineEditUsername')
        password = self.ui.findChild(QLineEdit, 'lineEditPassword')
        self.login.emit(username.text(), password.text())
