import tkinter as tk

class ActionCard(tk.Frame):
    def __init__(self, parent, action, unit, target, remove_func):
        super().__init__(
            parent,
            bg="#353535",
            padx=10,
            pady=8
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=0)

        self.configure(
            highlightbackground="#4a4a4a",
            highlightthickness=1
        )

        # Description frame
        self.description = tk.Frame(
            self,
            bg="#353535"
        )
        self.description.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # Action
        type_label = tk.Label(
            self.description,
            text=action,
            bg="#353535",
            fg="white",
            font=("Arial", 12, "bold"),
            anchor="w"
        )

        type_label.pack(
            fill="x",
            anchor="w"
        )

        # Unit
        unit_label = tk.Label(
            self.description,
            text="Unit: " + unit,
            bg="#353535",
            fg="#bbbbbb",
            font=("Arial", 10),
            anchor="w"
        )

        unit_label.pack(
            fill="x",
            anchor="w"
        )

        # Target
        target_label = tk.Label(
            self.description,
            text="Target: " + target,
            bg="#353535",
            fg="#bbbbbb",
            font=("Arial", 10),
            anchor="w"
        )

        target_label.pack(
            fill="x",
            anchor="w"
        )

        # Button
        delete_btn = tk.Button(
            self,
            text="Delete",
            width=10,
            command=remove_func
        )

        delete_btn.grid(
            row=0,
            column=1,
            sticky="nsew"
        )