import tkinter as tk
from display_module.gui.simulation.interaction_panel_views.orders_view.action_card import ActionCard

class ActionsView(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent, bg="#3b3b3b")

        self.context = context

        # Main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        # Header
        self.header = tk.Label(
            self,
            text="Actions",
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

        self.refresh_action_list()

    def add_action(self, unit_action, unit_id, target_id=None, move_vec=None):
        self.context.add_action(unit_action, unit_id, target_id, move_vec)
        self.refresh_action_list()

    def remove_action(self, action_id):
        self.context.remove_action(action_id)
        self.refresh_action_list()

    def refresh_action_list(self):
        for widget in self.list_container.winfo_children():
            widget.destroy()
        for i in range(len(self.context.actions)):
            action = self.context.actions[i]
            card = ActionCard(
                self.list_container,
                action.unit_action,
                action.unit_id,
                action.target_id if action.move_vec is None else action.move_vec,
                remove_func=lambda action_id=action.id: self.remove_action(i)
            )

            card.pack(
                fill="x",
                padx=8,
                pady=4,
            )