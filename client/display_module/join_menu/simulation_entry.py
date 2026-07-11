import tkinter as tk

BACKGROUND_COLOR = "#1e1e1e"
PANEL_COLOR = "#262626"
TEXT_COLOR = "#f0f0f0"
SECONDARY_COLOR = "#b0b0b0"
ACCENT_COLOR = "#3b3b3b"

class SimulationEntry(tk.Frame):
    def __init__(self, parent, name, noPlayers, maxNoPlayers):
        tk.Frame.__init__(self, parent)

        self.configure(bg=BACKGROUND_COLOR)

        # 1. Title of the simulation
        self.title = tk.Label(
            self,
            text=name,
            fg=TEXT_COLOR,
            bg=PANEL_COLOR,
            font=("Segue UI", 24, "bold")
        )
        self.title.pack(
            side="left",
            anchor="nw",
            padx=5,
            pady=5
        )

        # 2. Simulation player status
        self.player_status = tk.Label(
            self,
            text=f"{noPlayers}/{maxNoPlayers}",
            fg=TEXT_COLOR,
            bg=PANEL_COLOR,
            font=("Segue UI", 24)
        )
        self.player_status.pack(
            side="left",
            anchor="nw",
            padx=5,
            pady=5
        )

        # 3. Join button
        self.join_button = tk.Button(
            self,
            text="Join",
            font=("Segue UI", 24),
            bg=PANEL_COLOR,
            fg=TEXT_COLOR,
            width=20,
            height=2,
            command=lambda: print(f"Simulation {name} joined!")
        )
        self.join_button.pack(
            side="right",
            anchor="ne",
            padx=5,
            pady=5
        )

        self.pack(fill="x", padx=15, pady=5)