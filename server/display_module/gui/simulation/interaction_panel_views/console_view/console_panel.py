import tkinter as tk

class ConsolePanel(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent, bg="#3a3a3a")

        self.context = context

        # Main grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Message area
        self.commands = tk.Text(
            self,
            bg="#1e1e1e",
            fg="white",
            state="disabled"
        )
        self.commands.grid(
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
            command=self.send_command
        )
        send_btn.pack(side="right", padx=5, pady=5)

        self.load_console()

    def load_console(self):
        history = self.context.console_content

        self.commands.config(state="normal")
        self.commands.delete("1.0", tk.END)

        for command in history:
            self.commands.insert(tk.END, command)
        self.commands.config(state="disabled")

    def send_command(self):
        text = self.input.get()

        if not text:
            return

        self.context.execute_command(text)
        self.load_console()

        # Clearing entry
        self.input.delete(0, tk.END)