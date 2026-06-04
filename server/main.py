import tkinter as tk
from display_module.gui.simulation.simulation_screen import SimulationScreen
from simulation_module.simulation import Simulation

if __name__ == '__main__':
    simulation = Simulation([0])
    simulation.create_empty_board(9, 9, 9)
    simulation.add_light_infantry(0, -2, 2, 0)
    simulation.add_heavy_infantry(0, 4, -2, -2)
    simulation.add_cavalry(1, -3, -3, 6)

    simulation.board.tiles.get((0, 0, 0)).region = "Warszawa"
    simulation.board.tiles.get((-1, 0, 1)).region = "Warszawa"

    root = tk.Tk()

    root.title("Simulation")
    root.geometry("1280x720")
    root.minsize(900, 500)

    screen = SimulationScreen(root, simulation)
    screen.pack(fill="both", expand=True)

    root.mainloop()