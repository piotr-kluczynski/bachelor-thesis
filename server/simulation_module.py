import random
from collections import deque

HEX_DIRECTIONS = [
    (1, -1, 0),
    (1, 0, -1),
    (0, 1, -1),
    (-1, 1, 0),
    (-1, 0, 1),
    (0, -1, 1)
]

class Simulation:
    def __init__(self, players):
        self.players = players

        self.players_actions = {}
        self.units = {}
        self.occupancy = {}
        self.board = Board()

        self.new_unit_id = 0

    # TURN MANAGEMENT
    def end_round(self):
        self.occupancy = {}

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
    def add_player_actions(self, player, action_list):
        movement_actions, support_actions, attack_actions = self.process_action_list(player, action_list)
        if movement_actions is None:
            return False

        self.players_actions[player] = (movement_actions, support_actions, attack_actions)
        return True
    def execute_action(self, action):
        unit = self.units[action.unit_id]

        if action.unit_action == "Hold":
            return True

        if action.unit_action == "Move":
            q, r, s = action.move_vec
            return self.move_unit(unit, q, r, s)

        target_unit = self.units[action.target_id]

        if action.unit_action == "Attack":
            return self.attack_unit(unit, target_unit)

        if action.unit_action == "Support":
            return self.support_unit(unit, target_unit)

        return False
    def execute_player_actions(self):
        # Choosing random order of players
        player_order = [i for i in range(len(self.players))]
        random.shuffle(player_order)

        # Creating global order of player actions
        all_movement_orders = []
        all_support_orders = []
        all_attack_orders = []
        for player_id in player_order:
            movement_actions, support_actions, attack_actions = self.players_actions[player_id]

            all_movement_orders.append(movement_actions)
            all_support_orders.append(support_actions)
            all_attack_orders.append(attack_actions)

        all_actions = all_movement_orders + all_support_orders + all_attack_orders
        for action in all_actions:
            self.execute_action(action)

    def expand_movement_actions(self, action_list):
        result = []
        moved_units = {}
        simulated_occupancy = self.occupancy.copy()

        for action in action_list:
            dq, dr, ds = action.move_vec
            unit = self.units[action.unit_id]
            unit_tile = unit.tile
            target_tile = self.board.get_tile_by_coord(unit_tile.q + dq, unit_tile.r + dr, unit_tile.s + ds)

            path = self.board.find_shortest_path(unit_tile, target_tile, unit.movement_left, simulated_occupancy)

            if path is None:
                return False

            for i in range(0, len(path)-1):
                move_vec = (path[i+1].q - path[i].q, path[i+1].r - path[i].r, path[i+1].s - path[i].s)
                result.append(Action("Move", action.unit_id, move_vec=move_vec))

            # Update simulated occupancy
            del simulated_occupancy[(unit_tile.q, unit_tile.r, unit_tile.s)]
            simulated_occupancy[(target_tile.q, target_tile.r, target_tile.s)] = unit

            # Register moved unit to check later
            moved_units[action.unit_id] = target_tile
        return result, moved_units
    def split_actions(self, action_list):
        movement_actions = []
        support_actions = []
        attack_actions = []

        for action in action_list:
            if action.unit_action == "Move":
                movement_actions.append(action)
            elif action.unit_action == "Support":
                support_actions.append(action)
            elif action.unit_action == "Attack":
                attack_actions.append(action)

        return movement_actions, support_actions, attack_actions

    def verify_action_uniqueness(self, action_list):
        units_id = set()
        for action in action_list:
            if action.unit_id in units_id:
                return False
            else:
                units_id.add(action.unit_id)
        return True
    def verify_unit_ownership(self, player, action_list):
        for action in action_list:
            unit = self.units[action.unit_id]
            if unit.owner != player:
                return False

        return True
    def verify_action_range(self, action_list, moved_units):
        for action in action_list:
            unit_tile = self.units[action.unit_id].tile
            if action.target_id in moved_units.keys():
                target_tile = moved_units[action.target_id]
            else:
                target_tile = self.units[action.target_id].tile

            if calc_distance(unit_tile.q, unit_tile.r, unit_tile.s, target_tile.q, target_tile.r, target_tile.s) > 1:
                return False
        return True

    def process_action_list(self, player, action_list):
        # Check if every unit received up to 1 action
        if not self.verify_action_uniqueness(action_list):
            return False

        # Check if every ordered unit is owned by the player
        if not self.verify_unit_ownership(player, action_list):
            return False

        # Divide actions into categories: Movement, Support, Attack
        movement_actions, support_actions, attack_actions = self.split_actions(action_list)

        # Expand movement actions into separate moves
        expanded_movement_actions, moved_units = self.expand_movement_actions(movement_actions)
        if expanded_movement_actions is False:
            return False

        # Removing impossible support actions
        if not self.verify_action_range(support_actions, moved_units):
            return False

        # Removing impossible attack actions
        if not self.verify_action_range(attack_actions, moved_units):
            return False

        return expanded_movement_actions, support_actions, attack_actions

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

        light_infantry = Unit(self.new_unit_id, owner, 2, 1, 6)
        tile.unit = light_infantry
        light_infantry.tile = tile

        self.units.update({self.new_unit_id: light_infantry})
        self.new_unit_id += 1

        # Adding to the occupancy new unit
        self.occupancy[(tile.q, tile.r, tile.s)] = light_infantry

        return True
    def add_heavy_infantry(self, owner, q, r, s):
        tile = self.board.get_tile_by_coord(q, r, s)

        if tile.unit is not None:
            return False

        heavy_infantry = Unit(self.new_unit_id, owner, 1, 2, 8)
        tile.unit = heavy_infantry
        heavy_infantry.tile = tile

        self.units.update({self.new_unit_id: heavy_infantry})
        self.new_unit_id += 1

        # Adding to the occupancy new unit
        self.occupancy[(tile.q, tile.r, tile.s)] = heavy_infantry

        return True
    def add_cavalry(self, owner, q, r, s):
        tile = self.board.get_tile_by_coord(q, r, s)

        if tile.unit is not None:
            return False

        cavalry = Unit(self.new_unit_id, owner, 3, 3, 6)
        tile.unit = cavalry
        cavalry.tile = tile

        self.units.update({self.new_unit_id: cavalry})
        self.new_unit_id += 1

        # Adding to the occupancy new unit
        self.occupancy[(tile.q, tile.r, tile.s)] = cavalry

        return True

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


class Action:
    def __init__(self, unit_action, unit_id, target_id=None, move_vec=None):
        self.unit_action = unit_action
        self.unit_id = unit_id
        self.target_id = target_id
        self.move_vec = move_vec

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

class Tile:
    def __init__(self, q, r, s):
        self.q = q
        self.r = r
        self.s = s
        self.unit = None

class Board:
    def __init__(self, tiles=None):
        if tiles is None:
            tiles = {}
        self.tiles = tiles

    def get_tile_by_coord(self, q, r, s):
        if q + r + s != 0:
            return None

        return self.tiles.get((q, r, s))

    def get_tiles_in_range(self, center_tile, radius):
        results = []

        for dq in range(-radius, radius + 1):
            for dr in range(max(-radius, -dq - radius), min(radius, -dq + radius) + 1):
                ds = -dq - dr

                results.append(self.tiles.get((center_tile.q + dq, center_tile.r + dr, center_tile.s + ds)))
        return results

    def get_neighbours(self, tile):
        results = []

        for dq, dr, ds in HEX_DIRECTIONS:
            neighbour = self.tiles.get((
                tile.q + dq,
                tile.r + dr,
                tile.s + ds
            ))

            if neighbour is not None:
                results.append(neighbour)
        return results

    def find_shortest_path(self, start_tile, end_tile, max_distance, occupancy):
        if calc_distance(start_tile.q, start_tile.r, start_tile.s, end_tile.q, end_tile.r, end_tile.s) > max_distance:
            return None

        queue = deque([start_tile])
        visited = {start_tile}
        came_from = {}
        distance = {
            start_tile: 0,
        }

        while queue:
            current = queue.popleft()

            if current == end_tile:
                break

            for neighbour in self.get_neighbours(current):
                if occupancy.get((neighbour.q, neighbour.r, neighbour.s)) is not None:
                    continue

                if neighbour in visited:
                    continue

                new_distance = distance[current] + 1
                if new_distance > max_distance:
                    continue

                visited.add(neighbour)
                distance[neighbour] = new_distance
                came_from[neighbour] = current

                queue.append(neighbour)

        if end_tile not in came_from and end_tile != start_tile:
            return None

        path = [end_tile]
        current = end_tile
        while current != start_tile:
            current = came_from[current]
            path.append(current)

        path.reverse()
        return path


def calc_distance(q_1, r_1, s_1, q_2, r_2, s_2):
    return (abs(q_1 - q_2) + abs(r_1 - r_2) + abs(s_1 - s_2)) / 2