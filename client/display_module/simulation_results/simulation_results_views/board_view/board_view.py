import tkinter as tk

BACKGROUND_COLOR = "#1e1e1e"
PANEL_COLOR = "#262626"
TEXT_COLOR = "#f0f0f0"
SECONDARY_COLOR = "#b0b0b0"
ACCENT_COLOR = "#3b3b3b"

class BoardView(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = tk.Label(
            self,
            text="Board Statistics",
            fg="white",
            bg=PANEL_COLOR,
            font=("Segue UI", 24, "bold")
        )
        self.title_label.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.info_label = tk.Label(
            self,
            text="Not developed yet",
            fg="white",
            bg=PANEL_COLOR,
            font=("Segue UI", 16)
        )
        self.info_label.grid(
            row=1,
            column=0,
            sticky="nsew"
        )