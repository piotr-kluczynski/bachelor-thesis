import tkinter as tk

from display_module.gui.simulation.simulation_screen import SimulationScreen
from simulation_module.simulation import Simulation


class Manager:
    def __init__(self, display_mode):
        self.network = None # Initialize NetworkModule module

        # Start up as None - they are related to specific moments of application
        self.display = None
        self.logging = None
        self.simulation = None

        # Currently hardcoded data, later to be drawn from network module
        self.my_id = None
        self.players_ids = []
        self.players_names = {}
        self.players_status = {}

        self.display_mode = display_mode
        self.root = None # for GUI mode

        self.console = {}
        self.notifications = []
        self.conversations = {}

    def start_program(self):
        # Initialize the display
        if self.display_mode == "gui":
            self.root = tk.Tk()

    def join_session(self):
        self.my_id = 0
        # Other operations involving the network management

    def start_simulation(self):
        # Draw data from the session from the network module (or maybe just pass this data through the parameters?)
        self.players_ids = [0, 1, 2, 3, 4]
        self.players_names = {0: "Piotr", 1: "Alex", 2: "Bob", 3: "Martin", 4: "Eva"}
        self.players_status = {0: "Online", 1: "Online", 2: "Online", 3: "Online", 4: "Online"}
        max_round = 30

        for player_id in self.players_ids:
            self.conversations[player_id] = []



        # Initialize simulation
        # Currently hard-coded settings, later they need to be drawn from the simulation settings from networking module?
        self.simulation = Simulation(self.players_ids, max_round, )

        # Start the simulation screen
        if self.display_mode == "gui":
            self.root.title("Simulation")
            self.root.geometry("1280x720")
            self.root.minsize(900, 500)

            self.display = SimulationScreen(self.root)
            self.display.pack(fill="both", expand=True)

            self.root.mainloop()