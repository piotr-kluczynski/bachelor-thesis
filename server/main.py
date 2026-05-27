import tkinter as tk
from display_module.gui.simulation.simulation_screen import SimulationScreen
from simulation_module.simulation import Simulation

if __name__ == '__main__':
    simulation = Simulation([0])
    simulation.create_empty_board(9, 9, 9)

    root = tk.Tk()

    root.title("Simulation")
    root.geometry("1280x720")
    root.minsize(900, 500)

    screen = SimulationScreen(root, simulation.board)
    screen.pack(fill="both", expand=True)

    root.mainloop()