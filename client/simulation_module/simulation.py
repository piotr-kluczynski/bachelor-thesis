import random
from simulation_module.board import Board
from simulation_module.unit import Unit
from simulation_module.action import Action
from simulation_module.tile import Tile
from simulation_module.utils import calc_distance

class Simulation:
    def __init__(self, localPlayerName, players, max_round):
        self.localPlayerName = localPlayerName
        self.players = players

        self.actions = []
        self.units = {}
        self.occupancy = {}
        self.simulated_occupancy = {}
        self.board = Board()

        self.round = 1
        self.max_round = max_round

        self.new_unit_id = 0

    # TURN MANAGEMENT
    def new_round(self, actions, units):
        # Clear simulated occupancy
        self.simulated_occupancy = {}

        # Reset the units list
        self.units = units

    def end_round(self):
        self.occupancy = {}
        self.simulated_occupancy = {}

        # Executing players actions
        self.execute_player_actions()
        self.players_actions = {}

        # Removing dead units
        dead_units = []
        for unit_id, unit in self.units.items():
            if not unit.alive:
                dead_units.append(unit_id)
            else:
                self.occupancy[(unit.tile.q, unit.tile.r, unit.tile.s)] = unit

        for unit_id in dead_units:
            self.units[unit_id].tile = None
            del self.units[unit_id]

    # PROCESSING PLAYER ACTIONS
    def add_player_action(self, newAction):
        # Verify that you have ownership of this unit
        if self.units[newAction.unit_id].owner is not self.localPlayerName:
            return False

        # Verify that the action is not given to already used unit
        for action in self.actions:
            if action.unit_id == newAction.unit_id:
                return False

        # Verify (locally) that the action target is within range
        unit_q, unit_r, unit_s = [key for key, val in self.simulated_occupancy.items() if val == self.units[newAction.unit_id]]

        if newAction.unit_action == "Move": # Verify the movement action
            unit = self.units[newAction.unit_id]

            unit_tile = unit.tile
            target_tile = self.units[newAction.target_unit_id]

            path = self.board.find_shortest_path(unit_tile, target_tile, unit.movement_left, self.simulated_occupancy)

            if path is None:
                return False
            else:
                self.actions.append(newAction)

                del self.simulated_occupancy[(unit_tile.q, unit_tile.r, unit_tile.s)]
                self.simulated_occupancy[(target_tile.q, target_tile.r, target_tile.s)] = unit

                return True
        else: # Verify the attack/support actions
            target_q, target_r, target_s = [key for key, val in self.simulated_occupancy.items() if val == self.units[newAction.target_id]]

            if calc_distance(unit_q, unit_r, unit_s, target_q, target_r, target_s) > 1:
                return False

            self.actions.append(newAction)
            return True
    def cancel_player_action(self, action):
        self.actions.remove(action)
        return True

    # GENERATING BOARD
    def create_empty_board(self, q_range, r_range, s_range):
        new_tiles = {}
        for q in range(-q_range, q_range+1):
            for r in range(-r_range, r_range+1):
                for s in range(-s_range, s_range+1):
                    if q + r + s == 0:
                        new_tiles[(q, r, s)] = Tile(q, r, s)
        self.board.tiles = new_tiles

    # CREATING UNITS
    def add_light_infantry(self, owner, q, r, s):
        tile = self.board.get_tile_by_coord(q, r, s)

        if tile.unit is not None:
            return False

        light_infantry = Unit(f"light_infantry_{self.new_unit_id}", owner, 2, 1, 6)
        tile.unit = light_infantry
        light_infantry.tile = tile

        self.units.update({f"light_infantry_{self.new_unit_id}": light_infantry})
        self.new_unit_id += 1

        # Adding to the occupancy new unit
        self.occupancy[(tile.q, tile.r, tile.s)] = light_infantry

        return True
    def add_heavy_infantry(self, owner, q, r, s):
        tile = self.board.get_tile_by_coord(q, r, s)

        if tile.unit is not None:
            return False

        heavy_infantry = Unit(f"heavy_infantry_{self.new_unit_id}", owner, 1, 2, 8)
        tile.unit = heavy_infantry
        heavy_infantry.tile = tile

        self.units.update({f"heavy_infantry_{self.new_unit_id}": heavy_infantry})
        self.new_unit_id += 1

        # Adding to the occupancy new unit
        self.occupancy[(tile.q, tile.r, tile.s)] = heavy_infantry

        return True
    def add_cavalry(self, owner, q, r, s):
        tile = self.board.get_tile_by_coord(q, r, s)

        if tile.unit is not None:
            return False

        cavalry = Unit(f"cavalry_{self.new_unit_id}", owner, 3, 3, 6)
        tile.unit = cavalry
        cavalry.tile = tile

        self.units.update({f"cavalry_{self.new_unit_id}": cavalry})
        self.new_unit_id += 1

        # Adding to the occupancy new unit
        self.occupancy[(tile.q, tile.r, tile.s)] = cavalry

        return True

    # OBSERVATION ACTIONS
    def observe_unit(self, unit_id):
        unit = self.units[unit_id]
        return self.board.get_tiles_in_range(unit.tile, 3)
    def observe_region(self, region_id):
        return self.board.regions[region_id]

    # UNIT ACTIONS
    def move_unit(self, unit, dq, dr, ds):
        if unit.movement_left <= 0:
            return False

        current_tile = unit.tile

        new_q = current_tile.q + dq
        new_r = current_tile.r + dr
        new_s = current_tile.s + ds

        target_tile = self.board.get_tile_by_coord(new_q, new_r, new_s)
        if target_tile is None:
            return False

        if not target_tile.is_available():
            return False

        target_tile.unit = self
        current_tile.unit = None
        unit.movement_left -= 1

        return True
    def attack_unit(self, unit1, unit2):
        tile1 = unit1.tile
        tile2 = unit2.tile

        if calc_distance(tile1.q, tile1.r, tile1.s, tile2.q, tile2.r, tile2.s) > 1:
            return False

        if not unit2.alive:
            return False

        attack_power = random.randrange(1, unit1.strength)
        for _ in unit1.supporting_units:
            attack_power += 2

        defend_power = random.randrange(1, unit2.strength)
        for _ in unit2.supporting_units:
            defend_power += 2

        if defend_power >= attack_power:
            # Defenders stand their ground
            return True
        else:
            if 2*defend_power <= attack_power:
                # Defenders are completely destroyed
                unit2.alive = False
                return True

            # Defenders were defeated and fall back
            self.push_chain(unit1, unit2)
            return True
    def support_unit(self, unit1, unit2):
        tile1 = unit1.tile
        tile2 = unit2.tile

        if calc_distance(tile1.q, tile1.r, tile1.s, tile2.q, tile2.r, tile2.s) > 1:
            return False

        if not unit2.alive:
            return False

        unit2.supporting_units.append(unit1)
        return True

    def push_chain(self, unit1, unit2):
        chain = []

        current_tile = unit2.tile

        # Calculating the direction of the push
        dq = current_tile.q - unit1.tile.q
        dr = current_tile.r - unit1.tile.r
        ds = current_tile.s - unit1.tile.s

        # Building chain of tiles
        while current_tile.unit is not None:
            unit = current_tile.unit
            chain.append(unit)

            next_tile = self.board.get_tile_by_coord(
                current_tile.q + dq,
                current_tile.r + dr,
                current_tile.s + ds
            )

            # Board end
            if next_tile is None:
                break

            current_tile = next_tile

        # Checking if the last tile is free
        can_escape = current_tile.unit is None

        # If there's no space to fall back, the unit dies
        if not can_escape:
            unit2.alive = False

        # Moving to the back
        for unit in reversed(chain):
            old_tile = unit.tile

            new_tile = self.board.get_tile_by_coord(
                old_tile.q + dq,
                old_tile.r + dr,
                old_tile.s + ds
            )

            old_tile.unit = None
            new_tile.unit = unit
            unit.tile = new_tile

        return True