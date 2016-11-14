import socket
from threading import Thread
import server_utils

PORT = 8002


class ServerSocket(socket.socket):
    def __init__(self):
        super(ServerSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.setup_socket()

    def setup_socket(self):
        HOST = server_utils.get_host_ip()
        self.bind((HOST, PORT))
        self.listen(5)

    def listen_to_clients(self):
        while True:
            client_socket, address = server_socket.accept()
            print("Received connection from ", address)

            thread = Thread(target=self.respond_to_client, args=(client_socket, address))
            thread.start()

    @staticmethod
    def respond_to_client(client_socket, address):
        try:
            client_socket.send(str.encode("Accepted connection from {}".format(address)))
            while True:
                message = client_socket.recv(1024).decode()
                if len(message) == 0:
                    break
                print('Client sent:', message)
                if message in server_utils.orders:
                    response = server_utils.orders[message]()
                else:
                    response = "Unrecognized command"
                encoded_response = str.encode(response)
                client_socket.send(encoded_response)

        except BrokenPipeError:
            "Client disconnected"


if __name__ == '__main__':
    server_socket = ServerSocket()
    server_socket.listen_to_clients()
