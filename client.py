import socket
from time import sleep

HOST = '192.168.1.103'
PORT = 8002
ADDR = (HOST, PORT)


class Client:
    def __init__(self):
        self.client_socket = socket.socket()
        self.client_socket.connect(ADDR)
        print('Server sent:', self.client_socket.recv(1024).decode())

    def get_socket(self):
        return self.client_socket

    def get_temperature(self):
        self.client_socket.send(b'get_temperature')
        print('Server sent:', self.client_socket.recv(1024).decode())


if __name__ == '__main__':
    client = Client()
    try:
        for _ in range(10):
            client.get_temperature()
            sleep(1)
    except KeyboardInterrupt:
        client.client_socket.shutdown(socket.SHUT_RDWR)
        print("Shutdown")
        client.client_socket.close()
        print("Socket closed")
