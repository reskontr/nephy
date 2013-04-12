from PySide.QtCore import *
from PySide.QtGui import *
import sys

import auth
import database
from LoginDialog import LoginDialog

def main():
    app = QApplication(sys.argv)

    #dbConn = database.DatabaseConnection("asd")

    connection = None

    @Slot(str, str)
    def createConnection(username, password):
        """Creates connection to windows domain server"""
        connection = auth.FileServerConnection("192.168.56.1", 139, "macpro", "paju", username, password)
    
    loginDialog = LoginDialog()
    loginDialog.login.connect(createConnection)
    loginDialog.ui.exec_()

if __name__ == "__main__":
    main()
