import tkinter as tk

from display_module.simulation.board_panel import BoardPanel
from display_module.simulation.interaction_panel import InteractionPanel
from display_module.simulation.simulation_context import SimulationContext
from display_module.simulation.top_bar import TopBar


class SimulationScreen(tk.Frame):
    def __init__(self, parent, board, units, players_ids, player_names):
        super().__init__(parent)

        self.configure(bg="#1e1e1e")

        self.context = SimulationContext(board, units, players_ids, player_names)

        # Main Grid
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.grid_columnconfigure(0, weight=1)

        # Top bar
        self.top_bar = TopBar(self, self.context)
        self.top_bar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # Content
        self.content = tk.Frame(self, bg="#222222")
        self.content.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_columnconfigure(1, weight=1)

        self.content.grid_rowconfigure(0, weight=1)

        # Board panel
        self.board_panel = BoardPanel(self.content, self.context)
        self.board_panel.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # Interaction panel
        self.interaction_panel = InteractionPanel(self.content, self.context)
        self.interaction_panel.grid(
            row=0,
            column=1,
            sticky="nsew"
        )