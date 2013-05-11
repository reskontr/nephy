from PySide.QtCore import *
from PySide.QtGui import *
from ConfigParser import SafeConfigParser
import sys
import logging

import auth
import log
from LoginDialog import LoginDialog

def main():
    # Read the configuration.

    # TODO: Add a debug command line option.
    logging.basicConfig(level=logging.DEBUG)

    config = SafeConfigParser()
    config.read("config.ini")

    logServerName = config.get("log", "server_name")
    logServerAddress = config.get("log", "server_address")
    logServerPort = config.getint("log", "server_port")
    logShare = config.get("log", "share")
    logPath = config.get("log", "path")

    dbServerName = config.get("db", "server_name")
    dbServerAddress = config.get("db", "server_address")
    dbServerPort = config.getint("db", "server_port")

    app = QApplication(sys.argv)

    @Slot(str, str)
    def createConnection(username, password):
        """Create connections to file servers using the given credentials."""

        logConnection = auth.FileServerConnection(logServerAddress,
                                                  logServerPort,
                                                  "localhost",
                                                  logServerName,
                                                  username,
                                                  password)
        dbConnection = auth.FileServerConnection(dbServerAddress,
                                                 dbServerPort,
                                                 "localhost",
                                                 dbServerName,
                                                 username,
                                                 password)

        log.initialize(logConnection, logShare, logPath, username)

        remoteLogger = logging.getLogger("remote")
        remoteLogger.info("Logged in")

    loginDialog = LoginDialog()
    loginDialog.login.connect(createConnection)
    loginDialog.ui.exec_()

if __name__ == "__main__":
    main()
