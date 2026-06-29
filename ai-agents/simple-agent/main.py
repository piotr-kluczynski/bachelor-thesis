# Importing libraries
from network_module.networkModule import NetworkModule
from players import PlayerStrategy
from players.DebugMode import DebugMode
from prompts.simulationStartPrompt import simulationStartPrompt
from prompts.roundStartPrompt import roundStartPrompt
from prompts.turnEndPrompt import turnEndPrompt
from tools.tools import *
from tools.tools import supportUnit

# Define constants
CLIENT_PORT = 12345

# Defining Context object (Strategy pattern)
class Context:
    def __init__(self, playerStrategy: PlayerStrategy) -> None:
        self.playerStrategy = playerStrategy

    def initialize(self):
        self.playerStrategy.initializePlayer()

    def simulationStart(self, roundLimit, players, playerNames, regions, regionNames, regionNeighbours):
        simulationStartMessage = simulationStartPrompt(roundLimit, players, playerNames, regions, regionNames, regionNeighbours)
        self.playerStrategy.simulationStart(simulationStartMessage)

    def simulationEnd(self):
        self.playerStrategy.endSimulation()

    def roundStart(self, currentRound, roundLimit, players, playerNames, leaderBoard,
                   controlledUnits, controlledRegionsId, controlledRegionsNames, enemyUnitsPerRegion,
                   events):
        roundStartMessage = roundStartPrompt(currentRound, roundLimit, players, playerNames, leaderBoard, controlledUnits, controlledRegionsId, controlledRegionsNames, enemyUnitsPerRegion, events)
        self.playerStrategy.roundStart(roundStartMessage)
    def roundEnd(self):
        self.playerStrategy.roundEnd()

    def turnStart(self):
        self.playerStrategy.turnStart()
    def turnEnd(self, systemResponses, orderList, newMessages):
        turnStartMessage = turnEndPrompt(systemResponses, orderList, newMessages)
        self.playerStrategy.turnEnd(turnStartMessage)

if __name__ == '__main__':
    # Defining the player
    tools = [
        sendMessage,
        moveUnit, supportUnit, attackUnit,
        observeUnit, observeRegion,
        finishTurn, playerList, leaderBoard, controlledUnits, controlledRegions, unitDetails, mapDescription,
        getRecentEvents, getRecentEvents
    ]

    # CHANGE TO THE DESIRED AGENT
    context = Context(
        DebugMode(tools)
    )
    """
    context = Context(
        SimpleAgent(
            model_version="gpt-4.1-mini",
            tools=tools
        )
    )
    """
    context.initialize()

    # Initializing simulation - Step 1 - Connecting to the application
    networkModule = NetworkModule()
    networkModule.startClientConnection(CLIENT_PORT)

    # Initializing simulation - Step 2 - Initializing simulation
    data = networkModule.awaitSimulationStart()

    if data is not None:
        roundLimit = data["roundLimit"]
        players = data["players"]
        playerNames = data["playerNames"]
        regions = data["regions"]
        regionNames = data["regionNames"]
        regionNeighbours = data["regionNeighbours"]

    # Starting the player
    context.simulationStart(data["roundLimit"], data["players"], data["playerNames"], data["regions"], data["regionNames"], data["regionNeighbours"])

    # Round loop
    while True:
        endOfRoundFlag = False
        # await turn start
        data = networkModule.awaitTurnStart()

        # Sending the turn data to the chatbot
        context.roundStart(
            data["currentRound"], data["roundLimit"], data["players"], data["playerNames"], data["leaderBoard"],
            data["controlledUnits"], data["controlledRegionsId"], data["controlledRegionsNames"],
            data["enemyUnitsPerRegion"], data["events"]
        )

        while not endOfRoundFlag:
            # Clearing the action list after the previous turn
            used_actions.clear()

            # Let chatbot make its choices
            context.turnStart()

            # Send the request to the server
            data = networkModule.sendInTurnRequest(used_actions)

            context.turnEnd(data["system_responses"], data["order_list"], data["new_messages"])

            # Check if the current round shouldn't end
            for action in used_actions:
                if action["Action"] == "FinishTurn":
                    endOfRoundFlag = True