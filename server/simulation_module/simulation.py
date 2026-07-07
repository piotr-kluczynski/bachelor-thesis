import random
from enum import Enum

from simulation_module.board import Board
from simulation_module.unit import Unit
from simulation_module.action import ActionType
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
    def __init__(self, players, max_round, upkeep_round, tiles, regions):
        self.players = players
        self.players_status = {player: PlayerStatus.ACTIVE for player in players}

        self.players_actions = {}
        self.executed_actions = []

        self.units = {}
        self.occupancy = {}
        self.board = Board(tiles, regions)

        self.round = 1
        self.max_round = max_round
        self.upkeep_round = upkeep_round

        self.type_counters = {unit_type: 0 for unit_type in UNIT_TYPES}

        self.round_updates = []

    # TURN MANAGEMENT
    def start_round(self, new_units=None):
        # Clearing the array of the updates to the game state that happen during this round
        self.round_updates = []

        self.round += 1
        if self.round > self.max_round:
            return False

        if new_units is None:
            new_units = { player: [] for player in self.players }

        for player in self.players:
            owned_regions = self.board.get_owned_regions(player)
            owned_units = [units for units in self.units.values() if units.owner == player]

            # Checking if player regained control over some region
            if self.players_status[player] == PlayerStatus.EXILED and len(owned_regions) > 0:
                self.players_status[player] = PlayerStatus.ACTIVE

                # Registering the status change
                self.record_update("player_status_change", player=player, new_status="Active")

            # Checking if player should automatically lose the game
            if len(owned_regions) == 0 and len(owned_units) == 0:
                self.players_status[player] = PlayerStatus.LOST

                # Registering the status change
                self.record_update("player_status_change", player=player, new_status="Lost")


        # If the round is the upkeep round
        if self.round % self.upkeep_round == 0:

            # Recruiting/Disbanding units
            income = self.calculate_supplies()

            for player in self.players:
                score = income[player]
                if score > 0:
                    self.recruit_units(player, score, new_units.get(player, []))
                elif score < 0:
                    self.disband_units(player, score)

            # Checking if any player status should change
            for player, player_status in self.players_status.items():
                owned_regions = self.board.get_owned_regions(player)

                if len(owned_regions) == 0:
                    if player_status == PlayerStatus.ACTIVE:
                        self.players_status[player] = PlayerStatus.EXILED

                        # Registering the status change
                        self.record_update("player_status_change", player=player, new_status="Exiled")


                    elif player_status == PlayerStatus.EXILED:
                        self.players_status[player] = PlayerStatus.LOST

                        # Registering the status change
                        self.record_update("player_status_change", player=player, new_status="Lost")

                        # Killing off all units from the finished player
                        for _, unit in self.units.items():
                            if unit.owner == player:
                                unit.alive = False

                                self.record_update("unit_death", unit_id=unit.unit_id)
        return True
    def end_round(self):
        self.execute_players_actions()
        self.players_actions = {}
        self.executed_actions = []

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

        # Checking if any region should change ownership
        for region_id, region in self.board.regions.items():
            q, r, s = region.command_centre
            command_centre = self.board.get_tile_by_coord(q, r, s)

            if command_centre.unit is not None:
                unit_owner = command_centre.unit.owner
                region_owner = region.owner

                if unit_owner != region_owner:
                    region.owner = unit_owner

                    # Registering the ownership change
                    self.record_update("region_owner_change", region_id=region.region_id, new_owner=unit_owner)

    # PROCESSING PLAYER ACTIONS
    def add_player_actions(self, player, action_list):
        movement_actions, support_actions, attack_actions = self.process_action_list(player, action_list)
        if movement_actions is None:
            return False

        self.players_actions[player] = (movement_actions, support_actions, attack_actions)
        return True
    def execute_action(self, action):
        unit = self.units[action.unit_id]

        if action.unit_action == ActionType.HOLD:
            return True

        if action.unit_action == ActionType.MOVE:
            q, r, s = action.move_vec
            return self.move_unit(unit, q, r, s)

        target_unit = self.units[action.target_id]

        if action.unit_action == ActionType.ATTACK:
            return self.attack_unit(unit, target_unit)

        if action.unit_action == ActionType.SUPPORT:
            return self.support_unit(unit, target_unit)

        return False
    def execute_players_actions(self):
        # Choosing random order of players
        player_order = random.sample(self.players, len(self.players))

        # Creating global order of player actions
        all_movement_orders = []
        all_support_orders = []
        all_attack_orders = []
        for player_id in player_order:
            # We skip the player if they didn't add any actions
            if player_id not in self.players_actions:
                continue

            movement_actions, support_actions, attack_actions = self.players_actions[player_id]

            all_movement_orders.extend(movement_actions)
            all_support_orders.extend(support_actions)
            all_attack_orders.extend(attack_actions)

        all_actions = all_movement_orders + all_support_orders + all_attack_orders
        for action in all_actions:
            if self.execute_action(action):
                self.executed_actions.append(action)

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

    def process_action_list(self, player, action_list):
        # Check if every unit received up to 1 action
        if not self.verify_action_uniqueness(action_list):
            return None, None, None

        # Check if every ordered unit is owned by the player
        if not self.verify_unit_ownership(player, action_list):
            return None, None, None

        # Divide actions into categories: Movement, Support, Attack
        movement_actions, support_actions, attack_actions = self.split_actions(action_list)

        return movement_actions, support_actions, attack_actions

    # CREATING UNITS
    def add_unit(self, unit_type, owner, q, r, s):
        tile = self.board.get_tile_by_coord(q, r, s)
        if tile is None or tile.unit is not None:
            return False

        # Creating the new unit
        movement, upkeep, strength = UNIT_TYPES[unit_type]
        unit_id = f"{unit_type}_{self.type_counters[unit_type]}"
        unit = Unit(unit_id, owner, movement, upkeep, strength)
        self.units[unit_id] = unit

        # Registering new unit
        self.record_update("unit_spawn", unit_type=unit_type, unit_id=unit_id, owner=owner, q=q, r=r, s=s)

        # Placing the unit on the new position
        self.place_unit(unit, tile)

        self.type_counters[unit_type] += 1
        return True

    # UNIT ACTIONS
    def move_unit(self, unit, dq, dr, ds):
        # Checking if unit has any movement left
        if unit.movement_left < 1:
            return False

        # Check if the target tile exists
        current_tile = unit.tile

        new_q = current_tile.q + dq
        new_r = current_tile.r + dr
        new_s = current_tile.s + ds

        target_tile = self.board.get_tile_by_coord(new_q, new_r, new_s)
        if target_tile is None:
            return False

        # Check if the target tile isn't already occupied
        if target_tile.unit is not None:
            return False

        # Move unit to the target tile
        target_tile.unit = unit
        unit.movement_left -= 1

        unit.tile = target_tile
        current_tile.unit = None

        # Registering the unit movement
        self.record_update("unit_move", unit_id=unit.unit_id, new_q=new_q, new_r=new_r, new_s=new_s)

        return True
    def attack_unit(self, unit1, unit2):
        tile1 = unit1.tile
        tile2 = unit2.tile

        if calc_distance(tile1.q, tile1.r, tile1.s, tile2.q, tile2.r, tile2.s) > 1:
            return False

        if not unit2.alive:
            return False

        attack_power = random.randint(1, unit1.strength) + 2 * len(unit1.supporting_units)
        defend_power = random.randint(1, unit2.strength) + 2 * len(unit2.supporting_units)

        if defend_power >= attack_power:
            # Defenders stand their ground
            return True
        else:
            if 2*defend_power <= attack_power:
                # Defenders are completely destroyed
                unit2.alive = False
                self.record_update("unit_death", unit_id=unit2.unit_id)
                return True

            unit2_old_tile = unit2.tile

            # Defenders were defeated and fall back
            self.push_chain(unit1, unit2)

            # Attacker advances in the created free spot
            self.place_unit(unit1, unit2_old_tile)

            # Registering the unit movement
            self.record_update("unit_move", unit_id=unit1.unit_id, new_q=unit2_old_tile.q, new_r=unit2_old_tile.r, new_s=unit2_old_tile.s)

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
            self.record_update("unit_death", unit_id=unit2.unit_id)
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

            # Registering the unit movement
            self.record_update("unit_move", unit_id=unit.unit_id, new_q=old_tile.q + dq, new_r=old_tile.r + dr, new_s=old_tile.s + ds)
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
    def calculate_supplies(self):
        income = {player: 0 for player in self.players}

        # We add supply value of each controlled region
        for region in self.board.regions.values():
            if region.owner is not None:
                income[region.owner] += region.region_upkeep

        # We detract value of each controlled unit
        for unit in self.units.values():
            income[unit.owner] -= unit.upkeep

        return income
    def recruit_units(self, player, budget, unit_requests):
        for unit_type, region in zip(unit_requests, self.board.get_owned_regions(player)):
            cost = UNIT_TYPES[unit_type][1]

            if budget < cost:
                break

            q, r, s = region.command_centre
            if self.add_unit(unit_type, player, q, r, s):
                budget -= cost
    def disband_units(self, player, deficit):
        units_to_remove = []

        for unit in list(self.units.values()):
            if deficit >= 0:
                break

            if unit.owner == player:
                deficit += unit.upkeep
                units_to_remove.append(unit)

        for unit in units_to_remove:
            self.place_unit(unit, None)
            unit.alive = False
            self.record_update("unit_death", unit_id=unit.unit_id)
            del self.units[unit.unit_id]
    def record_update(self, update_type, **kwargs):
        self.round_updates.append({"type": update_type, **kwargs})
