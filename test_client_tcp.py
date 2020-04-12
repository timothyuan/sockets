import unittest
import socket
import subprocess
from mock import Mock, patch
from client_python_tcp import validatePort, checkConnection, getResponse

class TestClientTCP(unittest.TestCase):

    def test_validatePort(self):
        # valid port number
        self.assertTrue(validatePort('65432'))
        # invalid port number
        self.assertFalse(validatePort('-1'))
        self.assertFalse(validatePort('test'))

    @patch('socket.socket')
    def test_checkConnection(self, mock_socket):
        mock_address = ('ip', 3000)
        # mock correct response
        self.assertTrue(checkConnection(mock_socket, mock_address))
        # could not connect to server
        mock_socket.connect.side_effect = Exception
        self.assertFalse(checkConnection(mock_socket, mock_address))

    @patch('socket.socket')
    def test_getResponse(self, mock_socket):
        mock_address = ('ip', 3000)
        # could not connect to server
        mock_socket.recv.return_value = b'error'
        self.assertEqual(getResponse(mock_socket), 'error', 'Testing error response from server')
        # mock correct response, sends empty string for end of file
        mock_socket.recv.side_effect = [b'testtest', b'']
        self.assertTrue(getResponse(mock_socket))
        subprocess.check_output('rm client_output.txt', shell=True)


if __name__ == '__main__':
    unittest.main()
