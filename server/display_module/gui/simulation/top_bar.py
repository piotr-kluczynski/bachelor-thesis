import tkinter as tk

class TopBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2b2b2b", height=50)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # Left side
        left = tk.Frame(self, bg="#2b2b2b")
        left.grid(row=0, column=0, sticky="w")

        exit_btn = tk.Button(left, text="Exit")
        exit_btn.pack(side="left", padx=5, pady=5)

        pause_btn = tk.Button(left, text="Pause")
        pause_btn.pack(side="left", padx=5, pady=5)

        # Right side
        players = tk.Frame(self, bg="#2b2b2b")
        players.grid(row=0, column=1, sticky="e")

        # Mock data for displaying the screen
        for i in range(4):
            label = tk.Label(
                players,
                text=f"Player {i + 1}: ONLINE",
                bg="#2b2b2b",
                fg="white",
            )

            label.pack(side="left", padx=10)