import tkinter as tk

class TopBar(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent, bg="#2b2b2b", height=50)

        self.context = context

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
        self.players = tk.Frame(self, bg="#2b2b2b")
        self.players.grid(row=0, column=1, sticky="e")

        self.load_player_status()


    def load_player_status(self):
        for player_id in self.context.players_ids:
            label = tk.Label(
                self.players,
                text=f"{self.context.player_names.get(player_id)}: {self.context.players_status.get(player_id)}",
                bg="#2b2b2b",
                fg=self.context.players_colors.get(player_id),
            )

            label.pack(side="left", padx=10)
