import socket
import subprocess

def receiveCommand(con, addr):
    # receive command from client
    data = con.recv(1024)
    cmd = data.decode('utf-8')

    try:
        # attempts to call command on shell, sends error message if exception
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        con.send('error'.encode('utf-8'))
        con.shutdown((socket.SHUT_RDWR))
        return 'error'
    return cmd

def sendFile(file, con):
    # read output from file
    f = open(file, 'r')
    data = f.read(1024)

    # send output back to client
    while(data):
        try:
            con.send(data.encode('utf-8'))
            data = f.read(1024)
        except Exception:
            f.close()
            return False
    f.close()
    return True

def main():
    # create a tcp socket
    PORT = 65432
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', PORT))
    s.listen()

    while True:
        # accepts connections from clients
        con, addr = s.accept()
        cmd = receiveCommand(con, addr)

        # checks if valid command
        if cmd == 'error':
            continue

        # sends output back to client
        file = cmd.split(' > ')[1]
        if sendFile(file, con):
            print('Successful file transmission.')
        else:
            print('File transmission failed.')

        con.shutdown(socket.SHUT_RDWR)
    s.close()

if __name__ == '__main__':
    main()
