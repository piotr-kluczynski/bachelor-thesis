import tkinter as tk

class UnitCard(tk.Frame):
    def __init__(self, parent, context, unit):
        super().__init__(
            parent,
            bg="#353535",
            padx=10,
            pady=8
        )

        self.context = context

        self.configure(
            highlightbackground="#4a4a4a",
            highlightthickness=1
        )

        # Name
        name_label = tk.Label(
            self,
            text=unit.unit_id,
            bg="#353535",
            fg="white",
            font=("Arial", 12, "bold"),
            anchor="w"
        )

        name_label.pack(
            fill="y",
            side="left",
            anchor="w"
        )

        # Go-to button
        goto_btn = tk.Button(
            self,
            text="Go to",
            command=lambda: self.context.center_camera_on(unit.tile.q, unit.tile.r)
        )

        goto_btn.pack(
            fill="y",
            side="right",
            anchor="w"
        )