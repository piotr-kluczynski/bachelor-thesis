import tkinter as tk

class GamestateView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#3b3b3b")

        label = tk.Label(
            self,
            text="Game State",
            font=("Arial", 20),
            bg="#3b3b3b",
            fg="white"
        )

        label.pack(pady=20)