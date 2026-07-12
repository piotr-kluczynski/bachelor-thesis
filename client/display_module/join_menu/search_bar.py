import tkinter as tk

BACKGROUND_COLOR = "#1e1e1e"
PANEL_COLOR = "#262626"
TEXT_COLOR = "#f0f0f0"
SECONDARY_COLOR = "#b0b0b0"
ACCENT_COLOR = "#3b3b3b"

class SearchBar(tk.Frame):
    def __init__(self, parent, context):
        tk.Frame.__init__(self, parent)

        self.context = context

        # Search bar
        self.configure(
            bg=PANEL_COLOR,
            highlightthickness=1,
            highlightbackground=ACCENT_COLOR,
        )

        # Search bar text entry
        self.text_entry = tk.Entry(
            self,
            width=40,
            font=("Segue UI", 12),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=ACCENT_COLOR,
            highlightcolor="#4a90e2"
        )
        self.text_entry.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # Search bar button
        self.button = tk.Button(
            self,
            text="Search",
            font=("Segue UI", 11, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground="#4a4a4a",
            activeforeground="white",
            bd=0,
            padx=15,
            cursor="hand2",
            command=self.Search
        )
        self.button.pack(
            side="right",
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # Adding hover effect to the search button
        def on_enter(event):
            event.widget["bg"] = "#4a4a4a"

        def on_leave(event):
            event.widget["bg"] = ACCENT_COLOR

        self.button.bind("<Enter>", on_enter)
        self.button.bind("<Leave>", on_leave)

        # Adding placeholder to the search entry
        placeholder = "Search..."

        self.text_entry.insert(0, placeholder)
        self.text_entry.config(fg=SECONDARY_COLOR)

        def clear_placeholder(event):
            if self.text_entry.get() == placeholder:
                self.text_entry.delete(0, tk.END)
                self.text_entry.config(fg=TEXT_COLOR)

        def restore_placeholder(event):
            if not self.text_entry.get():
                self.text_entry.insert(0, placeholder)
                self.text_entry.config(fg=SECONDARY_COLOR)

        self.text_entry.bind("<FocusIn>", clear_placeholder)
        self.text_entry.bind("<FocusOut>", restore_placeholder)

        # Binding the "Enter" button with the search action
        self.text_entry.bind(
            "Return",
            lambda e: self.Search()
        )

    def Search(self):
        keyword = self.text_entry.get()

        if keyword:
            self.context.SearchForSimulation(self.text_entry.get())
        else:
            self.context.ResetSimulationList()