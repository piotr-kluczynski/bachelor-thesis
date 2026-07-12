import tkinter as tk
import tkinter.messagebox

from display_module.join_menu.join_menu_screen_context import JoinMenuContext
from display_module.join_menu.search_bar import SearchBar
from display_module.join_menu.simulation_list import SimulationList

BACKGROUND_COLOR = "#1e1e1e"
PANEL_COLOR = "#262626"
TEXT_COLOR = "#f0f0f0"
SECONDARY_COLOR = "#b0b0b0"
ACCENT_COLOR = "#3b3b3b"

class JoinMenuScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.context = JoinMenuContext()

        self.configure(bg=BACKGROUND_COLOR)

        # Main Grid
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.grid_columnconfigure(0, weight=1)

        # 1. Top bar
        self.top_bar = tk.Frame(self, bg=PANEL_COLOR)
        self.top_bar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # 1.1 Return button
        self.top_bar.return_button = tk.Button(
            self.top_bar,
            text="Return",
            font=("Segue UI", 18, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground="#4a4a4a",
            activeforeground="white",
            bd=0,
            padx=15,
            cursor="hand2",
            command=lambda:self.context.Return()
        )
        self.top_bar.return_button.pack(
            side="left",
            anchor="nw",
            padx=5,
            pady=5
        )

        # 1.2. Search bar
        self.top_bar.search_bar = SearchBar(self.top_bar, self.context)
        self.top_bar.search_bar.pack(
            side="right",
            anchor="ne",
            padx=5,
            pady=5
        )

        # 1.3. Reload Button
        self.top_bar.reload_button = tk.Button(
            self.top_bar,
            text="Reload",
            font=("Segue UI", 11, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground="#4a4a4a",
            activeforeground="white",
            bd=0,
            padx=15,
            cursor="hand2",
            command=self.context.ReloadList
        )
        self.top_bar.reload_button.pack(
            side="right",
            anchor="e",
            padx=5,
            pady=5
        )

        # 2. Main panel
        self.main_panel = SimulationList(self, self.context.active_simulations)
        self.main_panel.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        # We set up the reference to the simulation_list
        self.context.simulation_list = self.main_panel

        # We call the popup message for the user to choose the game mode
        self.ModePopupMsg()

    def ModePopupMsg(self):
        self.context.ai_agent_mode = tk.messagebox.askyesno(
            title="Choose client mode",
            message="Would you like to personally participate in the simulation?\nIf your answer is no, then the this client will be controlled by the AI Agent."
        )