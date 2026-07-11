import tkinter as tk
from display_module.main_menu.main_menu_context import MainMenuContext

BACKGROUND_COLOR = "#1e1e1e"
PANEL_COLOR = "#262626"
TEXT_COLOR = "#f0f0f0"
SECONDARY_COLOR = "#b0b0b0"
ACCENT_COLOR = "#3b3b3b"

class MainMenuScreen(tk.Frame):
    def __init__(self, parent, menu_buttons):
        super().__init__(parent)

        self.context = MainMenuContext(menu_buttons)

        self.configure(bg=BACKGROUND_COLOR)

        # Main Grid
        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 1. Left panel
        self.left_panel = tk.Frame(self, bg=PANEL_COLOR)
        self.left_panel.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # 1.1 Title label
        self.left_panel.title_label = tk.Label(
            self.left_panel,
            text="Large Language\nCivilization",
            fg="white",
            bg=PANEL_COLOR,
            font=("Segue UI", 56, "bold")
        )
        self.left_panel.title_label.pack(
            anchor="w",
            padx=10,
            pady=(40, 10)
        )

        # 1.2 Description
        self.left_panel.description_label = tk.Label(
            self.left_panel,
            text="Piotr Kluczyński\nBachelor Thesis",
            fg="#bbbbbb",
            bg=PANEL_COLOR,
            font=("Segue UI", 18)
        )
        self.left_panel.description_label.pack(
            anchor="w",
            padx=10,
            pady=(40, 10)
        )

        # 2. Right panel
        self.right_panel = tk.Frame(self, bg=PANEL_COLOR)
        self.right_panel.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        # 2.1 List of buttons
        for button_name, button_func in self.context.menu_buttons.items():
            new_button = tk.Button(
                self.right_panel,
                text=button_name,
                font=("Segue UI", 24),
                bg=PANEL_COLOR,
                fg=TEXT_COLOR,
                width=20,
                height=2,
                command=button_func
            )
            new_button.pack(
                side="bottom",
                anchor="s",
                padx=10,
                pady=10
            )