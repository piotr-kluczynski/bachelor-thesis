from simulation_module.action import Action


class SimulationContext:
    def __init__(self, my_id, manager):
        self.manager = manager # Reference to the Management object

        self.my_id = my_id # Current user id

        self.player_ids = [] # Array of player ids
        self.players_names = {} # Dictionary (player_id : playerName)
        self.players_status = {} # Dictionary (player_id : playerStatus)

        self.board = {} # Board object
        self.regions = {} # Dictionary ((q, r, s) : region_name)
        self.units = [] # Array of Unit objects
        self.simulated_occupancy = {} # Dictionary ((q, r, s) : Unit)

        self.current_round = 0
        self.max_round = 0

        self.console_content = [] # Array of string

        self.conversations = {} # Dictionary (player_id : Array of Message objects)

        self.notifications = [] # Array of Notification objects

        self.actions = [] # Array of Action objects

    def execute_command(self, command):
        self.console_content.append(f">{command}\r\n")
        # Just return "Unknown command error"
        self.console_content.append(f"Error: unknown command\r\nInput: {command}")

    def send_message(self, message):
        # Just add message to the conversation
        self.conversations[message.recipient] = message

    def add_action(self, unit_action, unit_id, target_id=None, move_vec=None):
        action = Action(unit_action, unit_id, target_id, move_vec)
        self.actions.append(action)

    def remove_action(self, action_id):
        # Just remove the action from the list
        self.actions.remove(self.actions[action_id])