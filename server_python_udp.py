import socket
import subprocess
import time
import sys
import os

def receiveCommand(sock):
    # receive length of command
    length, addr = sock.recvfrom(1024)
    try:
        sock.settimeout(0.5)
        deadline = time.time() + 0.5
        # receive a command with valid length until 0.5 s timeout
        cmd, addr = sock.recvfrom(1024)
        while (int(length.decode('utf-8'))!=len(cmd.decode('utf-8'))):
            sock.settimeout(deadline-time.time())
            cmd, addr = sock.recvfrom(1024)
        sock.sendto('ACK'.encode('utf-8'), addr)
        sock.settimeout(None)
        return cmd.decode('utf-8')
    except Exception:
        print('Failed to receive instructions from the client.')
        sock.settimeout(None)
        return 'error'

def sendFile(sock, address, file):
    # read from file
    f = open(file, 'r')
    text = f.read(1024)

    # send size of file to client
    sock.sendto(str(os.path.getsize(file)).encode('utf-8'), address)

    # while text exists in file
    while(text):
        i = 0
        # attempt to send each line 3 times
        while(i < 3):
            try:
                sock.sendto(str(len(text)).encode('utf-8'), address)
                sock.sendto(text.encode('utf-8'), address)
                # 0.5 seconds for client to ACK
                sock.settimeout(0.5)
                deadline = time.time() + 0.5
                response, address = sock.recvfrom(1024)
                while(response.decode('utf-8') != 'ACK'):
                    sock.settimeout(deadline - time.time())
                    response, address = sock.recvfrom(1024)
                sock.settimeout(None)
                break
            except Exception:
                sock.settimeout(None)
            i+=1
        if(i==3):
            f.close()
            print('File transmission failed.')
            return False
        text = f.read(1024)
    f.close()
    print('Successful file transmission')
    return True

def main():
    PORT = int(sys.argv[1])

    # create a udp socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # attempt to bind to port
    try:
        s.bind(('', PORT))
    except Exception:
        print('The port is already in use')
        sys.exit()

    while True:
        # test message to check connection
        test, addr = s.recvfrom(1024)
        if test.decode('utf-8') == 'test':
            s.sendto('test'.encode('utf-8'), addr)

        cmd = receiveCommand(s)
        if cmd == 'error':
            continue

        print(cmd)
        file = cmd.split(' > ')[1]

        # execute received command
        try:
            subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError:
            s.sendto('error'.encode('utf-8'), addr)
            continue


        if not sendFile(s, addr, file):
            continue

if __name__ == '__main__':
    main()
