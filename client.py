import socket
from time import sleep

import subprocess

import re

PORT = 8002


class Client:
    def __init__(self):
        self.client_socket = socket.socket()
        self.connect()
        print('Server sent:', self.client_socket.recv(1024).decode())

    def connect(self, ADDR=None):
        if ADDR is None:
            ADDR = (self.get_rpi_ip(), PORT)
        self.client_socket.connect(ADDR)

    def get_temperature(self):
        self.client_socket.send(b'get_temperature')
        print('Server sent:', self.client_socket.recv(1024).decode())

    @staticmethod
    def get_rpi_ip():
        with open("rpi_mac.txt") as mac_file:
            MAC = mac_file.readline().rstrip()
        stream = subprocess.Popen("arp -an", shell=True, stdout=subprocess.PIPE).stdout.read().decode()
        pattern = re.compile(r'\((\d+\.\d+\.\d+\.\d+)\) at ' + MAC)
        return re.search(pattern, stream).groups()[0]


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
