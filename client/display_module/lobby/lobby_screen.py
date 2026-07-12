import tkinter as tk

from display_module.lobby.lobby_context import LobbyContext
from display_module.lobby.player_list import PlayerList
from display_module.lobby.settings_list import SettingsList

BACKGROUND_COLOR = "#1e1e1e"
PANEL_COLOR = "#262626"
TEXT_COLOR = "#f0f0f0"
SECONDARY_COLOR = "#b0b0b0"
ACCENT_COLOR = "#3b3b3b"

class LobbyScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.context = LobbyContext()

        # Main grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.grid_columnconfigure(0, weight=1)

        # 1. Main panel
        self.main_panel = tk.Frame(
            self,
            bg=BACKGROUND_COLOR
        )
        self.main_panel.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.main_panel.grid_rowconfigure(0, weight=1)

        self.main_panel.grid_columnconfigure(0, weight=1)
        self.main_panel.grid_columnconfigure(1, weight=0)

        # 1.1. Left column
        self.main_panel.left_panel = tk.Frame(
            self.main_panel,
            bg=PANEL_COLOR
        )
        self.main_panel.left_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(15, 8),
            pady=15
        )

        # 1.1.1 Title label
        self.main_panel.left_panel.title = tk.Label(
            self.main_panel.left_panel,
            text=self.context.name,
            fg="white",
            bg=BACKGROUND_COLOR,
            font=("Segue UI", 36, "bold")
        )
        self.main_panel.left_panel.title.pack(
            side="top",
            anchor="w",
            fill="both",
            padx=10,
            pady=10
        )

        # 1.1.2 Player list
        self.main_panel.left_panel.player_list = PlayerList(self.main_panel.left_panel, self.context.lobby_players)
        self.main_panel.left_panel.player_list.pack(
            side="bottom",
            anchor="nw",
            fill="both",
            padx=10,
            pady=10
        )

        # 1.2. Right column
        self.main_panel.right_panel = tk.Frame(
            self.main_panel,
            bg=PANEL_COLOR
        )
        self.main_panel.right_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 15),
            pady=15
        )

        self.main_panel.right_panel.settings_title = tk.Label(
            self.main_panel.right_panel,
            text="Simulation Settings",
            fg="white",
            bg=BACKGROUND_COLOR,
            font=("Segue UI", 18)
        )
        self.main_panel.right_panel.settings_title.pack(
            side="top",
            anchor="w",
            fill="both",
            padx=10,
            pady=10
        )

        self.main_panel.right_panel.settings_list = SettingsList(self.main_panel.right_panel, self.context.settings)
        self.main_panel.right_panel.settings_list.pack(
            side="bottom",
            anchor="n",
            padx=10,
            pady=10
        )

        # 2. Bottom bar
        self.bottom_bar = tk.Frame(
            self,
            bg=BACKGROUND_COLOR
        )
        self.bottom_bar.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        # 2.1. Leave button
        self.bottom_bar.leave_button = tk.Button(
            self.bottom_bar,
            text="Leave",
            font=("Segue UI", 16, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground="#4a4a4a",
            activeforeground="white",
            bd=0,
            padx=15,
            cursor="hand2",
            command=self.context.Leave
        )
        self.bottom_bar.leave_button.pack(
            side="left",
            anchor="w",
            padx=5,
            pady=5
        )

        # 2.2. Ready button
        self.bottom_bar.ready_button = tk.Button(
            self.bottom_bar,
            text="Not Ready",
            font=("Segue UI", 16, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground="#4a4a4a",
            activeforeground="white",
            bd=0,
            padx=15,
            cursor="hand2",
            command=self.pressReadyBtn
        )
        self.bottom_bar.ready_button.pack(
            side="right",
            anchor="e",
            padx=5,
            pady=5
        )

    def pressReadyBtn(self):
        self.context.ChangeReadyState()
        self.bottom_bar.ready_button.config(text="Ready" if self.context.ready else "Not Ready")
