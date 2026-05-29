import tkinter as tk

class UnitCard(tk.Frame):
    def __init__(self, parent, name):
        super().__init__(
            parent,
            bg="#353535",
            padx=10,
            pady=8
        )

        self.configure(
            highlightbackground="#4a4a4a",
            highlightthickness=1
        )

        # Name
        name_label = tk.Label(
            self,
            text=name,
            bg="#353535",
            fg="white",
            font=("Arial", 12, "bold"),
            anchor="w"
        )

        name_label.pack(
            fill="x",
            anchor="w"
        )