from PySide.QtUiTools import *
from PySide.QtCore import *
from PySide.QtGui import *
import sys

import auth

class LoginDialog(QWidget):
    """Dialog with username and password fields"""

    # Signal for emitting the username and password when logging in
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
        """Slot for pressing the login button in the dialog"""

        username = self.ui.findChild(QLineEdit, 'lineEditUsername')
        password = self.ui.findChild(QLineEdit, 'lineEditPassword')
        self.login.emit(username.text(), password.text())
