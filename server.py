import socket
from threading import Thread
import utils

HOST = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
        [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
print(HOST)
PORT = 8002


def respond_to_client(client_socket, address):
    try:
        client_socket.send(str.encode("Accepted connection from {}".format(address)))
        while True:
            message = client_socket.recv(1024).decode()

            print('Client sent:', message)
            if message in utils.orders:
                response = str.encode(utils.orders[message]())
                client_socket.send(response)
            else:
                client_socket.send(b"Unrecognized command")
    except BrokenPipeError:
        "Client disconnected"


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    while True:
        client_socket, address = server_socket.accept()
        print("Received connection from ", address)

        thread = Thread(target=respond_to_client, args=(client_socket, address))
        thread.start()
