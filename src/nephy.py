from PySide.QtUiTools import *
from PySide.QtCore import *
from PySide.QtGui import *
import sys

class LoginDialog(QWidget):
    def __init__(self):
        super(LoginDialog, self).__init__()
        loader = QUiLoader()
        file = QFile("../ui/login.ui")
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, self)
        file.close()
        QMetaObject.connectSlotsByName(self)

    @Slot()
    def on_buttonBox_accepted(self):
        username = self.ui.findChild(QLineEdit, 'lineEditUsername')
        password = self.ui.findChild(QLineEdit, 'lineEditPassword')
        print(username.text() + " - " + password.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loginDialog = LoginDialog()
    loginDialog.ui.show()
    app.exec_()
    sys.exit()