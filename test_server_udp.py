import unittest
import socket
from mock import Mock, patch
from server_python_udp import receiveCommand, sendFile

class TestServerUDP(unittest.TestCase):

        @patch('socket.socket')
        def test_receiveCommand(self, mock_socket):
            # Correct response
            validcmd = b'test'
            mock_address = ('ip', 3000)
            mock_socket.recvfrom.side_effect = [(b'4', mock_address), (validcmd, mock_address)]
            self.assertEqual(validcmd.decode('utf-8'), receiveCommand(mock_socket), 'Testing valid command')
            # Failed to receive instructions from the client
            mock_socket.recvfrom.side_effect = [(b'4', mock_address), socket.timeout]
            self.assertEqual('error', receiveCommand(mock_socket), 'Testing invalid command')
            # Total command length doesnt match smaller packets added up
            mock_socket.recvfrom.side_effect = [(b'8', mock_address), (validcmd, mock_address), socket.timeout]
            self.assertEqual('error', receiveCommand(mock_socket), 'Testing invalid command')

        @patch('socket.socket')
        def test_sendFile(self, mock_socket):
            f = open('output.txt', 'w')
            f.write('testtest')
            f.close()
            mock_address = ('ip', 3000)
            # Successful file transmission
            mock_socket.recvfrom.return_value = (b'ACK', mock_address)
            self.assertTrue(sendFile(mock_socket, mock_address, 'output.txt'))

            # File transmission failed, timeout 3 times while waiting for ACK
            mock_socket.recvfrom.side_effect = socket.timeout
            self.assertFalse(sendFile(mock_socket, mock_address, 'output.txt'))



if __name__ == '__main__':
    unittest.main()
