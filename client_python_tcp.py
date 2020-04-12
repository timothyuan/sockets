import socket
import sys

def validatePort(port):
    try:
        port = int(port) # raise exception if not int
        if port > 65535 or port < 0:
            raise Exception # raise exception if invalid port
        return True
    except Exception:
        print('Invalid port number.')
        return False

def checkConnection(sock, address):
    # try to connect to server, timeout after 1 sec
    sock.settimeout(1)
    try:
        sock.connect(address)
        sock.settimeout(None)
        return True
    except Exception:
        print('Could not connect to server.')
        sock.settimeout(None)
        return False

def getResponse(sock):
    data = sock.recv(1024)
    # check for error message
    if data.decode('utf-8') == 'error':
        print('Did not receive response.')
        return 'error'

    # write response from server into client_output.txt
    f = open('client_output.txt', 'w')
    while(data):
        f.write(data.decode('utf-8'))
        data = sock.recv(1024)
    f.close()
    print('File client_output.txt saved.')
    return 'File client_output.txt saved'

def main():
    # take ip address input
    ip = input('Enter server name or IP address: ')

    while True:
        # take port input
        port = input('Enter port: ')
        if validatePort(port):
            port = int(port)
            break

    while True:
        # take command input
        cmd = input('Enter command: ')
        if ' > ' not in cmd:
            # prompt again if command does not contain >
            print('Command must contain >')
            continue
        break

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # checks connection with inputted credentials
    if not checkConnection(s, (ip, port)):
        sys.exit()

    # send command to server
    s.sendall(cmd.encode('utf-8'))

    # receive data and write to local file
    data = getResponse(s)
    if data == 'error':
        sys.exit()

    s.close()

if __name__ == '__main__':
    main()
