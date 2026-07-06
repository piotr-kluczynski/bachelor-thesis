from enum import Enum

class ActionType(Enum):
    HOLD = "Hold"
    MOVE = "Move"
    ATTACK = "Attack"
    SUPPORT = "Support"

class Action:
    def __init__(self, unit_action, unit_id, target_id=None, move_vec=None):
        self.unit_action = unit_action
        self.unit_id = unit_id
        self.target_id = target_id
        self.move_vec = move_vec