from PySide.QtCore import *
from PySide.QtGui import *
import sys

import auth
from LoginDialog import LoginDialog

def main():
    app = QApplication(sys.argv)
    connection = None

    @Slot(str, str)
    def createConnection(username, password):
        connection = auth.FileServerConnection("10.0.255.5", 139, "TestClientName", "wired.local", username, password)
    
    loginDialog = LoginDialog()
    loginDialog.login.connect(createConnection)
    loginDialog.ui.exec_()

if __name__ == "__main__":
    main()
