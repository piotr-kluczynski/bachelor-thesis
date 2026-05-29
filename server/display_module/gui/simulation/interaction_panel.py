import tkinter as tk

from display_module.gui.simulation.interaction_panel_views.console_view.console_view import ConsoleView
from display_module.gui.simulation.interaction_panel_views.conversation_view.conversation_view import ConversationView
from display_module.gui.simulation.interaction_panel_views.gamestate_view.gamestate_view import GamestateView
from display_module.gui.simulation.interaction_panel_views.notifications_view.notifications_view import NotificationsView
from display_module.gui.simulation.interaction_panel_views.orders_view.orders_view import OrdersView

class InteractionPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2f2f2f", width=300)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.grid_columnconfigure(0, weight=1)

        # Tab bar
        self.tab_bar = tk.Frame(self, bg="#252525", height=40)
        self.tab_bar.grid(row=0, column=0, sticky="nsew")

        # Content
        self.content = tk.Frame(self, bg="#2f2f2f")
        self.content.grid(row=1, column=0, sticky="nsew")

        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        # Views
        self.views = {
            "console": ConsoleView(self.content),
            "conversation": ConversationView(self.content),
            "gamestate": GamestateView(self.content),
            "notifications": NotificationsView(self.content),
            "orders": OrdersView(self.content)
        }

        for view in self.views.values():
            view.grid(row=0, column=0, sticky="nsew")

        # Buttons
        self.create_tab_button("Console", "console")
        self.create_tab_button("Conversation", "conversation")
        self.create_tab_button("Gamestate", "gamestate")
        self.create_tab_button("Notifications", "notifications")
        self.create_tab_button("Orders", "orders")

    def create_tab_button(self, text, view_name):
        btn = tk.Button(
            self.tab_bar,
            text=text,
            relief="flat",
            bg="#444444",
            fg="white",
            command=lambda: self.show_view(view_name),
        )

        btn.pack(side="left", padx=2, pady=2)

    def show_view(self, view_name):
        view = self.views[view_name]
        view.tkraise()