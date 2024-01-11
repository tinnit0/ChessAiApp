import tkinter as tk
from PIL import Image, ImageTk
import chess
import chess.svg
import io


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


def create_square(root, row, col, board):
    squares = board.attacks(chess.E4)

    svg_data = chess.svg.board(board, squares=squares, size=350)
    svg_image = ImageTk.PhotoImage(Image.open(io.BytesIO(svg_data)))

    frame = tk.Frame(root)
    frame.grid(row=row, column=col, sticky="nsew")

    label = tk.Label(frame, image=svg_image)
    label.image = svg_image
    label.pack(fill=tk.BOTH, expand=True)

    return frame
