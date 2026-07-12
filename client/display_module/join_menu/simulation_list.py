import tkinter as tk

from display_module.join_menu.simulation_entry import SimulationEntry

BACKGROUND_COLOR = "#1e1e1e"
PANEL_COLOR = "#262626"
TEXT_COLOR = "#f0f0f0"
SECONDARY_COLOR = "#b0b0b0"
ACCENT_COLOR = "#3b3b3b"

class SimulationList(tk.Frame):
    def __init__(self, parent, simulation_list):
        tk.Frame.__init__(self, parent)

        self.configure(bg=PANEL_COLOR)

        # Canvas
        self.canvas = tk.Canvas(
            self,
            bg=PANEL_COLOR,
            bd=0,
            highlightthickness=0,
            relief="flat"
        )
        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Scrollable frame
        self.scrollable_frame = tk.Frame(
            self.canvas,
            bg=PANEL_COLOR
        )

        # Canvas window
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        def resize_canvas(event):
            self.canvas.itemconfigure(
                self.canvas_window,
                width=event.width
            )

        self.canvas.bind("<Configure>", resize_canvas)


        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Adding the scrollbar
        scrollbar = tk.Scrollbar(
            self,
            command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Configuring the scrollbar change with the mousewheel
        def _on_mousewheel(event):
            content_height = self.scrollable_frame.winfo_height()
            canvas_height = self.canvas.winfo_height()

            if content_height <= canvas_height:
                return

            self.canvas.yview_scroll(int(-event.delta/120), "units")
        self.bind_all("<MouseWheel>", _on_mousewheel)

        # Filling the list elements
        self.populate_list(simulation_list)

    def populate_list(self, simulation_list):
        for simulation_name, simulation_players in simulation_list.items():
            SimulationEntry(
                self.scrollable_frame,
                simulation_name,
                simulation_players[0],
                simulation_players[1]
            ).pack(fill="x")

    def refresh_list(self, simulation_list):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.populate_list(simulation_list)

        # Update scrolling region
        self.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
