import tkinter as tk
from display_module.join_menu.join_menu_screen_context import JoinMenuContext
from display_module.join_menu.simulation_entry import SimulationEntry

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
            font=("Segue UI", 18),
            bg=PANEL_COLOR,
            fg=TEXT_COLOR,
            width=20,
            height=2,
            command=lambda:self.context.Return()
        )
        self.top_bar.return_button.pack(
            side="left",
            anchor="nw",
            padx=5,
            pady=5
        )

        # 1.2 Search bar
        self.top_bar.search_bar = tk.Frame(self.top_bar, bg=PANEL_COLOR)
        self.top_bar.search_bar.pack(
            side="right",
            anchor="ne",
            padx=5,
            pady=5
        )

        # 1.2.1 Search bar text entry
        self.top_bar.search_bar.text_entry = tk.Entry(self.top_bar.search_bar)
        self.top_bar.search_bar.text_entry.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # 1.2.2 Search bar button
        self.top_bar.search_bar.button = tk.Button(
            self.top_bar.search_bar,
            text="Search",
            font=("Segue UI", 18),
            bg=PANEL_COLOR,
            fg=TEXT_COLOR,
            width=20,
            height=2,
            command=lambda:self.Search()
        )
        self.top_bar.search_bar.pack(
            padx=5,
            pady=5
        )

        # 2. Main panel
        self.main_panel = tk.Canvas(self, bg=PANEL_COLOR)
        self.main_panel.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        # 2.1 Scrollable frame
        self.main_panel.scrollable_frame = tk.Frame(
            self.main_panel,
            bg=PANEL_COLOR
        )

        self.main_panel.create_window(
            (0, 0),
            window=self.main_panel.scrollable_frame,
            anchor="nw",
        )

        self.main_panel.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_panel.configure(scrollregion=self.main_panel.bbox("all"))
        )

        # Hard-coded data
        for simulation_name, simulation_players in self.context.active_simulations.items():
            simulation_entry = SimulationEntry(
                self.main_panel.scrollable_frame,
                simulation_name,
                simulation_players[0],
                simulation_players[1]
            )
            simulation_entry.pack(
                anchor="n"
            )

    def Search(self):
        print("Searching the simulations list!")
        pass