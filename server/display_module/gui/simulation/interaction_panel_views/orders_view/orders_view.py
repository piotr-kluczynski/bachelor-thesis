import tkinter as tk
from display_module.gui.simulation.interaction_panel_views.orders_view.order_card import OrderCard

class OrdersView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#3b3b3b")

        # Hard-coded order list
        self.orders = [
            (0, "Attack", "light_infantry23", "cavalry7"),
            (1, "Move", "cavalry4", "(-8, 9, -1)"),
            (2, "Move", "cavalry8", "(-2, 1, 1)"),
            (3, "Attack", "heavy_infantry10", "light_infantry12")
        ]

        # Main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        # Header
        self.header = tk.Label(
            self,
            text="Orders",
            font=("Arial", 20),
            bg="#2a2a2a",
            fg="white",
            padx=10,
            pady=10,
            anchor="w"
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        # Order list
        self.list_container = tk.Frame(
            self,
            bg="#2b2b2b",
        )

        self.list_container.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        # Bottom frame
        self.bottom_frame = tk.Frame(
            self,
            bg="#2b2b2b"
        )

        self.bottom_frame.grid(
            row=2,
            column=0,
            sticky="nsew"
        )

        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=3)
        self.bottom_frame.grid_columnconfigure(1, weight=1)

        # Send button
        self.send_button = tk.Button(
            self.bottom_frame,
            text="Send"
        )

        self.send_button.grid(
            row=0,
            column=1,
            padx=8,
            pady=8,
            sticky="ew"
        )

        self.refresh_order_list()

    def add_order(self, action, unit, target):
        self.orders.append((len(self.orders), action, unit, target))
        self.refresh_order_list()

    def remove_order(self, order_id):
        self.orders = [order for order in self.orders if order[0] != order_id]

        self.refresh_order_list()

    def refresh_order_list(self):
        for widget in self.list_container.winfo_children():
            widget.destroy()
        for order in self.orders:
            card = OrderCard(
                self.list_container,
                order[1],
                order[2],
                order[3],
                remove_func=lambda order_id=order[0]: self.remove_order(order_id)
            )

            card.pack(
                fill="x",
                padx=8,
                pady=4,
            )