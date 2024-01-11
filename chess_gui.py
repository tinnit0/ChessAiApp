import chess.svg
import tkinter as tk
from PIL import Image, ImageTk
import chess

def setup_ui(self):
    self.menu_frame = tk.Frame(self.root)
    self.menu_frame.grid(row=0, column=8, rowspan=8, sticky="nsew")

    buttons = [
        ("Reset", self.reset_game),
        ("AI vs AI", self.ai_vs_ai),
        ("Player vs AI", self.human_vs_ai),
        ("Teaching Mode", self.start_teaching_mode),
        ("AI vs Stockfish (1000)", self.start_ai_vs_stockfish),
    ]

    for text, cmd in buttons:
        button = tk.Button(self.menu_frame, text=text, command=cmd)
        button.pack(pady=20)


def create_square(self, row, col):
    icon_size = 60
    border_width = 1
    color = '#d9d9d9' if (row + col) % 2 == 0 else '#a9a9a9'

    frame = tk.Frame(self.root, width=icon_size + 2 * border_width, height=icon_size + 2 * border_width,
                     bg=color, borderwidth=border_width, relief="solid")
    frame.grid(row=row, column=col, sticky="nsew")
    frame.grid_propagate(False)

    frame.bind("<Button-1>", lambda event, r=row,
               c=col: self.on_square_click(r, c))

    piece = self.board.piece_at(chess.square(col, 7 - row))
    if piece:
        image = self.get_piece_image(piece)

        label = tk.Label(frame, image=image, bg=color,
                         width=icon_size, height=icon_size, anchor="center")
        label.image = image
        label.pack(fill=tk.BOTH, expand=True)

        label.bind("<Button-1>", lambda event, r=row,
                   c=col: self.on_square_click(r, c))
    else:
        label = tk.Label(frame, text="", bg=color,
                         width=icon_size, height=icon_size)
        label.pack(fill=tk.BOTH, expand=True)

    for r in range(8):
        self.root.grid_rowconfigure(r, weight=1)
    for c in range(8):
        self.root.grid_columnconfigure(c, weight=1)
