import tkinter as tk

class ChatPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#3a3a3a")

        self.current_player = None

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

    def load_conversation(self, player):
        self.current_player = player

        # Hardcoded chat history
        history = [
            f"{player}: Hello there",
            f"You: General Kenobi!"
        ]

        self.messages.config(state="normal")
        self.messages.delete("1.0", tk.END)

        for msg in history:
            self.messages.insert(tk.END, msg + "\n")
        self.messages.config(state="disabled")

    def send_message(self):
        text = self.input.get()

        if not text:
            return

        self.messages.config(state="normal")

        self.messages.insert(
            tk.END,
            f"You: {text}\n"
        )
        self.messages.config(state="disabled")
        self.input.delete(0, tk.END)