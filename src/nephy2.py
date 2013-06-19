from PySide.QtCore import *
from PySide.QtGui import *
import sys

#import auth
#from loader_test import LoginDialog
from NephyApp import NephyApp

def main():
	app = QApplication(sys.argv)
	connection = None

	#@Slot(str, str)
	#def createConnection(username, password):
	#    connection = auth.FileServerConnection("10.0.255.5", 139, "TestClientName", "wired.local", username, password)

	#loginDialog = LoginDialog()
	#loginDialog.login.connect(createConnection)
	#loginDialog.ui.show()

	main = NephyApp()
	main.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
    main()
