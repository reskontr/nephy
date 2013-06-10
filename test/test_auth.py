import auth

import mock


@mock.patch("auth.SMBConnection")
def testConnectionInitialized(mockSMBConnection):
    ip = "10.0.0.2"
    port = 139
    clientName = "Client"
    serverName = "Server"
    auth.FileServerConnection(ip, port, clientName, serverName, "user", "password")
    mockSMBConnection.called_once_with("user", "password", clientName, serverName)

@mock.patch.object(auth.SMBConnection, "connect")
@mock.patch.object(auth.SMBConnection, "listShares")
def testConnectionConnects(mockConnect, mockListShares):
    ip = "10.0.0.2"
    port = 139
    auth.FileServerConnection(ip, port, "client", "server", "user", "password")
    mockConnect.called_once_with(ip, port)
