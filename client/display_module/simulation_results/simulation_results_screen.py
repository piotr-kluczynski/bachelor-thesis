import tkinter as tk

from display_module.simulation_results.simulation_results_context import SimulationResultsContext
from display_module.simulation_results.simulation_results_views.board_view.board_view import BoardView
from display_module.simulation_results.simulation_results_views.military_view.military_view import MilitaryView
from display_module.simulation_results.simulation_results_views.ovierview_view.ovierview_view import OverviewView
from display_module.simulation_results.simulation_results_views.total_view.total_view import TotalView

BACKGROUND_COLOR = "#1e1e1e"
PANEL_COLOR = "#262626"
TEXT_COLOR = "#f0f0f0"
SECONDARY_COLOR = "#b0b0b0"
ACCENT_COLOR = "#3b3b3b"

class SimulationResultsScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.context = SimulationResultsContext()

        self.configure(bg=BACKGROUND_COLOR)

        # Main Grid
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.grid_columnconfigure(0, weight=1)

        # 1. Top bar
        self.top_bar = tk.Frame(
            self,
            bg=BACKGROUND_COLOR
        )
        self.top_bar.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5
        )

        self.view_buttons = {
            "overview": self.create_tab_button("Overview", "overview"),
            "military": self.create_tab_button("Military", "military"),
            "board": self.create_tab_button("Board", "board"),
            "total": self.create_tab_button("Total", "total")
        }

        # 2. Main panel
        self.main_panel = tk.Frame(
            self,
            bg=BACKGROUND_COLOR
        )
        self.main_panel.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=5
        )
        self.main_panel.grid_rowconfigure(0, weight=1)
        self.main_panel.grid_columnconfigure(0, weight=1)

        self.views = {
            "overview": OverviewView(self.main_panel),
            "military": MilitaryView(self.main_panel),
            "board": BoardView(self.main_panel),
            "total": TotalView(self.main_panel)
        }

        for view in self.views.values():
            view.grid(
                row=0,
                column=0,
                sticky="nsew"
            )

        # 3. Bottom bar
        self.bottom_bar = tk.Frame(
            self,
            bg=BACKGROUND_COLOR
        )
        self.bottom_bar.grid(
            row=2,
            column=0,
            sticky="nsew"
        )

        # 3.1. Leave button
        self.bottom_bar.return_button = tk.Button(
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
        self.bottom_bar.return_button.pack(
            side="left",
            anchor="w",
            padx=5,
            pady=5
        )

        # 3.2. Save button
        self.bottom_bar.save_button = tk.Button(
            self.bottom_bar,
            text="Save",
            font=("Segue UI", 16, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground="#4a4a4a",
            activeforeground="white",
            bd=0,
            padx=15,
            cursor="hand2",
            command=self.context.Save
        )
        self.bottom_bar.save_button.pack(
            side="right",
            anchor="e",
            padx=5,
            pady=5
        )

        self.set_active_btn("total")

    def create_tab_button(self, text, view_name):
        btn = tk.Button(
            self.top_bar,
            text=text,
            font=("Segue UI", 11, "bold"),
            bg=PANEL_COLOR,
            fg=TEXT_COLOR,
            activebackground="#4a4a4a",
            activeforeground="white",
            bd=0,
            padx=15,
            cursor="hand2",
            relief="flat",
            command=lambda: self.show_view(view_name),
        )
        btn.pack(
            side="left",
            pady=(5, 0)
        )

        return btn

    def show_view(self, view_name):
        view = self.views[view_name]
        self.set_active_btn(view_name)
        view.tkraise()

    def set_active_btn(self, active_btn_name):
        for name, btn in self.view_buttons.items():
            if name == active_btn_name:
                btn.configure(
                    bg=PANEL_COLOR
                )
            else:
                btn.configure(
                    bg=BACKGROUND_COLOR
                )