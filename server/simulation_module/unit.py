class Unit:
    def __init__(self, unit_id, owner, movement, upkeep, strength):
        self.unit_id = unit_id
        self.owner = owner
        self.tile = None

        self.movement = movement
        self.upkeep = upkeep
        self.strength = strength

        self.movement_left = movement
        self.supporting_units = []
        self.alive = True

    def new_round(self):
        self.movement_left = self.movement
        self.supporting_units = []