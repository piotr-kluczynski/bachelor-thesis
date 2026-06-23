import socket
import json

from network_module.utils import receive_message, send_message


class NetworkModule:
    def __init__(self):
        self.agentSocket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.agentPort = None
        self.agentConnection = None
        self.agentAddress = None

    def initializeAgentSocket(self, agentPort, backlog=5):
        self.agentPort = agentPort

        # Socket options
        self.agentSocket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        self.agentSocket.bind(('', agentPort))
        self.agentSocket.listen(backlog)

        print(f"Listening on port {agentPort}")

    def startAgentConnection(self):
        try:
            self.agentConnection, self.agentAddress = self.agentSocket.accept()
            print(f"Got connection from {self.agentAddress}")

            return True
        except socket.error as e:
            print(f"Connection error: {e}")
            return False

    def waitForAgentSimulationReady(self, timeout=30):
        self.agentConnection.settimeout(timeout)

        while True:
            try:
                message = receive_message(self.agentConnection)
            except socket.timeout:
                print("Agent readiness timeout")
                return False

            if message is None:
                return False

            message_type = message.get("type")

            if message["type"] == "READY":
                print("Agent ready")
                return True
            elif message["type"] == "ERROR":
                print(message["payload"].get("error"))
                return False
            else:
                print(f"Unexpected message: {message_type}")

    def initSimulation(self,
                       roundLimit,
                       players, playerNames,
                       regions, regionNames, regionNeighbours
    ):
        message = {
            "type": "INIT_SIMULATION",
            "payload": {
                "roundLimit": roundLimit,
                "players": players,
                "playerNames": playerNames,
                "regions": regions,
                "regionNames": regionNames,
                "regionNeighbours": regionNeighbours
            }
        }

        send_message(self.agentConnection, message)

        response = receive_message(self.agentConnection)

        if response is None:
            return False

        if response.get("type") == "ACK":
            print("Simulation initialized")
            return True
        elif response["type"] == "ERROR":
            print(response["payload"]["error"])
        else:
            print("Unexpected response")

        return False

    def waitForAgentTurnReady(self, timeout=30):
        self.agentConnection.settimeout(timeout)

        while True:
            try:
                message = receive_message(self.agentConnection)
            except socket.timeout:
                print("Agent readiness timeout")
                return False

            if message is None:
                return False

            message_type = message.get("type")
            if message["type"] == "READY":
                print("Agent ready")
                return True
            elif message["type"] == "ERROR":
                print(message["payload"].get("error"))
                return False
            else:
                print(f"Unexpected message: {message_type}")

    def startTurn(self,
                  currentRound, roundLimit, players, leaderBoard,
                  controlledUnits, controlledRegionsId, controlledRegions, enemyUnitsPerRegion,
                  events
    ):
        message = {
            "type": "INIT_TURN",
            "payload": {
                "currentRound": currentRound,
                "roundLimit": roundLimit,
                "players": players,
                "leaderBoard": leaderBoard,
                "controlledUnits": controlledUnits,
                "controlledRegionsNames": controlledRegions,
                "enemyUnitsPerRegion": enemyUnitsPerRegion,
                "events": events,
                "endOfSimulationFlag" : False
            }
        }

        send_message(self.agentConnection, message)

        response = receive_message(self.agentConnection)
        if response is None:
            print("Turn started")
            return True
        elif response["type"] == "ERROR":
            print(response["payload"]["error"])
        else:
            print("Unexpected response")

        return False

    def closeAgentConnection(self):
        if self.agentConnection:
            self.agentConnection.close()
        print(f"Connection from {self.agentAddress} closed")

        if self.agentSocket:
            self.agentSocket.close()
        print(f"Socket with port {self.agentPort} closed")


"""
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
"""