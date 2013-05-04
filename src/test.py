import mock
import auth

@mock.patch("auth.SMBConnection")
def test_connection_init(mock_SMBConnection):
    """Tests initialization of SMBConnection class"""
    ip = "10.0.0.2"
    port = 139
    clientName = "Client"
    serverName = "Server"
    auth.FileServerConnection(ip, port, clientName, serverName, "user", "password")
    mock_SMBConnection.called_once_with("user", "password", clientName, serverName)

@mock.patch.object(auth.SMBConnection, "connect")
def test_connects(mock_connect):
    """Tests the connect method of SMBConnection class"""
    ip = "10.0.0.2"
    port = 139
    auth.FileServerConnection(ip, port, "client", "server", "user", "password")
    mock_connect.called_once_with(ip, port)
