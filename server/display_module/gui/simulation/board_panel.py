import math
import tkinter as tk

HEX_SIZE = 40

class BoardPanel(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent, bg="#3a3a3a")

        self.context = context
        self.board = context.board

        self.canvas = tk.Canvas(
            self,
            bg="#222222"
        )

        self.canvas.pack(fill="both", expand=True)

        # MAPPING
        # canvas_id -> coordinates
        self.hex_items = {}

        # Coordinates -> canvas_id
        self.coord_items = {}

        self.draw_board()

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
        for (q, r, s), tile in self.game_board.tiles.items():
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

    # Event handlers
    def on_hex_click(self, event):
        item = self.canvas.find_withtag("current")[0]
        coords = self.hex_items[item]
        print("Clicked:", coords)
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