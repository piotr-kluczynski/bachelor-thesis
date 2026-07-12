import tkinter as tk

from display_module.lobby.lobby_screen import LobbyScreen

if __name__ == '__main__':
    root = tk.Tk()

    root.title("Simulation")
    root.geometry("1000x500")
    root.minsize(1000, 500)

    screen = LobbyScreen(root)
    screen.pack(fill="both", expand=True)

    root.mainloop()