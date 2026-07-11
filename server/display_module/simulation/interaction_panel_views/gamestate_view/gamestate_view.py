import tkinter as tk

from display_module.simulation.interaction_panel_views.gamestate_view.region_card import RegionCard
from display_module.simulation.interaction_panel_views.gamestate_view.unit_card import UnitCard


class GamestateView(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent, bg="#3b3b3b")

        self.context = context

        self.regions = [
            "Mossvale",
            "Starhold",
            "Frostpeak",
            "Dunescar",
            "Eldergrove"
        ]

        self.units = [
            (0, "light_infantry1"),
            (0, "light_infantry2"),
            (0, "light_infantry8"),
            (0, "light_infantry15"),
            (0, "light_infantry16"),
            (1, "heavy_infantry4"),
            (1, "heavy_infantry6"),
            (1, "heavy_infantry7"),
            (2, "cavalry8"),
            (2, "cavalry11")
        ]

        # Main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=4)

        # Header
        self.header = tk.Label(
            self,
            text="Game State",
            font=("Arial", 20),
            bg="#2a2a2a",
            fg="white",
            anchor="w",
            padx=10,
            pady=10
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        # Round counter
        self.round_label = tk.Label(
            self,
            text="Round " + str(self.context.current_round) + "/" + str(self.context.max_round),
            font=("Arial", 30),
            bg="#2a2a2a",
            fg="white",
            anchor="center",
            padx=10,
            pady=10
        )

        self.round_label.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        # Unit/Region frame
        self.content = tk.Frame(
            self,
            bg="#2a2a2a"
        )

        self.content.grid(
            row=2,
            column=0,
            sticky="nsew"
        )

        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_columnconfigure(1, weight=1)
        self.content.grid_rowconfigure(0, weight=0)
        self.content.grid_rowconfigure(1, weight=1)

        # Region header
        self.unit_header = tk.Label(
            self.content,
            text="Your Regions",
            font=("Arial", 15),
            bg="#2a2a2a",
            fg="white",
            padx=10,
            pady=10,
            anchor="w"
        )

        self.unit_header.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # Region list
        self.region_list = tk.Frame(
            self.content,
            bg="#2b2b2b"
        )

        self.region_list.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        # Unit header
        self.unit_header = tk.Label(
            self.content,
            text="Your Units",
            font=("Arial", 15),
            bg="#2a2a2a",
            fg="white",
            padx=10,
            pady=10,
            anchor="w"
        )

        self.unit_header.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        # Unit list
        self.units_list = tk.Frame(
            self.content,
            bg="#2b2b2b"
        )

        self.units_list.grid(
            row=1,
            column=1,
            sticky="nsew"
        )

        self.refresh_region_list()
        self.refresh_unit_list()

    def add_region_card(self, name):
        self.regions.append(name)
        self.refresh_region_list()

    def add_unit_card(self, unit_type, name):
        self.units.append((unit_type, name))
        self.refresh_unit_list()

    def refresh_region_list(self):
        for widget in self.region_list.winfo_children():
            widget.destroy()
        for region in self.context.regions.items():
            card = RegionCard(
                self.region_list,
                self.context,
                region
            )

            card.pack(
                fill="x",
                padx=8,
                pady=4,
            )

    def refresh_unit_list(self):
        for widget in self.units_list.winfo_children():
            widget.destroy()

        units = [unit[1] for unit in self.context.units.items() if unit[1].owner == self.context.my_id]

        for unit in units:
            card = UnitCard(
                self.units_list,
                self.context,
                unit
            )
            card.pack(
                fill="x",
                padx=8,
                pady=4,
            )