import socket
import sys

# take ip address input
ip = input('Enter server name or IP address: ')

while True:
    # take port input
    port = input('Enter port: ')
    try:
        port = int(port) # raise exception if not int
        if port > 65535 or port < 0:
            raise Exception # raise exception if invalid port
        break
    except Exception:
        print('Invalid port number.')

while True:
    # take command input
    cmd = input('Enter command: ')
    if ' > ' not in cmd:
        # prompt again if command does not contain >
        print('Command must contain >')
        continue
    break

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try to connect to server
try:
    s.connect((ip, port))
except Exception:
    print('Could not connect to server.')
    sys.exit()

# send command to server and receive data
s.sendall(cmd.encode('utf-8'))
data = s.recv(1024)

# check for error message
if data.decode('utf-8') == 'error':
    print('Did not receive response.')
    sys.exit()

# write to local file
file = cmd.split(' > ')[1]
f = open(file, 'w')
while(data):
    f.write(data.decode('utf-8'))
    data = s.recv(1024)

f.close()
print('File ', file, ' saved.')
s.close()
