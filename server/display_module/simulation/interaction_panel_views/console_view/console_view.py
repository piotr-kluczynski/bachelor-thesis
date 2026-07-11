import tkinter as tk

from display_module.simulation.interaction_panel_views.console_view.console_panel import ConsolePanel

class ConsoleView(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent, bg="#3b3b3b")

        self.context = context

        # Main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header = tk.Label(
            self,
            text="Console",
            bg="#2a2a2a",
            fg="white",
            anchor="w",
            padx=10,
            pady=10,
            font=("Arial", 20)
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        # Console frame
        content = tk.Frame(
            self,
            bg="#3b3b3b"
        )

        content.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        # Console layout
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

        self.console_panel = ConsolePanel(content, self.context)

        self.console_panel.grid(
            row=0,
            column=0,
            sticky="nsew"
        )