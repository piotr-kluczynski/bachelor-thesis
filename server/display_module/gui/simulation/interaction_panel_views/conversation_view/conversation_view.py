import tkinter as tk

from display_module.gui.simulation.interaction_panel_views.conversation_view.chat_panel import ChatPanel

class ConversationView(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent, bg="#3b3b3b")

        self.context = context
        self.players = self.context.player_names.items()

        # Main layout
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.grid_columnconfigure(0, weight=1)

        # Header
        header = tk.Label(
            self,
            text="Conversations",
            bg="#2a2a2a",
            fg="white",
            font=("Arial", 20),
            anchor="w",
            padx=10,
            pady=10
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        # Content frame
        content = tk.Frame(
            self,
            bg="#3b3b3b"
        )

        content.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        # content layout

        content.grid_rowconfigure(0, weight=1)

        content.grid_columnconfigure(0, weight=0)
        content.grid_columnconfigure(1, weight=1)

        # Contact list
        self.contacts_panel = tk.Frame(
            content,
            bg="#252525",
            width=220
        )

        self.contacts_panel.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # Chat panel
        self.chat_panel = ChatPanel(content, self.context)

        self.chat_panel.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.create_contact_buttons()

    def open_chat(self, player_id):
        self.chat_panel.load_conversation(player_id)

    def create_contact_buttons(self):
        for player in self.players:
            if player[0] is self.context.my_id:
                continue
            btn = tk.Button(
                self.contacts_panel,
                text=player[1], # Player Name
                anchor="w",
                relief="flat",
                bg="#333333",
                fg=self.context.players_colors[player[0]],
                command=lambda playerId=player[0]: self.open_chat(playerId)
            )

            btn.pack(
                fill="x",
                padx=5,
                pady=2
            )