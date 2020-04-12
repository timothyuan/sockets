import unittest
import socket
import subprocess
from mock import Mock, patch
from server_python_tcp import receiveCommand, sendFile

class TestServerTCP(unittest.TestCase):

    @patch('socket.socket')
    def test_receiveCommand(self, mock_socket):
        mock_address = ('ip', 3000)
        # valid command, saves output of ls to a file
        mock_socket.recv.return_value = b'ls > output.txt'
        self.assertEqual(receiveCommand(mock_socket, mock_address), 'ls > output.txt', 'Testing valid command')
        # invalid command, returns error
        mock_socket.recv.return_value = b'asdf'
        self.assertEqual(receiveCommand(mock_socket, mock_address), 'error', 'Testing invalid command')
        subprocess.check_output('rm output.txt', shell=True)

    @patch('socket.socket')
    def test_sendFile(self, mock_socket):
        f = open('output.txt', 'w')
        f.write('testtest')
        f.close()
        # successful read and transmission of output.txt
        self.assertTrue(sendFile('output.txt', mock_socket))
        # file transmission failed, throw exception
        mock_socket.send.side_effect = Exception
        self.assertFalse(sendFile('output.txt', mock_socket))
        subprocess.check_output('rm output.txt', shell=True)


if __name__ == '__main__':
    unittest.main()
