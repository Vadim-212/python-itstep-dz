import socket
from server import HOSTNAME, PORT


if __name__ == '__main__':

    with socket.socket() as sock:
        sock.connect((HOSTNAME, PORT))

        sended_data = input('enter: ')
        sended_data += '\n'
        sock.sendall(sended_data.encode())

        data = sock.recv(4096)

        print(f'received: {data.decode()}')
        