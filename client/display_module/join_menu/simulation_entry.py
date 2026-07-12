import tkinter as tk

BACKGROUND_COLOR = "#1e1e1e"
PANEL_COLOR = "#262626"
TEXT_COLOR = "#f0f0f0"
SECONDARY_COLOR = "#b0b0b0"
ACCENT_COLOR = "#3b3b3b"

class SimulationEntry(tk.Frame):
    def __init__(self, parent, name, no_players, max_no_players):
        tk.Frame.__init__(self, parent)

        self.configure(bg=BACKGROUND_COLOR)

        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)

        # Title of the simulation
        self.title = tk.Label(
            self,
            text=name,
            fg=TEXT_COLOR,
            bg=PANEL_COLOR,
            font=("Segue UI", 14, "bold")
        )
        self.title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=8
        )

        # Simulation player status
        self.player_status = tk.Label(
            self,
            text=f"{no_players}/{max_no_players}",
            fg=TEXT_COLOR,
            bg=PANEL_COLOR,
            font=("Segue UI", 12)
        )
        self.player_status.grid(
            row=0,
            column=1,
            padx=20,
            pady=8
        )

        # Join button
        self.join_button = tk.Button(
            self,
            text="Join",
            font=("Segue UI", 11),
            bg=PANEL_COLOR,
            fg=TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground="#505050",
            padx=20,
            command=lambda: print(f"Simulation {name} joined!")
        )
        self.join_button.grid(
            row=0,
            column=2,
            padx=15,
            pady=8
        )

        # Hover effect for the tile
        def enter(event):
            self.title.configure(bg="#343434")
            self.join_button.configure(bg="#343434")
            self.player_status.configure(bg="#343434")
            self.configure(bg="#343434")

        def leave(event):
            self.title.configure(bg=BACKGROUND_COLOR)
            self.join_button.configure(bg=BACKGROUND_COLOR)
            self.player_status.configure(bg=BACKGROUND_COLOR)
            self.configure(bg=BACKGROUND_COLOR)

        self.bind("<Enter>", enter)
        self.bind("<Leave>", leave)

        # Disabling the button if the simulation lobby is full
        if no_players >= max_no_players:
            self.join_button.config(
                state="disabled"
            )