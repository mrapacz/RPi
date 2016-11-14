import socket
from time import sleep

from client_utils import get_rpi_ip

PORT = 8002


class Client:
    def __init__(self):
        self.client_socket = socket.socket()
        self.connect()
        print('Server sent:', self.client_socket.recv(1024).decode())

    def connect(self, ADDR=None):
        if ADDR is None:
            ADDR = (get_rpi_ip(), PORT)
        self.client_socket.connect(ADDR)

    def get_temperature(self):
        self.client_socket.send(b'get_temperature')
        return self.client_socket.recv(1024).decode()


if __name__ == '__main__':
    client = Client()
    try:
        temperature = client.get_temperature()
        sleep(1)

        # -*- coding: utf-8 -*-
        print("Current temperature is " + str(float(temperature) / 1000) + "°C")

    except KeyboardInterrupt:
        client.client_socket.shutdown(socket.SHUT_RDWR)
        print("Shutdown")
        client.client_socket.close()
        print("Socket closed")
