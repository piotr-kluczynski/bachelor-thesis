# Importing libraries
import socket
import json
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, AIMessage
from langchain_openai import ChatOpenAI

from network_module.networkModule import NetworkModule
from prompts.simulationStartPrompt import simulationStartPrompt
from prompts.turnStartPrompt import turnStartPrompt
from prompts.systemResponsePrompt import systemResponsePrompt
from tools.tools import *

# Define constants
CLIENT_PORT = 12345

if __name__ == '__main__':
    # Defining the agent
    """
    tools = [
        sendMessage,
        moveUnit, supportUnit, attackUnit,
        observeUnit, observeRegion,
        finishTurn, playerList, leaderBoard, controlledUnits, controlledRegions, unitDetails, mapDescription,
        getRecentEvents, getRecentEvents
    ]

    model = ChatOpenAI(
        model="gpt-4.1-mini",
        api_key=input("Enter your API key: "),
    )

    agent = create_agent(
        model=model,
        tools=tools
    )
    """
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

    # Initializing the agent's conversation
    """
    conversation = [
        SystemMessage(
            content=simulationStartPrompt(roundLimit, players, playerNames, regions, regionNames, regionNeighbours)
        )
    ]
    """
    # Round loop
    while True:
        endOfTurnFlag = False
        # await turn start
        data = networkModule.awaitTurnStart()
        if data["endOfSimulationFlag"]:
            break

        print(turnStartPrompt(
                    data["currentRound"], data["roundLimit"], data["players"], data["leaderBoard"],
                    data["controlledUnits"], data["controlledRegions"], data["enemyUnitsPerRegion"],
                    data["events"]
                ))
        break

        # Sending the turn data to the chatbot
        conversation.append(
            SystemMessage(
                content=turnStartPrompt(
                    data["currentRound"], data["roundLimit"], data["players"], data["leaderBoard"],
                    data["controlledUnits"], data["controlledRegions"], data["enemyUnitsPerRegion"],
                    data["events"]
                )
            )
        )

        while not endOfTurnFlag:
            actions = []
            # Let chatbot make its choices
            response = agent.invoke(conversation)

            # Send the request to the server
            data = networkModule.sendInTurnRequest(actions)

            # Send system response to the chatbot
            conversation.append(
                AIMessage(content=response),
                SystemMessage(
                    content=systemResponsePrompt(data["systemResponses"], data["actionList"], data["newMessages"])
                )
            )


    """
    # Starting the Communication loop
    running = True
    
    while running:
        # Draw data about the new turn
        currentRound = 1 # drawn from app
        players = ["kuba", "michal", "bartek"] # drawn from app
        leaderBoard = {"kuba": 150, "michal": 100, "bartek": 50} # drawn from app
        controlledUnits = ["light_infantry3", "light_infantry4", "heavy_infantry6", "cavalry2"] # drawn from app
        controlledRegions = ["warsaw"] # drawn from app
        enemyUnitsPerRegion = [2] # drawn from app
        events = { # drawn from app
            "New message": "bartek: Let's team up against kuba!",
            "Your unit was destroyed!": "Your unit light_infantry2 was destroyed by heavy_infantry3 owned by kuba!"
        }
    
        conversation.append(
            SystemMessage(
                content=turnStartPrompt(
                    currentRound, roundLimit, players, leaderBoard,
                    controlledUnits, controlledRegions, enemyUnitsPerRegion,
                    events
                )
            )
        )
    
        playingTurn = True
        while playingTurn:
            response = agent.invoke(conversation)
    
            # Get system responses from the app
            systemResponses = ["Movement action was added successfully!", "<Map description>"] # drawn from app
            actionList = {"Action1":"Action1 description", "Action2":"Action2 description"} # drawn from app
            newMessages = {"kuba":"don't you even dare to conspire against me!"}
    
            conversation.append(
                AIMessage(content=response),
                SystemMessage(
                    content=systemResponsePrompt(systemResponses, actionList, newMessages)
                )
            )
    
            if False:
                playingTurn = False
    
        if False:
            running = False
    """