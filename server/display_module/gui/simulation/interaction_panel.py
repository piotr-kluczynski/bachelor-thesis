import tkinter as tk

class InteractionPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2f2f2f", width=300)

        self.pack_propagate(False)