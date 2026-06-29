import tkinter as tk
from display_module.gui.simulation.simulation_screen import SimulationScreen
from network_module.networkModule import NetworkModule
from simulation_module.simulation import Simulation

# Define constants
CLIENT_PORT = 12345

if __name__ == '__main__':
    # Initializing simulation - Step 1 - Starting connection
    networkModule = NetworkModule()
    networkModule.initializeAgentSocket(CLIENT_PORT)
    networkModule.startAgentConnection()

    # Initializing simulation - Step 2 - Waiting for player to declare readiness
    networkModule.waitForAgentSimulationReady()

    # Initializing simulation - Step 3 - Sending initial data to the agent and waiting for response
    # Mockup data
    roundLimit = 15
    players = [0, 1, 2, 3]
    playerNames = ["Ty", "kuba", "michal", "bartek"]
    regions = [0, 1, 2]
    regionNames = ["alexandria", "radom", "warsaw"]
    regionNeighbours = [[1], [0, 2], [1]]

    networkModule.initSimulation(roundLimit, players, playerNames, regions, regionNames, regionNeighbours)



    # Starting new turn - Step 1 - Waiting for player to declare readiness
    networkModule.waitForAgentTurnReady()

    # Starting new turn - Step 2 - Sending turn data to the agent and waiting for their response
    # Mockup turn data
    currentRound = 1
    roundLimit = 15,
    players = [0, 1, 2, 3],
    playerNames = ["Ty", "kuba", "michal", "bartek"]
    leaderBoard = {"kuba": 150, "michal": 100, "bartek": 50}
    controlledUnits = ["light_infantry3", "light_infantry4", "heavy_infantry6", "cavalry2"]
    controlledRegionsId = [2]
    controlledRegionsNames = ["warsaw"]
    enemyUnitsPerRegion = [2]
    events = {
        "New message": "bartek: Let's team up against kuba!",
        "Your unit was destroyed!": "Your unit light_infantry2 was destroyed by heavy_infantry3 owned by kuba!"
    }

    networkModule.startTurn(currentRound, roundLimit, players, playerNames, leaderBoard, controlledUnits, controlledRegionsId, controlledRegionsNames, enemyUnitsPerRegion, events)

    currentOrderList = {}
    newMessages = {}
    # Simulating single within-turn communication
    networkModule.waitForAgentInTurnRequest(currentOrderList, newMessages)


    networkModule.closeAgentConnection()

    """
    simulation = Simulation([0])
    simulation.create_empty_board(9, 9, 9)
    simulation.add_light_infantry(0, -2, 2, 0)
    simulation.add_heavy_infantry(0, 4, -2, -2)
    simulation.add_cavalry(1, -3, -3, 6)

    simulation.board.tiles.get((0, 0, 0)).region = "Warszawa"
    simulation.board.tiles.get((-1, 0, 1)).region = "Warszawa"

    root = tk.Tk()

    root.title("Simulation")
    root.geometry("1280x720")
    root.minsize(900, 500)

    screen = SimulationScreen(root, simulation)
    screen.pack(fill="both", expand=True)

    root.mainloop()
    """