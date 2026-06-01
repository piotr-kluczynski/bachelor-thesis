from simulation_module.action import Action


class SimulationContext:
    def __init__(self, simulation): # Temporarily passing simulation reference for development
        #self.manager = manager # Reference to the Management object
        self.board_panel = None # Board panel reference, possibly replace with better solution access board_panel

        self.my_id = 0 # Current user id

        self.players_ids = [] # Array of player ids
        self.players_names = {} # Dictionary (player_id : playerName)
        self.players_status = {} # Dictionary (player_id : playerStatus)
        self.player_colors = {} # Dictionary (player_id : playerColor)

        self.board = simulation.board # {} Board object
        self.regions = {} # Dictionary ((q, r, s) : region_name)
        self.units = simulation.units # []  Array of Unit objects
        self.simulated_occupancy = {} # Dictionary ((q, r, s) : Unit)

        self.current_round = 0
        self.max_round = 0

        self.console_content = [] # Array of string

        self.conversations = {} # Dictionary (player_id : Array of Message objects)

        self.notifications = [] # Array of Notification objects

        self.actions = [] # Array of Action objects

        self.initialize()

    # Hard-coded function for creating the initial data
    def initialize(self):
        self.players_ids = [0, 1, 2, 3, 4]
        self.players_names = {0: "Piotr", 1: "Alex", 2: "Bob", 3: "Martin", 4: "Eva"}
        self.players_status = {0: "Online", 1: "Online", 2: "Online", 3: "Online", 4: "Online"}
        self.players_colors = {0: "green", 1: "blue", 2: "red", 3: "yellow", 4: "purple"}

        self.regions = {(0, 0, 0): "Central region"}

        self.current_round = 1
        self.max_round = 50

        self.conversations = {1 : [], 2 : [], 3 : [], 4 : []}


    def execute_command(self, command):
        self.console_content.append(f">{command}\r\n")
        # Just return "Unknown command error"
        self.console_content.append(f"Error: unknown command\r\nInput: {command}")

    def send_message(self, message):
        # Just add message to the conversation
        self.conversations[message.recipient].append(message)

    def add_action(self, unit_action, unit_id, target_id=None, move_vec=None):
        action = Action(unit_action, unit_id, target_id, move_vec)
        self.actions.append(action)

    def remove_action(self, action_id):
        # Just remove the action from the list
        self.actions.remove(self.actions[action_id])

    def center_camera_on(self, q, r):
        if self.board_panel is not None:
            self.board_panel.center_camera_on(q, r)