from smb.SMBConnection import SMBConnection
from PySide.QtCore import *

class FileServerConnection(object):
    def __init__(self, ip, port, clientName, serverName, username, password):
        conn = SMBConnection(username, password, clientName, serverName)
        conn.connect(ip, port)

