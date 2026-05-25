import simulation_module
from simulation_module import Simulation

if __name__ == '__main__':
    simulation = Simulation([0, 1])
    simulation.create_empty_board(3, 3, 3)
    simulation.add_heavy_infantry(0, 0, 0, 0)
    simulation.add_light_infantry(1, -1, 1, 0)

    player0_orders = [simulation_module.Action("Attack", 0, 1, None)]
    simulation.add_player_actions(0, player0_orders)
    simulation.end_round()