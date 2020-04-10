import socket
import subprocess

PORT = 65432

# create a tcp socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', PORT))
s.listen()

while True:
    # accepts connections
    con, addr = s.accept()

    # receive command from client
    data = con.recv(1024)
    cmd = data.decode('utf-8')

    try:
        # attempts to call command on shell, sends error message if exception
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        con.send('error'.encode('utf-8'))
        con.shutdown((socket.SHUT_RDWR))
        continue

    # read output from file
    file = cmd.split(' > ')[1]
    f = open(file, 'r')
    data = f.read(1024)

    # send output back to client
    while(data):
        con.send(data.encode('utf-8'))
        data = f.read(1024)

    con.shutdown(socket.SHUT_RDWR)
s.close()
