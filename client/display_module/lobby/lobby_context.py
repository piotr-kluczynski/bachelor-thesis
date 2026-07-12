class LobbyContext:
    def __init__(self):
        self.name = "Simulation1"
        self.lobby_players = {
            "Piotr": True,
            "Olek": False,
            "Laura": True
        }
        self.settings = {
            "Max round": 150,
            "Supply counter": 12,
            "Max players": 10,
            "Map": "Equestria",
            "No. regions": 8,
            "Alliances": False
        }

        self.ready = False

    def ChangeReadyState(self):
        self.ready = not self.ready
        print(f"Changed the local user state from {not self.ready} to {self.ready}")

    def Leave(self):
        print("Leaving the lobby and navigating back to the simulation searching screen.")