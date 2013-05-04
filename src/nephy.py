from PySide.QtCore import *
from PySide.QtGui import *
from ConfigParser import SafeConfigParser
import sys

import auth
from LoginDialog import LoginDialog

def main():
    config = SafeConfigParser()
    config.read("config.ini")

    dbServerName = config.get("db", "server_name")
    dbServerAddress = config.get("db", "server_address")
    dbServerPort = config.getint("db", "server_port")

    app = QApplication(sys.argv)

    connection = None

    @Slot(str, str)
    def createConnection(username, password):
        """Create a connection to the database file server."""
        connection = auth.FileServerConnection(dbServerAddress, dbServerPort, "localhost", dbServerName, username, password)

    loginDialog = LoginDialog()
    loginDialog.login.connect(createConnection)
    loginDialog.ui.exec_()

if __name__ == "__main__":
    main()
