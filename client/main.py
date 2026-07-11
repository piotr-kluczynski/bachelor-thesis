import tkinter as tk

from display_module.join_menu.join_menu_screen import JoinMenuScreen
from display_module.main_menu.main_menu_screen import MainMenuScreen

if __name__ == '__main__':
    root = tk.Tk()

    root.title("Simulation")
    root.geometry("1000x500")
    root.minsize(1000, 500)

    screen = JoinMenuScreen(root)
    screen.pack(fill="both", expand=True)

    root.mainloop()