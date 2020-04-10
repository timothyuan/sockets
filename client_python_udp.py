import socket
import sys
import time

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
    # Check if connection is successful
    try:
        sock.sendto('test'.encode('utf-8'), address)
        sock.settimeout(1)
        test, address = sock.recvfrom(1024)
        if test.decode('utf-8') != 'test':
            raise Exception
        return True
    except Exception:
        print("Could not connect to server")
        return False

def executeCommand(cmd, sock, address):
    for _ in range(0,3):
        try:
            sock.sendto(str(len(cmd)).encode('utf-8'), address)
            sock.sendto(cmd.encode('utf-8'), address)
            sock.settimeout(1)
            # one second deadline to send an ACK
            deadline = time.time()+1
            response, addr = sock.recvfrom(1024)
            while(response.decode('utf-8')!='ACK'):
                sock.settimeout(deadline - time.time())
                response, addr = sock.recvfrom(1024)
            sock.settimeout(None)
            return True
        except socket.timeout:
            continue
    # completed three iterations without an ACK
    print("Failed to send command. Terminating")
    sock.settimeout(None)
    return False

def getResponse(sock, file):
    total, addr = sock.recvfrom(1024)

    if total.decode('utf-8') == 'error':
        print('Did not receive response.')
        return False

    total = int(total.decode('utf-8'))
    length, addr = sock.recvfrom(1024)
    text, addr = sock.recvfrom(1024)

    f = open(file, 'w')
    f.write(text.decode('utf-8'))
    current = int(length.decode('utf-8'))

    sock.sendto('ACK'.encode('utf-8'), addr)

    while(current!=total):
        try:
            length, addr = sock.recvfrom(1024)
            sock.settimeout(0.5)
            deadline = time.time()+0.5
            text, addr = sock.recvfrom(1024)
            while(int(length.decode('utf-8'))!=len(text.decode('utf-8'))):
                sock.settimeout(deadline - time.time())
                text, addr = sock.recvfrom(1024)
            sock.sendto('ACK'.encode('utf-8'), addr)
            sock.settimeout(None)
        except socket.timeout:
            print('Did not receive response.')
            sock.settimeout(None)
            return False
        f.write(text.decode('utf-8'))
        current += int(length.decode('utf-8'))
    f.close()
    sock.close()
    print('File ', file, ' saved.')
    return True


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

    addr = (ip, port)
    file = cmd.split(' > ')[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    if not checkConnection(s, addr):
        sys.exit()

    if not executeCommand(cmd, s, addr):
        sys.exit()

    if not getResponse(s, file):
        sys.exit()

if __name__ == '__main__':
    main()
