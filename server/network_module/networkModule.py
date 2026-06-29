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

    def waitForAgentInTurnRequest(self, currentOrderList, newMessages):
        while True:
            message = receive_message(self.agentConnection)

            if message is None:
                return False

            message_type = message.get("type")
            responses = []
            if message_type == "IN_TURN_REQUEST":
                for request in message["payload"]["requests"]:
                    if request["Action"] == "SendMessage":
                        # Send Message to the another player
                        responses.append(f"Message successfully sent to {request['PlayerId']}")
                    elif request["Action"] == "MoveUnit":
                        # Create a new order for the unit, verify its validity
                        responses.append(f"The order to move unit {request['UnitID']} to the position ({request['MoveQ']}, {request['MoveR']}, {request['MoveS']}) was successfully added to the list")
                    elif request["Action"] == "SupportUnit":
                        # Create a new support order, verify its validity
                        responses.append(f"The order for the unit {request['UnitID']} to support the unit {request['TargetUnitID']} was successfully added to the list")
                    elif request["Action"] == "AttackUnit":
                        # Create a new attack order, verify its validity
                        responses.append(f"The order for the unit {request['UnitID']} to attack the unit {request['TargetUnitID']} was successfully added to the list")
                    elif request["Action"] == "ObserveUnit":
                        # Get the local version of the map to display for the agent
                        responses.append(f"Tiles viewed by the unit {request['UnitID']}: ...")
                    elif request["Action"] == "ObserveRegion":
                        # Get the local version of the map to display for the agent
                        responses.append(f"Region {request['RegionId']} view: ...")
                    elif request["Action"] == "PlayerList":
                        # Get the locally stored list of players
                        responses.append(f"Players: Player1 (You), Player2, Player3")
                    elif request["Action"] == "LeaderBoard":
                        # Get the locally stored scoreboard of all players
                        responses.append(f"LeaderBoard: 1. Player1: 12304, 2. Player3: 4231, 3. Player2: 3394")
                    elif request["Action"] == "ControlledUnits":
                        # Get the list of currently owned units
                        responses.append(f"light_infantry3, light_infantry4, heavy_infantry6, cavalry2")
                    elif request["Action"] == "UnitDetails":
                        # Get the description of the unit visible to the player (and stored locally)
                        responses.append(f"Unit {request['UnitID']} description: ...")
                    elif request["Action"] == "ControlledRegions":
                        # Get the list of currently controlled regions
                        responses.append(f"Warsaw (id: 2)")
                    elif request["Action"] == "GetRecentEvents":
                        # Send again the list of events from the current round
                        responses.append(f"Recent events: New message: bartek: Let's team up against kuba!, Your unit was destroyed!: Your unit light_infantry2 was destroyed by heavy_infantry3 owned by kuba!")
                    elif request["Action"] == "GetConversation":
                        # Retrieve the conversation with the target player
                        responses.append(f"Conversation with the player {request['UserId']}")
                    else:
                        responses.append("The action couldn't be recognised!")

                send_message(
                    self.agentConnection,
                    {
                        "type": "IN_TURN_RESPONSE",
                        "payload": {
                            "system_responses": responses,
                            "order_list": currentOrderList,
                            "new_messages": newMessages
                        }
                    }
                )

                response = receive_message(self.agentConnection)
                if response is None:
                    return False

                if response.get("type") == "ACK":
                    print("In Turn Request Handled")
                    return True
                elif response["type"] == "ERROR":
                    print(response["payload"]["error"])
                else:
                    print("Unexpected response")

                return False


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
                "controlledRegionsId": controlledRegionsId,
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