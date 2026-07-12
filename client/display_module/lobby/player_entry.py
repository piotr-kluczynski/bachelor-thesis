import tkinter as tk

BACKGROUND_COLOR = "#1e1e1e"
PANEL_COLOR = "#262626"
TEXT_COLOR = "#f0f0f0"
SECONDARY_COLOR = "#b0b0b0"
ACCENT_COLOR = "#3b3b3b"

class PlayerEntry(tk.Frame):
    def __init__(self, parent, player_name, player_status):
        tk.Frame.__init__(self, parent)

        self.configure(bg=BACKGROUND_COLOR)

        # Player name
        self.player_name = tk.Label(
            self,
            text=player_name,
            fg=TEXT_COLOR,
            bg=PANEL_COLOR,
            font=("Segue UI", 14, "bold")
        )
        self.player_name.pack(
            side="left",
            anchor="w",
            padx=5,
            pady=5
        )

        # Player status
        self.player_status = tk.Label(
            self,
            text="Ready" if player_status else "Not ready",
            fg=TEXT_COLOR,
            bg=PANEL_COLOR,
            font=("Segue UI", 14, "bold")
        )
        self.player_status.pack(
            side="right",
            anchor="e",
            padx=5,
            pady=5
        )