import unittest
from mock import Mock
from client_python_udp import validatePort, checkConnection

class TestClientUDP(unittest.TestCase):

    def test_validatePort(self):
        self.assertFalse(validatePort('-1'))
        self.assertFalse(validatePort('test'))
        self.assertTrue(validatePort('65432'))

    def test_checkConnection(self):
        mock_socket = Mock()
        mock_address = ('test',3000)
        self.assertFalse(checkConnection(mock_socket, mock_address))
        mock_socket.recvfrom.return_value = [b'test', mock_address]
        self.assertTrue(checkConnection(mock_socket, mock_address))

if __name__ == '__main__':
    unittest.main()
