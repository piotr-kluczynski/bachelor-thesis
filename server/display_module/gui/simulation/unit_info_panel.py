import tkinter as tk

class UnitInfoPanel(tk.Frame):
    def __init__(self, parent, context):
        tk.Frame.__init__(self, parent)

        self.context = context

        self.unit_id = ""
        self.unit_movement = ""
        self.unit_strength = ""
        self.unit_upkeep = ""
        self.unit_owner = ""

        self.configure(
            bg="#444444",
            height=120
        )

        self.unit_id_label = tk.Label(
            self,
            text=f"Name:\n{self.unit_id}",
            bg="#444444",
            fg="white",
            font=("Arial", 12)
        )
        self.unit_id_label.pack(
            anchor="w",
            side="left",
            padx=10,
            pady=10
        )

        self.unit_movement_label = tk.Label(
            self,
            text=f"Movement:\n{self.unit_movement}",
            bg="#444444",
            fg="white",
            font=("Arial", 12)
        )
        self.unit_movement_label.pack(
            anchor="w",
            side="left",
            padx=10,
            pady=10
        )

        self.unit_strength_label = tk.Label(
            self,
            text=f"Strength:\n{self.unit_strength}",
            bg="#444444",
            fg="white",
            font=("Arial", 12)
        )
        self.unit_strength_label.pack(
            anchor="w",
            side="left",
            padx=10,
            pady=10
        )

        self.unit_upkeep_label = tk.Label(
            self,
            text=f"Upkeep:\n{self.unit_upkeep}",
            bg="#444444",
            fg="white",
            font=("Arial", 12)
        )
        self.unit_upkeep_label.pack(
            anchor="w",
            side="left",
            padx=10,
            pady=10
        )

        self.unit_owner_label = tk.Label(
            self,
            text=f"Owner:\n{self.context.players_names.get(self.unit_owner)}",
            bg="#444444",
            fg="white",
            font=("Arial", 12)
        )
        self.unit_owner_label.pack(
            anchor="w",
            side="left",
            padx=10,
            pady=10
        )

    def refresh_labels(self):
        self.unit_id_label.config(
            text=f"Name:\n{self.unit_id}"
        )

        self.unit_movement_label.config(
            text=f"Movement:\n{self.unit_movement}"
        )

        self.unit_strength_label.config(
            text=f"Strength:\n{self.unit_strength}"
        )

        self.unit_upkeep_label.config(
            text=f"Upkeep:\n{self.unit_upkeep}"
        )

        self.unit_owner_label.config(
            text=f"Owner:\n{self.context.players_names.get(self.unit_owner)}"
        )

    def set_data(self, unit):
        self.unit_id = unit.unit_id
        self.unit_movement = unit.movement
        self.unit_strength = unit.strength
        self.unit_upkeep = unit.upkeep
        self.unit_owner = unit.owner

        self.refresh_labels()