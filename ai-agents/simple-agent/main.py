# Importing libraries
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from prompts.simulationStartPrompt import simulationStartPrompt
from prompts.turnStartPrompt import turnStartPrompt
from prompts.systemResponsePrompt import systemResponsePrompt
from tools.tools import *

# Define constants
API_KEY = input("Enter your API key: ")

# Test connection with the local application
running = True

finalRoundNum = 15 # drawn from app
playerList = ["kuba", "michal", "bartek"] # drawn from app
regionNames = {0:"alexandria", 1:"radom", 2:"warsaw"} # drawn from app
regionNeighbours = [[1], [0, 2], [1]] # drawn from app

# Defining the agent
tools = [
    sendMessage,
    moveUnit, supportUnit, attackUnit,
    observeUnit, observeRegion,
    playerList, leaderBoard, controlledUnits, controlledRegions, unitDetails, mapDescription, getRecentEvents, getRecentEvents
]

model = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=API_KEY,
)

agent = create_agent(
    model=model,
    tools=tools
)

conversation = [
    SystemMessage(
        content=simulationStartPrompt(finalRoundNum, playerList, regionNames, regionNeighbours)
    )
]

while running:
    # Draw data about the new turn
    currentRound = 1 # drawn from app
    playerList = ["kuba", "michal", "bartek"] # drawn from app
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
                currentRound, finalRoundNum, playerList, leaderBoard,
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