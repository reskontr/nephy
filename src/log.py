import os
import logging
from cStringIO import StringIO

class FileServerLogHandler(logging.Handler):
    def __init__(self, connection, share, path):
        super(FileServerLogHandler, self).__init__()
        self.conn = connection
        self.share = share
        self.path = path

    def emit(self, record):
        message = self.format(record)
        self.conn.append(self.share, self.path, "{}\n".format(message))

def initialize(logConnection, logShare, logPath, username):
    logFile = "{}.log".format(os.path.join(logPath, username))
    handler = FileServerLogHandler(logConnection, logShare, logFile)
    formatter = logging.Formatter("%(asctime)s %(message)s")
    handler.setFormatter(formatter)
    logger = logging.getLogger("remote")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
