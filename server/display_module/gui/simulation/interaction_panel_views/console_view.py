import tkinter as tk

from display_module.gui.simulation.interaction_panel_views.console_panel import ConsolePanel

class ConsoleView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#3b3b3b")

        # Main grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Console panel
        self.console_panel = ConsolePanel(self)

        self.console_panel.grid(
            row=0,
            column=1,
            sticky="nsew"
        )