import logging
import ntpath
import smb
from cStringIO import StringIO
from smb.SMBConnection import SMBConnection
from PySide.QtCore import *

class FileServerException(Exception):
    pass

class FileServerConnection(object):
    """Connection to a Samba file server"""

    def __init__(self, ip, port, clientName, serverName, username, password):
        self.conn = SMBConnection(username, password, clientName, serverName)
        self.conn.connect(ip, port)

        try:
            shares = self.conn.listShares()
            sharesStr = ", ".join("{0.name} ({0.comments})".format(s) for s in shares)
            logging.info("Visible shares on {} ({}:{}): {}".format(serverName,
                                                                   ip,
                                                                   port,
                                                                   sharesStr))
        except smb.base.NotReadyError as e:
            raise FileServerException(e)

    def append(self, share, path, data):
        try:
            # Get the existing contents of the file.
            file = StringIO()
            try:
                self.conn.retrieveFile(share, path, file)
            except smb.smb_structs.OperationFailure as e:
                # The file might not exist yet.
                if not e.message.endswith("Unable to open file"):
                    # Something else went wrong.
                    raise

            # Append the data.
            file.write(data)
            file.seek(0)

            # NOTE: Apparently storeFile fails if the target file exists. It
            # must be deleted first.
            # TODO: Rename the old file instead of deleting until the store
            # operation is completed succesfully?
            try:
                self.conn.deleteFiles(share, path)
            except smb.smb_structs.OperationFailure as e:
                # The file might not exist yet.
                if not e.message.endswith("Delete failed"):
                    # Something else went wrong.
                    raise
            self.conn.storeFile(share, path, file)
        except smb.smb_structs.OperationFailure as e:
            raise FileServerException(e.message)
