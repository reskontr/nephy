from smb.SMBConnection import SMBConnection
from PySide.QtCore import *

class FileServerConnection(object):
    """Connection to a Samba file server"""

    def __init__(self, ip, port, clientName, serverName, username, password):
        conn = SMBConnection(username, password, clientName, serverName)
        ok = conn.connect(ip, port)
        if(ok):
            print("CONNECTED")
            shares = conn.listShares()
            for share in shares:
                print(share.name)
