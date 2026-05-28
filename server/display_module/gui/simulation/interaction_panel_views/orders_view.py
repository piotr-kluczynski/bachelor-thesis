import tkinter as tk

class OrdersView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#3b3b3b")

        label = tk.Label(
            self,
            text="Orders",
            font=("Arial", 20),
            bg="#3b3b3b",
            fg="white"
        )

        label.pack(pady=20)