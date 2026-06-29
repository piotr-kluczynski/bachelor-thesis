import socket
import json

from network_module.utils import send_message, receive_message


class NetworkModule:
    def __init__(self):
        self.clientSocket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.clientPort = None

    def startClientConnection(self, port):
        self.clientPort = port

        try:
            self.clientSocket.connect(("127.0.0.1", port))
            print("Connected to simulation server")

            return True
        except socket.error as e:
            print(f"Connection failed: {e}")
            return False

    def awaitSimulationStart(self, timeout=30):
        self.clientSocket.settimeout(timeout)

        # Sending READY status
        send_message(
            self.clientSocket,
            {
                "type": "READY",
                "payload": {}
            }
        )

        try:
              response = receive_message(self.clientSocket)
        except socket.timeout:
            print("Waiting for simulation timeout")
            return None

        if response is None:
            return None

        if response.get("type") == "INIT_SIMULATION":
            print("Simulation initialized.")

            send_message(
                self.clientSocket,
                {
                    "type": "ACK",
                    "payload": {}
                }
            )

            return response["payload"]

        elif response["type"] == "ERROR":
            print(response["payload"]["error"])
        else:
            print(f"Unexpected message: {response.get('type')}")

        return None

    def awaitTurnStart(self, timeout=30):
        self.clientSocket.settimeout(timeout)

        # Sending READY status
        send_message(
            self.clientSocket,
            {
                "type": "READY",
                "payload": {}
            }
        )

        try:
            response = receive_message(self.clientSocket)
        except socket.timeout:
            print("Waiting for simulation timeout")
            return None

        if response is None:
            return None

        if response.get("type") == "INIT_TURN":
            print("Turn initialized.")

            send_message(
                self.clientSocket,
                {
                    "type": "ACK",
                    "payload": {}
                }
            )

            return response["payload"]

        elif response["type"] == "ERROR":
            print(response["payload"]["error"])
        else:
            print(f"Unexpected message: {response.get('type')}")

        return None

    def sendInTurnRequest(self, actions, timeout=30):
        self.clientSocket.settimeout(timeout)

        send_message(
            self.clientSocket,
            {
                "type": "IN_TURN_REQUEST",
                "payload": {
                    "requests": actions
                }
            }
        )

        try:
            response = receive_message(self.clientSocket)
        except socket.timeout:
            print("Waiting for simulation timeout")
            return None

        if response is None:
            return None

        if response.get("type") == "IN_TURN_RESPONSE":
            print("Received in turn response")

            send_message(
                self.clientSocket,
                {
                    "type": "ACK",
                    "payload": {}
                }
            )

            return response["payload"]

        elif response["type"] == "ERROR":
            print(response["payload"]["error"])
        else:
            print(f"Unexpected message: {response.get('type')}")

        return None

    def closeClientConnection(self):
        if self.clientSocket:
            self.clientSocket.close()
        print(f"Socket with port {self.clientPort} closed")