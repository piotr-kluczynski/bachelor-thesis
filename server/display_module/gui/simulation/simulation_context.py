from simulation_module.action import Action

COLORS = {
    0 : "red",
    1 : "green",
    2 : "blue",
    3 : "brown",
    4 : "yellow",
    5: "purple"
}

class SimulationContext:
    def __init__(self, board, units, players_ids):
        #self.manager = manager # Reference to the Management object
        self.board_panel = None # Board panel reference, possibly replace with better solution access board_panel
        self.players_colors = {} # Dictionary (player_id : playerColor)

        self.board = board # {} Board object
        self.regions = {} # Dictionary ((q, r, s) : region_name)
        self.units = units # []  Array of Unit objects
        self.simulated_occupancy = {} # Dictionary ((q, r, s) : Unit)

        self.console_content = [] # Array of string

        self.conversations = {} # Dictionary (player_id : Array of Message objects)

        self.notifications = [] # Array of Notification objects

        self.actions = [] # Array of Action objects

        self.initialize()

    # Hard-coded function for creating the initial data
    def initialize(self):
        self.players_colors = {0: "green", 1: "blue", 2: "red", 3: "yellow", 4: "purple"}

        for player_id in self.players_ids:
            self.players_colors[player_id] = COLORS[player_id]



    def execute_command(self, command):
        self.console_content.append(f">{command}\r\n")
        # Just return "Unknown command error"
        self.console_content.append(f"Error: unknown command\r\nInput: {command}")

    def send_message(self, message):
        # Just add message to the conversation
        self.conversations[message.recipient].append(message)

    def declare_attack(self, unit, target_unit):
        return 0

    def declare_support(self, unit, target_unit):
        return 0

    def declare_move(self, unit, coords):
        return 0

    def add_action(self, unit_action, unit_id, target_id=None, move_vec=None):
        action = Action(unit_action, unit_id, target_id, move_vec)
        self.actions.append(action)

    def remove_action(self, action_id):
        # Just remove the action from the list
        self.actions.remove(self.actions[action_id])

    def center_camera_on(self, q, r):
        if self.board_panel is not None:
            self.board_panel.center_camera_on(q, r)