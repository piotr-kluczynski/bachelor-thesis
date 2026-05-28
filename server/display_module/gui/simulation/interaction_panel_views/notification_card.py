import tkinter as tk

class NotificationCard(tk.Frame):
    def __init__(self, parent, title, description):
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

        # Title
        title_label = tk.Label(
            self,
            text=title,
            bg="#353535",
            fg="white",
            font=("Arial", 12, "bold"),
            anchor="w"
        )

        title_label.pack(
            fill="x",
            anchor="w"
        )

        # Description
        desc_label = tk.Label(
            self,
            text=description,
            bg="#353535",
            fg="#bbbbbb",
            font=("Arial", 10),
            wraplength=400,
            anchor="w"
        )
        desc_label.pack(
            fill="x",
            anchor="w",
            pady=(4, 0)
        )