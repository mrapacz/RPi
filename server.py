import socket
from threading import Thread
import server_utils

PORT = 8002


def respond_to_client(client_socket, address):
    try:
        client_socket.send(str.encode("Accepted connection from {}".format(address)))
        while True:
            message = client_socket.recv(1024).decode()
            if len(message) == 0:
                break
            print('Client sent:', message)
            if message in server_utils.orders:
                response = str.encode(server_utils.orders[message]())
                client_socket.send(response)
            else:
                client_socket.send(b"Unrecognized command")
    except BrokenPipeError:
        "Client disconnected"


if __name__ == '__main__':
    HOST = server_utils.get_host_ip()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    while True:
        client_socket, address = server_socket.accept()
        print("Received connection from ", address)

        thread = Thread(target=respond_to_client, args=(client_socket, address))
        thread.start()
