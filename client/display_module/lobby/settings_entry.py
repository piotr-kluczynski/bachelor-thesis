import tkinter as tk

BACKGROUND_COLOR = "#1e1e1e"
PANEL_COLOR = "#262626"
TEXT_COLOR = "#f0f0f0"
SECONDARY_COLOR = "#b0b0b0"
ACCENT_COLOR = "#3b3b3b"

class SettingsEntry(tk.Frame):
    def __init__(self, parent, name, value):
        tk.Frame.__init__(self, parent)

        self.configure(bg=BACKGROUND_COLOR)

        # Settings name
        self.name = tk.Label(
            self,
            text=name,
            fg=TEXT_COLOR,
            bg=PANEL_COLOR,
            font=("Segue UI", 11)
        )
        self.name.pack(
            side="left",
            anchor="w",
            padx=5,
            pady=5
        )

        # Setting value
        self.value = tk.Label(
            self,
            text=value,
            fg=TEXT_COLOR,
            bg=PANEL_COLOR,
            font=("Segue UI", 14, "bold")
        )
        self.value.pack(
            side="left",
            anchor="e",
            padx=5,
            pady=5
        )