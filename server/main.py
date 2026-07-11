# Define constants
CLIENT_PORT = 12345

if __name__ == '__main__':
    """
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

    """
    players = ["Piotrek", "Marcin", "Michał"]
    max_round = 5
    upkeep_round = 3
    simulation = Simulation(players, max_round, upkeep_round)

    tiles_between = [
        Tile(0, 0, 0),  # Land Between
        Tile(-1, 0, 1),  # Land Between
        Tile(1, -1, 0),  # Land Between
        Tile(0, 1, -1),  # Land Between
    ]
    region_between = Region(tiles_between, (0, 0, 0), region_upkeep=4)

    tiles_q = [
        Tile(0, -1, 1),  # Land of Q
        Tile(-1, -1, 2),  # Land of Q
        Tile(0, -2, 2),  # Land of Q
        Tile(1, -2, 1),  # Land of Q
    ]
    region_q = Region(tiles_q, (0, -2, 2), owner="Piotrek")

    tiles_r = [
        Tile(1, 0, -1),  # Land of R
        Tile(2, 0, -2),  # Land of R
        Tile(2, -1, -1),  # Land of R
        Tile(1, 1, -2),  # Land of R
    ]
    region_r = Region(tiles_r, (2, 0, -2), owner="Marcin")

    tiles_s = [
        Tile(-1, 1, 0),  # Land of S
        Tile(-2, 1, 1),  # Land of S
        Tile(-2, 2, 0),  # Land of S
        Tile(-1, 2, -1)  # Land of S
    ]
    region_s = Region(tiles_s, (-2, 2, 0), owner="Michał")

    starting_units = {
        (0, -2, 2): [Unit("light_infantry1", "Piotrek", 2, 1, 6)],
        (2, 0, -2): [Unit("light_infantry2", "Marcin", 2, 1, 6)],
        (-2, 2, 0): [Unit("light_infantry3", "Michał", 2, 1, 6)],
    }

    total_tiles = {}
    for tile in tiles_between + tiles_r + tiles_s + tiles_q:
        total_tiles[(tile.q, tile.r, tile.s)] = tile

    simulation.start_simulation(
        total_tiles,
        [region_between, region_q, region_r, region_s],
        starting_units
    )

    print(simulation.units)
    """


    """
    root = tk.Tk()

    root.title("Simulation")
    root.geometry("1280x720")
    root.minsize(900, 500)

    screen = SimulationScreen(root, simulation.board, {}, [0, 1, 2], {0: "Andrzej (You)", 1: "Kuba", 2: "Michał"})
    screen.pack(fill="both", expand=True)

    root.mainloop()
    """