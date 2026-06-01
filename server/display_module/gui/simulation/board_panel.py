import math
import tkinter as tk

from display_module.gui.simulation.unit_info_panel import UnitInfoPanel

HEX_SIZE = 40

class BoardPanel(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent, bg="#3a3a3a")

        self.context = context
        self.context.board_panel = self # Assign self as a reference - possibly look for better solutions later

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.grid_columnconfigure(0, weight=1)

        self.unit_items = {}

        # Board
        self.canvas = tk.Canvas(
            self,
            bg="#222222"
        )

        self.canvas.grid(
           row=0,
           column=0,
            sticky="nsew"
        )

        # Unit information panel
        self.unit_info_panel = UnitInfoPanel(self, self.context)
        self.unit_info_panel.grid(
            row=1,
            column=0,
            sticky="ew"
        )
        self.unit_info_panel.grid_remove()

        # MAPPING
        # canvas_id -> coordinates
        self.hex_items = {}

        # Coordinates -> canvas_id
        self.coord_items = {}

        self.draw_board()
        self.draw_units()

        self.canvas.config(
            scrollregion=self.canvas.bbox("all")
        )

        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.pan_board)

        # Setting canvas to the center
        self.after(100, lambda: self.center_camera_on(0, 0))

    # Dragging board
    def start_pan(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def pan_board(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    # Translating coordinates to hexes and opposite
    def hex_to_pixel(self, q, r):
        x = HEX_SIZE * 3/2 * q
        y = HEX_SIZE * math.sqrt(3) * (r + q/2)

        return x, y
    def get_hex_points(self, center_x, center_y):
        points = []

        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)

            x = center_x + HEX_SIZE * math.cos(angle_rad)
            y = center_y + HEX_SIZE * math.sin(angle_rad)

            points.extend([x, y])

        return points

    def draw_board(self):
        for (q, r, s), tile in self.context.board.tiles.items():
            center_x, center_y = self.hex_to_pixel(q, r)
            points = self.get_hex_points(center_x, center_y)
            color = "white"

            hex_id = self.canvas.create_polygon(
                points,
                fill=color,
                outline="black",
                width=2,
            )

            self.hex_items[hex_id] = (q, r, s)
            self.coord_items[(q, r, s)] = hex_id

            self.canvas.tag_bind(
                hex_id,
                "<Button-1>",
                self.on_hex_click
            )

            self.canvas.tag_bind(
                hex_id,
                "<Enter>",
                self.on_hex_hover_enter
            )

            self.canvas.tag_bind(
                hex_id,
                "<Leave>",
                self.on_hex_hover_leave
            )

    def draw_units(self):
        for unit_id, unit in self.context.units.items():
            q, r, s = unit.tile.q, unit.tile.r, unit.tile.s

            radius = HEX_SIZE * 0.5
            color = self.context.players_colors.get(unit.owner)
            center_x, center_y = self.hex_to_pixel(q, r)

            unit_canvas_id = self.canvas.create_oval(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                fill=color
            )

            self.canvas.tag_bind(
                unit_canvas_id,
                "<Button-1>",
                self.on_unit_click
            )

            self.unit_items[unit_canvas_id] = unit

    def center_camera_on(self, q, r):

        x, y = self.hex_to_pixel(q, r)

        bbox = self.canvas.bbox("all")

        world_x1, world_y1, world_x2, world_y2 = bbox

        world_width = world_x2 - world_x1
        world_height = world_y2 - world_y1

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        target_x = x - canvas_width / 2
        target_y = y - canvas_height / 2

        x_fraction = (target_x - world_x1) / world_width
        y_fraction = (target_y - world_y1) / world_height

        x_fraction = max(0, min(1, x_fraction))
        y_fraction = max(0, min(1, y_fraction))

        self.canvas.xview_moveto(x_fraction)
        self.canvas.yview_moveto(y_fraction)
    def show_unit_info(self, unit):
        self.unit_info_panel.set_data(unit)
        self.unit_info_panel.grid()

    # Event handlers
    def on_hex_click(self, event):
        item = self.canvas.find_withtag("current")[0]
        coords = self.hex_items[item]
        print("Clicked:", coords)

        # Hiding unit description
        self.unit_info_panel.grid_remove()
    def on_hex_hover_enter(self, event):
        item = self.canvas.find_withtag("current")[0]
        self.canvas.itemconfig(
            item,
            width=4
        )
    def on_hex_hover_leave(self, event):
        item = self.canvas.find_withtag("current")[0]

        self.canvas.itemconfig(
            item,
            width=2
        )
    def on_unit_click(self, event):
        item = self.canvas.find_withtag("current")[0]
        unit = self.unit_items[item]

        self.show_unit_info(unit)