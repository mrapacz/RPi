import socket
from threading import Thread

import subprocess
from time import sleep

import utils

PORT = 8002
MAX_FAIL_COUNT = 60


def respond_to_client(client_socket, address):
    try:
        client_socket.send(str.encode("Accepted connection from {}".format(address)))
        while True:
            message = client_socket.recv(1024).decode()
            if len(message) == 0:
                break
            print('Client sent:', message)
            if message in utils.orders:
                response = str.encode(utils.orders[message]())
                client_socket.send(response)
            else:
                client_socket.send(b"Unrecognized command")
    except BrokenPipeError:
        "Client disconnected"


def get_host_ip():
    ip = None
    fail_count = 0
    while ip is None and fail_count < MAX_FAIL_COUNT:
        ip = subprocess.Popen("hostname -I", shell=True, stdout=subprocess.PIPE).stdout.read().decode().rstrip()
        fail_count += 1
        sleep(1)
    if ip is None:
        raise ConnectionError("No internet connection")
    return ip


if __name__ == '__main__':
    HOST = get_host_ip()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    while True:
        client_socket, address = server_socket.accept()
        print("Received connection from ", address)

        thread = Thread(target=respond_to_client, args=(client_socket, address))
        thread.start()
