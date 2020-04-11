import unittest
import socket
import subprocess
from mock import Mock, patch
from client_python_udp import validatePort, checkConnection, executeCommand, getResponse

class TestClientUDP(unittest.TestCase):

    def test_validatePort(self):
        # Valid port number
        self.assertTrue(validatePort('65432'))
        # Invalid port number
        self.assertFalse(validatePort('-1'))
        self.assertFalse(validatePort('test'))

    @patch('socket.socket')
    def test_checkConnection(self, mock_socket):
        mock_address = ('test', 3000)
        # Could not connect to server
        self.assertFalse(checkConnection(mock_socket, mock_address))
        # mock correct response
        mock_socket.recvfrom.return_value = (b'test', mock_address)
        self.assertTrue(checkConnection(mock_socket, mock_address))
        # Could not connect to server
        mock_socket.recvfrom.return_value = (b'incorrect', mock_address)
        self.assertFalse(checkConnection(mock_socket, mock_address))

    @patch('socket.socket')
    def test_executeCommand(self, mock_socket):
        mock_cmd = 'cmd'
        mock_address = ('ip', 3000)
        # mock correct response
        mock_socket.recvfrom.return_value = (b'ACK', mock_address)
        self.assertTrue(executeCommand(mock_cmd, mock_socket, mock_address))
        # Failed to send command. Terminating
        mock_socket.recvfrom.side_effect = socket.timeout
        self.assertFalse(executeCommand(mock_cmd, mock_socket, mock_address))

    @patch('socket.socket')
    def test_getResponse(self, mock_socket):
        # Did not receive response, File saved
        mock_address = ('ip', 3000)
        # Did not receive total length
        mock_socket.recvfrom.return_value = (b'error', mock_address)
        self.assertFalse(getResponse(mock_socket))
        # True case, File saved
        mock_socket.recvfrom.side_effect = [(b'8', mock_address), (b'4', mock_address), (b'test', mock_address), (b'4', mock_address), (b'test', mock_address)]
        self.assertTrue(getResponse(mock_socket))
        # Timeout case, receives a valid total length but subsequent packets don't add to total
        mock_socket.recvfrom.side_effect = [(b'8', mock_address), (b'4', mock_address), (b'test', mock_address), socket.timeout]
        self.assertFalse(getResponse(mock_socket))
        # Remove client_output.text
        subprocess.check_output('rm client_output.txt', shell=True)

if __name__ == '__main__':
    unittest.main()
