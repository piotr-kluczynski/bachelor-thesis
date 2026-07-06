import random
import unittest

from simulation_module.action import Action, ActionType
from simulation_module.region import Region
from simulation_module.simulation import Simulation, UNIT_TYPES, PlayerStatus
from simulation_module.tile import Tile
from simulation_module.unit import Unit

class TestPlacingUnits(unittest.TestCase):
    def setUp(self):
        pass

    def test_place_unit_sets_tile(self):
        simulation = prepare_simulation()

        # We add unit to place on different tile
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )

        unit = simulation.board.get_tile_by_coord(0, 0, 0).unit
        tile = simulation.board.get_tile_by_coord(0, -1, 1)

        simulation.place_unit(unit, tile)
        results = (
            unit.tile == tile, # Unit
            tile.unit == unit, # Tile
            simulation.occupancy[(tile.q, tile.r, tile.s)] == unit # Occupancy
        )

        self.assertEqual(results, (True, True, True))
    def test_place_unit_clears_old_tile(self):
        simulation = prepare_simulation()

        # We add unit to place on different tile
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )

        unit = simulation.board.get_tile_by_coord(0, 0, 0).unit
        tile = simulation.board.get_tile_by_coord(0, -1, 1)

        simulation.place_unit(unit, tile)
        results = (
            simulation.board.get_tile_by_coord(0, 0, 0).unit is None,
            (0, 0, 0) not in simulation.occupancy.keys()
        )

        self.assertEqual(results, (True, True))

class TestAddingUnits(unittest.TestCase):
    def test_add_unit_valid(self):
        simulation = prepare_simulation()

        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )

        self.assertIsInstance(simulation.units["light_infantry_0"], Unit)
    def test_add_unit_occupied_tile(self):
        simulation = prepare_simulation()

        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )

        # We try to add another unit on the same tile
        result = simulation.add_unit(
            "heavy_infantry",
            simulation.players[1],
            0, 0, 0
        )

        self.assertFalse(result)
    def test_add_unit_invalid_coord(self):
        simulation = prepare_simulation()

        result = simulation.add_unit(
            UNIT_TYPES["light_infantry"],
            simulation.players[0],
            -1, -1, 1
        )

        self.assertFalse(result)
    def test_add_unit_all_types(self):
        simulation = prepare_simulation()

        tiles = random.sample(list(simulation.board.tiles.values()), len(UNIT_TYPES))

        results = []
        expected = [True for _ in range(len(UNIT_TYPES))]

        for tile, unit_type in zip(tiles, UNIT_TYPES):
            results.append(
                simulation.add_unit(
                    unit_type,
                    random.choice(simulation.players),
                    tile.q, tile.r, tile.s
                )
            )

        self.assertEqual(results, expected)
    def test_add_unit_increments_id(self):
        simulation = prepare_simulation()

        # Creating one unit of each type
        tiles = random.sample(list(simulation.board.tiles.values()), len(UNIT_TYPES))

        results = []
        expected = [True for _ in range(len(UNIT_TYPES))]

        for tile, unit_type in zip(tiles, UNIT_TYPES):
            results.append(
                simulation.add_unit(
                    unit_type,
                    random.choice(simulation.players),
                    tile.q, tile.r, tile.s
                )
            )
        self.assertEqual(results, expected)

class TestMovementAction(unittest.TestCase):
    def test_move_unit_valid(self):
        simulation = prepare_simulation()

        # Adding unit to test movement on
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )

        simulation.move_unit(
            simulation.board.get_tile_by_coord(0, 0, 0).unit,
            0, 1, -1
        )

        self.assertIsNotNone(simulation.board.get_tile_by_coord(0, 1, -1).unit)
    def test_move_unit_occupied(self):
        simulation = prepare_simulation()

        # Adding unit to test movement on
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )

        # Adding unit to block the target tile
        simulation.add_unit(
            "cavalry",
            simulation.players[1],
            0, -1,  1
        )

        result = simulation.move_unit(
            simulation.board.get_tile_by_coord(0, 0, 0).unit,
            0, -1, 1
        )

        self.assertFalse(result)
    def test_move_unit_off_board(self):
        simulation = prepare_simulation(radius=1)

        # Adding unit to test movement on
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, -1, 1
        )

        result = simulation.move_unit(
            simulation.board.get_tile_by_coord(0, -1, 1).unit,
            0, -1, 1
        )

        self.assertFalse(result)
    def test_move_unit_depletes_movement(self):
        simulation = prepare_simulation()

        # Adding unit to test movement on
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )

        starting_movement = simulation.board.get_tile_by_coord(0, 0, 0).unit.movement_left

        simulation.move_unit(
            simulation.board.get_tile_by_coord(0, 0, 0).unit,
            0, -1, 1
        )

        ending_movement = simulation.board.get_tile_by_coord(0, -1, 1).unit.movement_left

        self.assertNotEqual(starting_movement, ending_movement)
    def test_move_unit_no_movement_left(self):
        simulation = prepare_simulation()

        # Adding unit to test movement on
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )

        # Setting the movement to 0
        simulation.board.get_tile_by_coord(0, 0, 0).unit.movement_left = 0

        result = simulation.move_unit(
            simulation.board.get_tile_by_coord(0, 0, 0).unit,
            0, -1, 1
        )

        self.assertFalse(result)

class TestAttackAction(unittest.TestCase):
    def test_attack_defender_holds(self):
        simulation = prepare_simulation()

        # Adding attacker unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        attacker = simulation.board.get_tile_by_coord(0, 0, 0).unit
        attacker.strength = 1

        # Adding defender unit
        simulation.add_unit(
            "heavy_infantry",
            simulation.players[1],
            0, -1, 1
        )
        defender = simulation.board.get_tile_by_coord(0, -1, 1).unit
        defender.strength = 8

        simulation.attack_unit(attacker, defender)
        self.assertIsNotNone(simulation.board.get_tile_by_coord(0, 0, 0).unit)
    def test_attack_defender_pushed(self):
        simulation = prepare_simulation()

        # Adding attacker unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        attacker = simulation.board.get_tile_by_coord(0, 0, 0).unit
        attacker.strength = 8

        # Adding defender unit
        simulation.add_unit(
            "heavy_infantry",
            simulation.players[1],
            0, -1, 1
        )
        defender = simulation.board.get_tile_by_coord(0, -1, 1).unit
        defender.strength = 4

        simulation.attack_unit(attacker, defender)
        self.assertEqual(simulation.board.get_tile_by_coord(0, -2, 2).unit, defender)
    def test_attack_defender_destroyed(self):
        simulation = prepare_simulation()

        # Adding attacker unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        attacker = simulation.board.get_tile_by_coord(0, 0, 0).unit
        attacker.strength = 8

        # Adding defender unit
        simulation.add_unit(
            "heavy_infantry",
            simulation.players[1],
            0, -1, 1
        )
        defender = simulation.board.get_tile_by_coord(0, -1, 1).unit
        defender.strength = 1

        defender_id = defender.unit_id

        simulation.attack_unit(attacker, defender)
        self.assertFalse(simulation.units.get(defender_id).alive)
    def test_attack_attacker_advances(self):
        simulation = prepare_simulation()

        # Adding attacker unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        attacker = simulation.board.get_tile_by_coord(0, 0, 0).unit
        attacker.strength = 8

        # Adding defender unit
        simulation.add_unit(
            "heavy_infantry",
            simulation.players[1],
            0, -1, 1
        )
        defender = simulation.board.get_tile_by_coord(0, -1, 1).unit
        defender.strength = 1

        simulation.attack_unit(attacker, defender)
        self.assertEqual(simulation.board.get_tile_by_coord(0, -1, 1).unit, defender)
    def test_attack_out_of_range(self):
        simulation = prepare_simulation()

        # Adding attacker unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        attacker = simulation.board.get_tile_by_coord(0, 0, 0).unit

        # Adding defender unit
        simulation.add_unit(
            "heavy_infantry",
            simulation.players[1],
            0, -2, 2
        )
        defender = simulation.board.get_tile_by_coord(0, -2, 2).unit

        result = simulation.attack_unit(attacker, defender)
        self.assertFalse(result)
    def test_attack_dead_unit(self):
        simulation = prepare_simulation()

        # Adding attacker unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        attacker = simulation.board.get_tile_by_coord(0, 0, 0).unit

        # Adding defender unit
        simulation.add_unit(
            "heavy_infantry",
            simulation.players[1],
            0, -1, 1
        )
        defender = simulation.board.get_tile_by_coord(0, -1, 1).unit
        defender.alive = False

        result = simulation.attack_unit(attacker, defender)
        self.assertFalse(result)

class TestChainPush(unittest.TestCase):
    def test_push_single_unit_free_space(self):
        simulation = prepare_simulation()

        # Adding attacker unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        attacker = simulation.board.get_tile_by_coord(0, 0, 0).unit

        # Adding defender unit
        simulation.add_unit(
            "heavy_infantry",
            simulation.players[1],
            0, -1, 1
        )
        defender = simulation.board.get_tile_by_coord(0, -1, 1).unit

        simulation.push_chain(attacker, defender)
        self.assertEqual(simulation.board.get_tile_by_coord(0, -2, 2).unit, defender)
    def test_push_chain_two_allies(self):
        simulation = prepare_simulation()

        # Adding attacker unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        attacker = simulation.board.get_tile_by_coord(0, 0, 0).unit

        # Adding defender unit
        simulation.add_unit(
            "heavy_infantry",
            simulation.players[1],
            0, -1, 1
        )
        defender = simulation.board.get_tile_by_coord(0, -1, 1).unit

        # Adding another unit behind defender
        simulation.add_unit(
            "cavalry",
            simulation.players[1],
            0, -2, 2
        )
        ally = simulation.board.get_tile_by_coord(0, -2, 2).unit

        simulation.push_chain(attacker, defender)
        self.assertEqual(simulation.board.get_tile_by_coord(0, -3, 3).unit, ally)
    def test_push_unit_against_wall(self):
        simulation = prepare_simulation(radius=1)

        # Adding attacker unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        attacker = simulation.board.get_tile_by_coord(0, 0, 0).unit

        # Adding defender unit
        simulation.add_unit(
            "heavy_infantry",
            simulation.players[1],
            0, -1, 1
        )
        defender = simulation.board.get_tile_by_coord(0, -1, 1).unit

        simulation.push_chain(attacker, defender)
        self.assertFalse(defender.alive)
    def test_push_unit_against_enemy(self):
        simulation = prepare_simulation()

        # Adding attacker unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        attacker = simulation.board.get_tile_by_coord(0, 0, 0).unit

        # Adding defender unit
        simulation.add_unit(
            "heavy_infantry",
            simulation.players[1],
            0, -1, 1
        )
        defender = simulation.board.get_tile_by_coord(0, -1, 1).unit

        # Adding another enemy unit behind
        simulation.add_unit(
            "cavalry",
            simulation.players[0],
            0, -2, 2
        )

        simulation.push_chain(attacker, defender)
        self.assertFalse(defender.alive)

class TestSupportAction(unittest.TestCase):
    def test_support_adds_to_supporting_units(self):
        simulation = prepare_simulation()

        # Adding supporting unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        supporting = simulation.board.get_tile_by_coord(0, 0, 0).unit

        # Adding supported unit
        simulation.add_unit(
            "heavy_infantry",
            simulation.players[0],
            0, -1, 1
        )
        supported = simulation.board.get_tile_by_coord(0, -1, 1).unit

        simulation.support_unit(supporting, supported)
        self.assertIn(supporting, supported.supporting_units)
    def test_support_out_of_range(self):
        simulation = prepare_simulation()

        # Adding supporting unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        supporting = simulation.board.get_tile_by_coord(0, 0, 0).unit

        # Adding supported unit
        simulation.add_unit(
            "heavy_infantry",
            simulation.players[0],
            0, -2, 2
        )
        supported = simulation.board.get_tile_by_coord(0, -2, 2).unit

        result = simulation.support_unit(supporting, supported)
        self.assertFalse(result)
    def test_support_dead_unit(self):
        simulation = prepare_simulation()

        # Adding supporting unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        supporting = simulation.board.get_tile_by_coord(0, 0, 0).unit

        # Adding supported unit
        simulation.add_unit(
            "heavy_infantry",
            simulation.players[0],
            0, -1, 1
        )
        supported = simulation.board.get_tile_by_coord(0, -1, 1).unit
        supported.alive = False

        result = simulation.support_unit(supporting, supported)
        self.assertFalse(result)

class TestBoardOperations(unittest.TestCase):
    def test_get_tile_invalid_coords(self):
        simulation = prepare_simulation()

        result = simulation.board.get_tile_by_coord(3, -1, -1)
        self.assertIsNone(result)
    def test_get_neighbour_center(self):
        simulation = prepare_simulation()

        tile = simulation.board.get_tile_by_coord(0, 0, 0)
        neighbours = simulation.board.get_neighbours(tile)

        self.assertIsNotNone(len(neighbours), 6)
    def test_get_neighbours_edge(self):
        simulation = prepare_simulation(radius=1)

        tile = simulation.board.get_tile_by_coord(0, -1, 1)
        neighbours = simulation.board.get_neighbours(tile)

        self.assertLess(len(neighbours), 6)
    def test_get_tiles_in_range_no_nones(self):
        simulation = prepare_simulation(radius=1)

        center_tile = simulation.board.get_tile_by_coord(0, 0, 0)
        tiles = simulation.board.get_tiles_in_range(center_tile=center_tile, radius=3)

        self.assertNotIn(None, tiles)
    def test_find_shortest_path_direct(self):
        simulation = prepare_simulation()

        start_tile = simulation.board.get_tile_by_coord(0, 0, 0)
        end_tile = simulation.board.get_tile_by_coord(0, -1, 1)
        occupancy = simulation.occupancy

        path = simulation.board.find_shortest_path(start_tile, end_tile, max_distance=3, occupancy=occupancy)
        self.assertEqual(len(path), 2)
    def test_find_shortest_path_blocked(self):
        simulation = prepare_simulation()

        # We add unit to block path
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, -1, 1
        )
        occupied_tile = simulation.board.get_tile_by_coord(0, -1, 1)

        start_tile = simulation.board.get_tile_by_coord(0, 0, 0)
        end_tile = simulation.board.get_tile_by_coord(0, -2, 2)
        occupancy = simulation.occupancy

        path = simulation.board.find_shortest_path(start_tile, end_tile, max_distance=10, occupancy=occupancy)
        self.assertNotIn(occupied_tile, path)
    def test_find_shortest_path_too_far(self):
        simulation = prepare_simulation(radius=5)

        start_tile = simulation.board.get_tile_by_coord(0, 0, 0)
        end_tile = simulation.board.get_tile_by_coord(0, -5, 5)
        occupancy = simulation.occupancy

        path = simulation.board.find_shortest_path(start_tile, end_tile, max_distance=3, occupancy=occupancy)
        self.assertIsNone(path)

class TestActionVerification(unittest.TestCase):
    def test_duplicate_action_rejected(self):
        simulation = prepare_simulation()

        # We add unit to give orders to
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        unit = simulation.board.get_tile_by_coord(0, 0, 0).unit

        # We add 2 movement orders to the same unit
        player_actions = [
            Action(
                ActionType.MOVE,
                unit.unit_id,
                move_vec=(0, -1, 1)
            ),
            Action(
                ActionType.MOVE,
                unit.unit_id,
                move_vec=(1, 0, -1)
            )
        ]

        result = simulation.verify_action_uniqueness(player_actions)
        self.assertFalse(result)
    def test_unowned_unit_rejected(self):
        simulation = prepare_simulation()

        # We add unit to give orders to
        simulation.add_unit(
            "light_infantry",
            simulation.players[1],
            0, 0, 0
        )
        unit = simulation.board.get_tile_by_coord(0, 0, 0).unit

        # We add movement order for the unit
        player = simulation.players[0]

        player_actions = [
            Action(
                ActionType.MOVE,
                unit.unit_id,
                move_vec=(0, -1, 1)
            )
        ]

        result = simulation.verify_unit_ownership(player, player_actions)
        self.assertFalse(result)
    def test_out_of_range_rejected(self):
        simulation = prepare_simulation()

        # We add supporting unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[1],
            0, 0, 0
        )
        supporting = simulation.board.get_tile_by_coord(0, 0, 0).unit

        # We add supporting unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[1],
            -1, 2, -1
        )
        supported = simulation.board.get_tile_by_coord(-1, 2, -1).unit

        # We add support order to the unit
        player_actions = [
            Action(
                ActionType.SUPPORT,
                supporting.unit_id,
                target_id=supported.unit_id,
            )
        ]

        result = simulation.verify_action_range(player_actions, simulation.occupancy)
        self.assertFalse(result)
    def test_two_units_same_destination_rejected(self):
        simulation = prepare_simulation()

        # We add first moving unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[1],
            0, 0, 0
        )
        unit1 = simulation.board.get_tile_by_coord(0, 0, 0).unit

        # We add second moving unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[1],
            1, 0, -1
        )
        unit2 = simulation.board.get_tile_by_coord(1, 0, -1).unit

        # We add movement orders
        player_actions = [
            Action(
                ActionType.MOVE,
                unit1.unit_id,
                move_vec=(1, -1, 0)
            ),
            Action(
                ActionType.MOVE,
                unit2.unit_id,
                move_vec=(0, -1, 1)
            )
        ]

        player = simulation.players[1]

        result = simulation.add_player_actions(player, player_actions)
        self.assertFalse(result)

class TestObservationAction(unittest.TestCase):
    def test_observe_unit_sees_full_range(self):
        simulation = prepare_simulation()

        # We add unit to give orders to
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        unit = simulation.board.get_tile_by_coord(0, 0, 0).unit

        view = simulation.observe_unit(unit.unit_id)
        self.assertEqual(len(view), 37)
    def test_observe_unit_sees_limited_range(self):
        simulation = prepare_simulation(radius=2)

        # We add unit to give orders to
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        unit = simulation.board.get_tile_by_coord(0, 0, 0).unit

        view = simulation.observe_unit(unit.unit_id)
        self.assertEqual(len(view), 19)
    def test_observe_unit_sees_units(self):
        simulation = prepare_simulation(radius=2)

        # We add unit to give orders to
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        unit = simulation.board.get_tile_by_coord(0, 0, 0).unit

        # We add other unit to be observed
        simulation.add_unit(
            "light_infantry",
            simulation.players[1],
            -2, 1, 1
        )
        observed_unit = simulation.board.get_tile_by_coord(-2, 1, 1).unit

        view = simulation.observe_unit(unit.unit_id)
        observed_units = [tile.unit for tile in view if tile.unit is not None]

        self.assertIn(observed_unit, observed_units)
    def test_observe_region_sees_full_range(self):
        simulation = prepare_simulation(radius=1)

        region = simulation.board.regions.get("Dalaran")

        view = simulation.observe_region(region.region_id)
        self.assertEqual(len(view), 7)
    def test_observe_region_sees_units(self):
        simulation = prepare_simulation(radius=2)

        # We add other unit to be observed
        simulation.add_unit(
            "light_infantry",
            simulation.players[1],
            -2, 1, 1
        )
        observed_unit = simulation.board.get_tile_by_coord(-2, 1, 1).unit

        view = simulation.observe_region("Dalaran")
        observed_units = [tile.unit for tile in view.values() if tile.unit is not None]

        self.assertIn(observed_unit, observed_units)

class TestStartingRound(unittest.TestCase):
    def test_start_round_max_round(self):
        simulation = prepare_simulation(max_round=0)

        new_units = { player_name : [] for player_name in simulation.players }

        result = simulation.start_round(new_units)
        self.assertFalse(result)
    def test_start_round_spawns_units(self):
        simulation = prepare_simulation(upkeep_round=1)

        # We set the owner of the region to the first player
        simulation.board.regions["Dalaran"].owner = simulation.players[0]

        # We create player order for one new unit
        new_units = { player_name : [] for player_name in simulation.players }
        new_units[simulation.players[0]].append("light_infantry")

        # Start new round with the new_units order
        simulation.start_round(new_units)

        self.assertIsNotNone(simulation.board.get_tile_by_coord(0, 0, 0).unit)
    def test_start_round_disbands_unit(self):
        simulation = prepare_simulation(upkeep_round=1)

        # We create new unit to disband
        simulation.add_unit(
            "cavalry",
            simulation.players[1],
            1, 0, -1
        )
        unit = simulation.board.get_tile_by_coord(1, 0, -1)

        new_units = { player_name : [] for player_name in simulation.players }

        simulation.start_round(new_units)
        self.assertNotIn(unit, simulation.units.values())
    def test_start_round_non_upkeep(self):
        simulation = prepare_simulation()

        # We set the owner of the region to the first player
        simulation.board.regions["Dalaran"].owner = simulation.players[0]

        # We create new unit (which will be kept even though player 1 can't afford it)
        simulation.add_unit(
            "cavalry",
            simulation.players[1],
            1, 0, -1
        )
        unit = simulation.board.get_tile_by_coord(1, 0, -1).unit

        # We create player order for one new unit (which shouldn't go through)
        new_units = {player_name: [] for player_name in simulation.players}
        new_units[simulation.players[0]].append("light_infantry")

        simulation.start_round(new_units)

        result = (
            unit.alive,
            True if simulation.board.get_tile_by_coord(0, 0, 0).unit is None else False,
        )

        self.assertEqual(result, (True, True))
    def test_start_round_units_marked_dead(self):
        simulation = prepare_simulation(upkeep_round=1)

        simulation.add_unit(
            "cavalry",
            simulation.players[0],
            0, 0, 0
        )
        unit = simulation.board.get_tile_by_coord(0, 0, 0).unit

        # We set the player status to EXILED
        player = simulation.players[0]
        simulation.players_status[player] = PlayerStatus.EXILED

        new_units = {player_name: [] for player_name in simulation.players}
        simulation.start_round(new_units)

        self.assertFalse(unit.alive)

class TestEndingRound(unittest.TestCase):
    def test_end_round_clears_dead_units(self):
        simulation = prepare_simulation()

        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        unit = simulation.board.get_tile_by_coord(0, 0, 0)
        unit.alive = False

        simulation.end_round()
        self.assertNotIn(unit, simulation.units.values())
    def test_end_round_resets_movement(self):
        simulation = prepare_simulation()

        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        unit = simulation.board.get_tile_by_coord(0, 0, 0).unit
        unit.movement_left = 0

        simulation.end_round()
        self.assertEqual(unit.movement_left, unit.movement)
    def test_end_round_clears_supports(self):
        simulation = prepare_simulation()

        # We add supporting unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        supporting = simulation.board.get_tile_by_coord(0, 0, 0).unit

        # We add supported unit
        simulation.add_unit(
            "heavy_infantry",
            simulation.players[0],
            -1, 0, 1
        )
        supported = simulation.board.get_tile_by_coord(-1, 0, 1).unit

        simulation.support_unit(supporting, supported)

        simulation.end_round()
        self.assertEqual([], supported.supporting_units)
    def test_end_round_changes_region_owner(self):
        simulation = prepare_simulation()

        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )

        # We set region owner to the second player
        simulation.board.regions["Dalaran"].owner = simulation.players[1]

        simulation.end_round()
        self.assertEqual(simulation.board.regions["Dalaran"].owner, simulation.players[0])

class TestPlayerStatusChange(unittest.TestCase):
    def test_status_change_active_to_lost(self):
        simulation = prepare_simulation()

        # We set the owner of the region to the first player
        simulation.board.regions["Dalaran"].owner = simulation.players[0]

        # We create player order for one new unit
        new_units = { player_name : [] for player_name in simulation.players }

        # Start new round with the new_units order
        simulation.start_round(new_units)

        player = simulation.players[1]
        self.assertEqual(simulation.players_status[player], PlayerStatus.LOST)
    def test_status_change_active_to_exiled(self):
        simulation = prepare_simulation(upkeep_round=1)

        # We set the owner of the region to the first player
        simulation.board.regions["Dalaran"].owner = simulation.players[0]

        # We create player order for one new unit
        new_units = {player_name: [] for player_name in simulation.players}

        # Adding unit to the second player
        simulation.add_unit(
            "light_infantry",
            simulation.players[1],
            0, 1, -1
        )

        # Start new round with the new_units order
        simulation.start_round(new_units)

        player = simulation.players[1]
        self.assertEqual(simulation.players_status[player], PlayerStatus.EXILED)
    def test_status_change_exiled_to_lost(self):
        simulation = prepare_simulation(upkeep_round=1)

        # We set the owner of the region to the first player
        simulation.board.regions["Dalaran"].owner = simulation.players[0]

        # We create player order for one new unit
        new_units = {player_name: [] for player_name in simulation.players}

        # Adding unit to the second player
        simulation.add_unit(
            "light_infantry",
            simulation.players[1],
            0, 1, -1
        )

        player = simulation.players[1]
        simulation.players_status[player] = PlayerStatus.EXILED

        # Start new round with the new_units order
        simulation.start_round(new_units)

        self.assertEqual(simulation.players_status[player], PlayerStatus.LOST)
    def test_status_change_exiled_to_active(self):
        simulation = prepare_simulation()

        # We set the owner of the region to the first player
        simulation.board.regions["Dalaran"].owner = simulation.players[1]

        # We create player order for one new unit
        new_units = {player_name: [] for player_name in simulation.players}

        # Adding unit to the second player
        simulation.add_unit(
            "light_infantry",
            simulation.players[1],
            0, 0, 0
        )

        player = simulation.players[1]
        simulation.players_status[player] = PlayerStatus.EXILED

        # Start new round with the new_units order
        simulation.start_round(new_units)

        self.assertEqual(simulation.players_status[player], PlayerStatus.ACTIVE)

class TestEndToEnd(unittest.TestCase):
    def test_few_turns(self):
        simulation = prepare_simulation()
        playerA = simulation.players[0]
        playerB = simulation.players[1]

        simulation.board.regions["Dalaran"].owner = simulation.players[0]

        # Creating initial armies for both players
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, 0, 0
        )
        unitA_1 = simulation.board.get_tile_by_coord(0, 0, 0).unit
        simulation.add_unit(
            "light_infantry",
            simulation.players[0],
            0, -1, 1
        )
        unitA_2 = simulation.board.get_tile_by_coord(0, -1, 1).unit

        simulation.add_unit(
            "heavy_infantry",
            simulation.players[1],
            -1, 2, -1
        )
        unitB_1 = simulation.board.get_tile_by_coord(-1, 2, -1).unit

        simulation.add_unit(
            "cavalry",
            simulation.players[1],
            0, 3, -3
        )
        unitB_2 = simulation.board.get_tile_by_coord(0, 3, -3).unit

        simulation.add_unit(
            "light_infantry",
            simulation.players[1],
            2, 0, -2
        )
        unitB_3 = simulation.board.get_tile_by_coord(2, 0, -2).unit

        # Players give orders
        actions_A = [
            Action(
              ActionType.HOLD,
                unitA_1.unit_id
            ),
            Action(
                ActionType.SUPPORT,
                unitA_2.unit_id,
                target_id=unitA_1.unit_id
            )
        ]
        simulation.add_player_actions(playerA, actions_A)

        actions_B = [
            Action(
                ActionType.MOVE,
                unitB_3.unit_id,
                move_vec=(-1, 0, 1)
            ),
            Action(
                ActionType.MOVE,
                unitB_1.unit_id,
                move_vec=(1,- 1, 0)
            ),
            Action(
                ActionType.MOVE,
                unitB_2.unit_id,
                move_vec=(-1, -1, 2)
            )
        ]

        simulation.add_player_actions(playerB, actions_B)

        # Ending first round
        simulation.end_round()

        # Starting second round
        new_units = { player_name : [] for player_name in simulation.players }
        simulation.start_round(new_units)

        # Players give orders
        actions_A = [
            Action(
              ActionType.HOLD,
                unitA_1.unit_id
            ),
            Action(
                ActionType.SUPPORT,
                unitA_2.unit_id,
                target_id=unitA_1.unit_id
            )
        ]
        simulation.add_player_actions(playerA, actions_A)

        actions_B = [
            Action(
                ActionType.ATTACK,
                unitB_3.unit_id,
                target_id=unitA_1.unit_id
            ),
            Action(
                ActionType.ATTACK,
                unitB_1.unit_id,
                target_id=unitA_1.unit_id
            ),
            Action(
                ActionType.SUPPORT,
                unitB_2.unit_id,
                target_id=unitB_1.unit_id
            )
        ]
        simulation.add_player_actions(playerB, actions_B)

        # Ending second round
        simulation.end_round()

        self.assertTrue(True)

def prepare_simulation(radius=3, max_round=20, upkeep_round=5):
    tiles = {}
    for q in range(-radius, radius+1):
        for r in range(max(-radius, -q-radius), min(radius, -q+radius)+1):
            s = -q - r
            tiles[(q, r, s)] = Tile(q, r, s)

    region = Region(
        "Dalaran",
        tiles,
        (0, 0, 0)
    )

    simulation = Simulation(
        players = ["Alice", "Bob"],
        max_round = max_round,
        upkeep_round = upkeep_round,
        tiles = tiles,
        regions = {region.region_id: region}
    )

    return simulation