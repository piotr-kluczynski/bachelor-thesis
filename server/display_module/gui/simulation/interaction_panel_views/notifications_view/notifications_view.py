import tkinter as tk

from display_module.gui.simulation.interaction_panel_views.notifications_view.notification_card import NotificationCard


class NotificationsView(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent, bg="#2a2a2a")

        self.context = context

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

        self.refresh_notification_list()


    def refresh_notification_list(self):
        for widget in self.list_container.winfo_children():
            widget.destroy()

        for notification in self.context.notifications:
            card = NotificationCard(
                self.list_container,
                notification.title,
                notification.description
            )

            card.pack(
                fill="x",
                pady=4
            )
