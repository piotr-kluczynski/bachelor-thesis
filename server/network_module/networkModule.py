import socket
import json

from network_module.utils import receive_message, send_message


class NetworkModule:
    def __init__(self, manager):
        self.agentSocket = socket.socket()

        self.manager = manager
        self.agentPort = None
        self.agentConnection = None
        self.agentAddress = None

    def initializeAgentSocket(self, agentPort, backlog=5):
        self.agentPort = agentPort

        self.agentSocket.bind(('', agentPort))
        print(f"Socket bound to {agentPort}")
        self.agentSocket.listen(backlog)
        print("Socket is listening")

    def startAgentConnection(self):
        self.agentConnection, self.agentAddress = self.agentSocket.accept()
        print(f"Got connection from {self.agentAddress}")

    def closeAgentConnection(self):
        if self.agentSocket:
            self.agentSocket.close()
        print(f"Socket with port {self.agentPort} closed")

        if self.agentConnection:
            self.agentConnection.close()
        print(f"Connection from {self.agentAddress} closed")

    def sendSimulationDataToAgent(self, roundLimit, players, playerNames, regions, regionNames, regionNeighbours):
        if self.agentConnection is not None:
            data = {
                "roundLimit": roundLimit,
                "players": players,
                "playerNames": playerNames,
                "regions": regions,
                "regionNames": regionNames,
                "regionNeighbours": regionNeighbours
            }

            json_data = json.dumps(data).encode("utf-8")
            messageLength = len(json_data)

            self.agentConnection.sendall(messageLength.to_bytes(4, "big"))
            self.agentConnection.sendall(json_data)

            print("Simulation data sent to agent")
        else:
            print("No connection to agent")

    def handleConnection(self):
        while True:
            request = receive_message(self.agentConnection)
            print(f"Received: {request}")

            if request["action"] == "get_simulation_data":
                roundLimit, players, playerNames, regions, regionNames, regionNeighbours = self.manager.getSimulationData() # Correct it later to properly draw data from the manager

                response = {
                    "roundLimit": roundLimit,
                    "players": players,
                    "playerNames": playerNames,
                    "regions": regions,
                    "regionNames": regionNames,
                    "regionNeighbours": regionNeighbours
                }
            else:
                response = {
                    "error": "Unknown action"
                }

            send_message(self.agentConnection, response)

    def sendMessageToAgent(self, message):
        self.agentConnection.send(message.encode())