import socket
import json

from network_module.utils import send_message, receive_message


class NetworkModule:
    def __init__(self):
        self.clientSocket = socket.socket()

        self.clientPort = None

    def startClientConnection(self, port):
        self.clientPort = port
        self.clientSocket.connect(("127.0.0.1", port))

        print("Connected to the client simulation app.")

    def getSimulationData(self):
        request = {
            "action": "getSimulationData"
        }
        send_message(self.clientPort, request)
        response = receive_message(self.clientSocket)

        return response

    def closeClientConnection(self):
        if self.clientSocket:
            self.clientSocket.close()
        print(f"Socket with port {self.clientPort} closed")