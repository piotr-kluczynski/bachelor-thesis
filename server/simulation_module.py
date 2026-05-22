import random

class Simulation:
    def __init__(self, players):
        self.players = players

        self.players_actions = {}
        self.units = {}
        self.board = Board()

        self.new_unit_id = 0

    def add_player_actions(self, owner, action_list):
        self.players_actions[owner] = action_list
        return True

    def execute_action(self, order):
        unit = self.units[order.unit_id]

        if order.unit_action == "Move":
            q, r, s = order.move_vec
            return unit.move(q, r, s, self.board)

        target_unit = self.units[order.target_id]
        target_tile = self.board.get_tile_by_unit(target_unit)

        if order.unit_action == "Attack":
            return unit.attack(target_tile, self.board)

        if order.unit_action == "Support":
            return unit.support(target_tile, self.board)

        return False

    def add_light_infantry(self, owner, q, r, s):
        tile = self.board.get_tile_by_coord(q, r, s)

        if tile.unit is not None:
            return False

        light_infantry = Unit(self.new_unit_id, owner, 2, 1, 6)
        tile.unit = light_infantry

        self.units.update({self.new_unit_id: light_infantry})
        self.new_unit_id += 1

        return True
    def add_heavy_infantry(self, owner, q, r, s):
        tile = self.board.get_tile_by_coord(q, r, s)

        if tile.unit is not None:
            return False

        heavy_infantry = Unit(self.new_unit_id, owner, 1, 2, 8)
        tile.unit = heavy_infantry

        self.units.update({self.new_unit_id: heavy_infantry})
        self.new_unit_id += 1

        return True
    def add_cavalry(self, owner, q, r, s):
        tile = self.board.get_tile_by_coord(q, r, s)

        if tile.unit is not None:
            return False

        cavalry = Unit(self.new_unit_id, owner, 3, 3, 6)
        tile.unit = cavalry

        self.units.update({self.new_unit_id: cavalry})
        self.new_unit_id += 1

        return True

    def end_round(self):
        for player_actions in self.players_actions.values():
            for action in player_actions:
                self.execute_action(action)

        for unit_id, unit in self.units.items():
            if not unit.alive:
                self.board.get_tile_by_unit(unit).unit = None
                self.units.pop(unit_id)
                del unit

        self.players_actions = {}


class Order:
    def __init__(self, unit_id, unit_action, target_id, move_vec):
        self.unit_id = unit_id
        self.unit_action = unit_action
        self.target_id = target_id
        self.move_vec = move_vec


class Unit:
    def __init__(self, unit_id, owner, movement, upkeep, strength):
        self.unit_id = unit_id
        self.owner = owner

        self.movement = movement
        self.upkeep = upkeep
        self.strength = strength

        self.movement_left = movement
        self.supporting_units = []
        self.alive = True

    def move(self, q_1, r_1, s_1, board):
        if self.movement_left <= 0:
            return False

        current_tile = board.get_tile_by_unit(self)

        new_q = current_tile.q+q_1
        new_r = current_tile.r+r_1
        new_s = current_tile.s+s_1

        new_tile = board.get_tile_by_coord(new_q, new_r, new_s)
        if new_tile is None:
            return False

        if not new_tile.is_available():
            return False

        new_tile.unit = self
        current_tile.unit = None
        self.movement_left -= 1

        return True
    def attack(self, opponent_tile, board):
        current_tile = board.get_tile_by_unit(self)
        opponent_unit = opponent_tile.unit

        if calc_distance(current_tile.q, current_tile.r, current_tile.s, opponent_tile.q, opponent_tile.r, opponent_tile.s) > 1:
            return False

        if opponent_unit is None:
            return False

        attack_power = random.randrange(1, self.strength)
        for _ in self.supporting_units:
            attack_power += 2

        opponent_unit.defend(attack_power, board)
        return True
    def defend(self, attack_power):
        defend_power = random.randrange(1, self.strength)

        if defend_power >= attack_power:
            return False

        self.alive = False
        return True
    def support(self, ally_tile, board):
        current_tile = board.get_tile_by_unit(self)
        ally_unit = ally_tile.unit

        if calc_distance(current_tile.q, current_tile.r, current_tile.s, ally_tile.q, ally_tile.r, ally_tile.s) > 1:
            return False

        if ally_unit is None:
            return False

        ally_unit.supporting_units.append(self)
        return True

    def new_round(self):
        self.movement_left = self.movement
        self.supporting_units = []


class Tile:
    def __init__(self, q, r, s):
        self.q = q
        self.r = r
        self.s = s
        self.unit = None

    def is_available(self):
        return False if self.unit is None else True

class Board:
    def __init__(self, tiles = None):
        if tiles is None:
            self.tiles = []
            for q in range(5):
                temp1 = []
                for r in range(5):
                    temp2 = []
                    for s in range(5):
                        temp2.append(Tile(q, r, s))
                    temp1.append(temp2)
                self.tiles.append(temp1)

        else:
            self.tiles = tiles

    def get_tile_by_coord(self, q, r, s):
        if not validate_coord(q, r, s):
            return None

        return self.tiles[q][r][s]
    def get_tile_by_unit(self, unit):
        for q in range(len(self.tiles)):
            for r in range(len(self.tiles[q])):
                for s in range(len(self.tiles[q][r])):
                    if self.tiles[q][r][s].unit == unit:
                        return self.tiles[q][r][s]
        return None


def validate_coord(q, r, s):
    return True if q + r + s == 0 else False

def calc_distance(q_1, r_1, s_1, q_2, r_2, s_2):
    return (abs(q_1 - q_2) + abs(r_1 - r_2) + abs(s_1 - s_2)) / 2