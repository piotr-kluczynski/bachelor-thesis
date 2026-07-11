import tkinter as tk

from message import Message


class ChatPanel(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent, bg="#3a3a3a")

        self.context = context
        self.current_player = context.players_ids[0]

        # Main grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Message area
        self.messages = tk.Text(
            self,
            bg="#1e1e1e",
            fg="white",
            state="disabled"
        )
        self.messages.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )

        # Player input
        bottom = tk.Frame(self, bg="#2a2a2a")
        bottom.grid(
            row=2,
            column=0,
            sticky="ew"
        )

        self.input = tk.Entry(bottom)

        self.input.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5,
            pady=5
        )

        send_btn = tk.Button(
            bottom,
            text="Send",
            command=self.send_message
        )

        send_btn.pack(side="right", padx=5, pady=5)

    def load_conversation(self, player_id):
        self.current_player = player_id
        conversation = [message for message in self.context.conversations.get(self.current_player)]

        self.messages.config(state="normal")
        self.messages.delete("1.0", tk.END)

        for msg in conversation:
            sender_name = self.context.player_names.get(msg.sender)
            self.messages.insert(tk.END, f"({sender_name}) {msg.content}\n")
        self.messages.config(state="disabled")

    def send_message(self):
        text = self.input.get()

        if not text:
            return

        if self.current_player is self.context.my_id:
            return

        message = Message(sender=self.context.my_id, recipient=self.current_player, content=text)
        self.context.send_message(message)
        self.load_conversation(message.recipient)

        # Clearing entry
        self.input.delete(0, tk.END)