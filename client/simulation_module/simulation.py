import random
from enum import Enum

from simulation_module.board import Board
from simulation_module.unit import Unit
from simulation_module.action import Action, ActionType
from simulation_module.utils import calc_distance

UNIT_TYPES = {
    "light_infantry": (2, 1, 6),
    "heavy_infantry": (1, 2, 8),
    "cavalry": (3, 3, 6)
}

class PlayerStatus(Enum):
    ACTIVE = "Active"
    EXILED = "Exiled"
    LOST = "Lost"

class Simulation:
    def __init__(self, my_id, players, max_round, upkeep_round, tiles, regions):
        self.my_id =my_id
        self.players = players
        self.players_status = {player: PlayerStatus.ACTIVE for player in players}

        self.my_actions = []
        self.units = {}
        self.occupancy = {}
        self.simulated_occupancy = {}
        self.board = Board(tiles, regions)

        self.round = 1
        self.max_round = max_round
        self.upkeep_round = upkeep_round

    # TURN MANAGEMENT
    def start_round(self):
        self.round += 1
        if self.round > self.max_round:
            return False
        return True
    def synchronize_game_state(self, simulation_updates):
        for update in simulation_updates:
            if update["type"] == "unit_death":
                unit_id = update["unit_id"]

                self.units[unit_id].alive = False
            elif update["type"] == "unit_move":
                unit_id = update["unit_id"]
                new_q, new_r, new_s = update["new_q"], update["new_r"], update["new_s"]

                self.place_unit(self.units[unit_id], self.board.get_tile_by_coord(new_q, new_r, new_s))
            elif update["type"] == "unit_spawn":
                unit_type = update["unit_type"]
                unit_id = update["unit_id"]
                owner = update["owner"]
                q, r, s = update["q"], update["r"], update["s"]

                self.add_unit(unit_type, unit_id, owner, q, r, s)
            elif update["type"] == "player_status_change":
                player = update["player"]
                new_status = update["new_status"]

                self.players_status[player] = new_status
            elif update["type"] == "region_owner_change":
                region_id = update["region_id"]
                new_owner = update["new_owner"]

                self.board.regions[region_id].owner = new_owner
    def end_round(self):
        self.simulated_occupancy = {}
        self.my_actions = []

        # Removing dead units and rebuilding occupancy
        self.occupancy = {}
        dead_units = []

        for unit_id, unit in self.units.items():
            if not unit.alive:
                dead_units.append(unit_id)
            else:
                self.occupancy[(unit.tile.q, unit.tile.r, unit.tile.s)] = unit
                unit.new_round() # We reset all persisting units temporary parameters

        for unit_id in dead_units:
            self.units[unit_id].tile = None
            self.units[unit_id].tile.unit = None
            del self.units[unit_id]

    # PREPARING PLAYER ACTIONS
    def add_player_actions(self, action_list):
        movement_actions, support_actions, attack_actions = self.process_action_list(action_list)
        if movement_actions is None:
            return False

        self.my_actions = movement_actions + support_actions + attack_actions
        return True
    def expand_movement_actions(self, action_list):
        result = []

        for action in action_list:
            dq, dr, ds = action.move_vec
            unit = self.units[action.unit_id]
            unit_tile = unit.tile
            target_tile = self.board.get_tile_by_coord(unit_tile.q + dq, unit_tile.r + dr, unit_tile.s + ds)

            path = self.board.find_shortest_path(unit_tile, target_tile, unit.movement_left, self.simulated_occupancy)

            if path is None:
                return False

            for i in range(0, len(path)-1):
                move_vec = (path[i+1].q - path[i].q, path[i+1].r - path[i].r, path[i+1].s - path[i].s)
                result.append(Action(ActionType.MOVE, action.unit_id, move_vec=move_vec))

            # Update simulated occupancy
            self.simulated_occupancy.pop((unit_tile.q, unit_tile.r, unit_tile.s), None)
            self.simulated_occupancy[(target_tile.q, target_tile.r, target_tile.s)] = unit

        return result
    def split_actions(self, action_list):
        move_actions = [a for a in action_list if a.unit_action == ActionType.MOVE]
        support_actions = [a for a in action_list if a.unit_action == ActionType.SUPPORT]
        attack_actions = [a for a in action_list if a.unit_action == ActionType.ATTACK]

        return move_actions, support_actions, attack_actions

    def verify_action_uniqueness(self, action_list):
        ids = [a.unit_id for a in action_list]
        return len(ids) == len(set(ids))
    def verify_unit_ownership(self, player, action_list):
        for action in action_list:
            unit = self.units[action.unit_id]
            if unit.owner != player:
                return False

        return True
    def verify_action_range(self, action_list, occupancy):
        for action in action_list:
            unit = self.units[action.unit_id]
            target_unit = self.units[action.target_id]

            unit_coords = [key for key, val in occupancy.items() if val == unit]
            target_coords = [key for key, val in occupancy.items() if val == target_unit]

            if not unit_coords or not target_coords:
                return False

            unit_q, unit_r, unit_s = unit_coords[0]
            target_q, target_r, target_s = target_coords[0]

            if calc_distance(unit_q, unit_r, unit_s, target_q, target_r, target_s) > 1:
                return False
        return True

    def process_action_list(self, action_list):
        # We create simulated occupancy to predict future unit positions
        self.simulated_occupancy = self.occupancy.copy()

        # Check if every unit received up to 1 action
        if not self.verify_action_uniqueness(action_list):
            return None, None, None

        # Check if every ordered unit is owned by the player
        if not self.verify_unit_ownership(self.my_id, action_list):
            return None, None, None

        # Divide actions into categories: Movement, Support, Attack
        movement_actions, support_actions, attack_actions = self.split_actions(action_list)

        # Expand movement actions into separate moves
        expanded_movement_actions = self.expand_movement_actions(movement_actions)
        if expanded_movement_actions is False:
            return None, None, None

        # Removing impossible support actions
        if not self.verify_action_range(support_actions, self.simulated_occupancy):
            return None, None, None

        # Removing impossible attack actions
        if not self.verify_action_range(attack_actions, self.simulated_occupancy):
            return None, None, None

        return expanded_movement_actions, support_actions, attack_actions

    # CREATING UNITS
    def add_unit(self, unit_type, unit_id, owner, q, r, s):
        tile = self.board.get_tile_by_coord(q, r, s)
        if tile is None or tile.unit is not None:
            return False

        # Creating the new unit
        movement, upkeep, strength = UNIT_TYPES[unit_type]
        unit = Unit(unit_id, owner, movement, upkeep, strength)
        self.units[unit_id] = unit

        # Placing the unit on the new position
        self.place_unit(unit, tile)
        return True

    # OBSERVATION ACTIONS
    def observe_unit(self, unit_id):
        unit = self.units[unit_id]
        return self.board.get_tiles_in_range(unit.tile, 3)
    def observe_region(self, region_id):
        return self.board.regions[region_id].tiles

    # UTILITIES
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

            # The path is blocked by not allied unit (if such unit exists)
            if next_tile.unit is not None and next_tile.unit.owner is not unit2.owner:
                break

            current_tile = next_tile

        # Checking if the last tile is free
        can_escape = current_tile.unit is None

        # If there's no space to fall back, the unit dies
        if not can_escape:
            unit2.alive = False
            return True

        # Moving to the back
        for unit in reversed(chain):
            old_tile = unit.tile

            new_tile = self.board.get_tile_by_coord(
                old_tile.q + dq,
                old_tile.r + dr,
                old_tile.s + ds
            )

            self.place_unit(unit, new_tile)
        return True
    def place_unit(self, unit, tile):
        # We remove the old tile
        if unit.tile is not None:
            unit.tile.unit = None
            self.occupancy.pop((unit.tile.q, unit.tile.r, unit.tile.s), None)

        # We place the unit on the new tile
        unit.tile = tile
        if tile is not None:
            tile.unit = unit
            self.occupancy[(tile.q, tile.r, tile.s)] = unit