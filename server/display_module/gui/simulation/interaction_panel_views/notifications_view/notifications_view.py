import tkinter as tk

from display_module.gui.simulation.interaction_panel_views.notifications_view.notification_card import NotificationCard


class NotificationsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2a2a2a")

        header = tk.Label(
            self,
            text="Notifications",
            font=("Arial", 20),
            bg="#2a2a2a",
            fg="white"
        )

        header.pack(
            anchor="w",
            padx=10,
            pady=10
        )

        # Notification list
        self.list_container = tk.Frame(
            self,
            bg="#2b2b2b"
        )
        self.list_container.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=5
        )

        # Hard-coded notification
        self.add_notification(
            "New message",
            "Player4 send you a new message"
        )
        self.add_notification(
            "Your unit was attacked",
            "Your unit of Light Infantry: light_infantry23 was attacked by heavy_infantry10 and had to retreat"
        )
        self.add_notification(
            "Command center was conquered",
            "You have conquered the command center of Player2"
        )

    def add_notification(self, title, description):
        card = NotificationCard(
            self.list_container,
            title,
            description
        )

        card.pack(
            fill="x",
            pady=4
        )