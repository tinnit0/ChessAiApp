import tkinter as tk
from PIL import Image, ImageTk
import chess
import os
import subprocess
from tkinter import messagebox
from chess_ai import AI
import chess.engine
import sys
from stockfish import Stockfish
import chess.pgn
import threading
import queue

class chessapp:
    def __init__(self, root, ai):
        self.board = chess.Board()
        self.root = root
        self.ai = ai
        self.selected_piece = None
        self.ai_delay = 1000
        self.image_cache = {}
        self.scores = {'white': 0, 'black': 0, 'draw': 0}
        self.teaching = False
        self.teaching_speed_limit = 5
        self.ai_instance = AI()

        self.setup_ui()
        self.update_score_display()
        self.stockfish_queue = queue.Queue()

        self.draw_board()
        pass

    def setup_ui(self):
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.grid(row=0, column=8, rowspan=8, sticky="nsew")

        buttons = [
            ("Reset", self.reset_game),
            ("AI vs AI", self.ai_vs_ai),
            ("Human vs AI", self.human_vs_ai),
            ("Teaching Mode", self.start_teaching_mode),
            ("AI vs Stockfish (1000)", self.start_ai_vs_stockfish),
        ]

        for text, cmd in buttons:
            button = tk.Button(self.menu_frame, text=text, command=cmd)
            button.pack(pady=20)

    def piece_to_image_name(self, piece):
        return f"{piece.symbol().lower()}{'W' if piece.color == chess.WHITE else 'B'}.png"

    def get_piece_image(self, piece):
        image_name = self.piece_to_image_name(piece)
        if image_name not in self.image_cache:
            image_path = os.path.join(
                "ChessAiApp\\Icons", image_name)
            self.image_cache[image_name] = ImageTk.PhotoImage(
                Image.open(image_path))
        return self.image_cache[image_name]

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                self.create_square(row, col)

    def create_square(self, row, col):
        color = 'brown' if (row + col) % 2 == 0 else 'white'
        frame = tk.Frame(self.root, width=60, height=60, bg=color)
        frame.grid(row=row, column=col)
        frame.bind("<Button-1>", lambda event, r=row,
                   c=col: self.on_square_click(r, c))

        piece = self.board.piece_at(chess.square(col, 7 - row))
        if piece:
            label = tk.Label(
                frame, image=self.get_piece_image(piece), bg=color)
            label.image = self.get_piece_image(piece)
            label.pack(fill=tk.BOTH, expand=True)
            label.bind("<Button-1>", lambda event, r=row,
                       c=col: self.on_square_click(r, c))
        else:
            frame.config(bg=color)

    def update_square(self, col, row):
        color = 'brown' if (row + col) % 2 == 0 else 'white'
        position = chess.square(col, 7 - row)
        piece = self.board.piece_at(position)
        frame = self.root.grid_slaves(row=row, column=col)[0]
        for widget in frame.winfo_children():
            widget.destroy()
        if piece:
            image = self.get_piece_image(piece)
            label = tk.Label(frame, image=image, bg=color)
            label.image = image
            label.pack(fill=tk.BOTH, expand=True)
            label.bind("<Button-1>", lambda event, row=row,
                       col=col: self.on_square_click(row, col))
        else:
            frame.config(bg=color)

    def update_score_display(self):
        try:
            self.score_label.destroy()
        except AttributeError:
            pass
        score_text = f"White: {self.scores['white']} | Black: {self.scores['black']} | Draw: {self.scores['draw']}"
        self.score_label = tk.Label(self.menu_frame, text=score_text)
        self.score_label.pack(pady=20)

    def move_piece(self, row, col, move):
        if move in self.board.legal_moves:
            self.board.push(move)
            self.selected_piece = None
            self.selected_label.config(
                bg=('brown' if (row + col) % 2 == 0 else 'white'))
            self.clear_highlights()
            self.update_square(move.from_square %
                               8, 7 - (move.from_square // 8))
            self.update_square(move.to_square % 8, 7 - (move.to_square // 8))

            if move.promotion:
                self.update_square(move.to_square %
                                   8, 7 - (move.to_square // 8))

            if move in [m for m in self.board.legal_moves if m.uci().endswith('e.p.')]:
                ep_rank = 5 if self.board.turn == chess.WHITE else 2
                ep_square = chess.square(move.to_square % 8, ep_rank)
                self.update_square(ep_square % 8, 7 - (ep_square // 8))

    def on_square_click(self, row, col):
        position = chess.square(col, 7 - row)
        piece = self.board.piece_at(position)
        print(f"Clicked on {piece} at ({row}, {col})")

        if self.selected_piece:
            move = chess.Move(self.selected_piece, position)
            if move in self.board.legal_moves:
                self.move_piece(row, col, move)

                if not self.board.is_game_over() and self.board.turn == chess.BLACK:
                    ai_move = self.ai.make_ai_move(self.board)
                    self.board.push(ai_move)
                    self.update_square(ai_move.from_square %
                                       8, 7 - (ai_move.from_square // 8))
                    self.update_square(ai_move.to_square %
                                       8, 7 - (ai_move.to_square // 8))
            else:
                self.selected_label.config(
                    bg=('brown' if (row + col) % 2 == 0 else 'white'))
                self.selected_piece = None

        elif piece and piece.color == chess.WHITE:
            self.clear_highlights()
            if self.selected_piece == position:
                self.selected_label.config(
                    bg=('brown' if (row + col) % 2 == 0 else 'white'))
                self.selected_piece = None
                self.highlight_legal_moves(position)
            else:
                self.selected_piece = position
                clicked_frame = self.root.grid_slaves(row=row, column=col)[0]
                self.selected_label = clicked_frame.winfo_children()[0]
                self.selected_label.config(bg='yellow')

    def run_stockfish_moves(self, stockfish):
        try:
            def make_ai_move():
                print("Making AI move...")
                if self.board.turn == chess.WHITE:
                    move = self.ai.choose_move(self.board)
                else:
                    result = stockfish.play(
                        self.board, chess.engine.Limit(time=2.0))
                    move = result.move

                self.board.push(move)
                self.update_stockfish_gui()

                if not self.board.is_game_over():
                    self.root.after(1000, make_stockfish_move)
                else:
                    print("Game over!")

            def make_stockfish_move():
                try:
                    print("Making Stockfish move...")
                    if self.board.turn == chess.BLACK:
                        result = stockfish.play(
                            self.board, chess.engine.Limit(time=2.0))
                        move = result.move
                        self.board.push(move)
                        self.update_stockfish_gui()
                except chess.engine.EngineTerminatedError as e:
                    print(f"Stockfish engine terminated: {e}")
                    return  # Terminate the thread gracefully

                if not self.board.is_game_over():
                    self.root.after(1000, make_ai_move)
                else:
                    print("Game over!")

            make_ai_move()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if stockfish.is_alive():
                stockfish.quit()
            self.stockfish_thread = None

    def update_stockfish_gui(self):
        self.update_square(
            self.board.move_stack[-1].from_square % 8, 7 - (self.board.move_stack[-1].from_square // 8))
        self.update_square(
            self.board.move_stack[-1].to_square % 8, 7 - (self.board.move_stack[-1].to_square // 8))

    def update_gui_after_stockfish_moves(self):
        self.root.after(100, self.perform_update_gui_after_stockfish_moves)


    def perform_update_gui_after_stockfish_moves(self):
        self.reset_game()
        self.root.update()
        self.root.update_idletasks()

    def start_ai_vs_stockfish(self):
        try:
            stockfish_rating = 1000
            stockfish_path = "C:\\xampp\\htdocs\\ChessAiApp\\stockfish"
            stockfish_executable = os.path.join(
                stockfish_path, "stockfish-windows-x86-64-avx2.exe")

            if not os.path.exists(stockfish_executable):
                raise FileNotFoundError(
                    f"Stockfish executable not found: {stockfish_executable}")

            stockfish = chess.engine.SimpleEngine.popen_uci(
                stockfish_executable)

            stockfish_thread = threading.Thread(
                target=self.run_stockfish_moves, args=(stockfish,), daemon=True)
            stockfish_thread.start()

            self.stockfish_thread = stockfish_thread

            self.root.after(
                100, lambda: self.check_stockfish_thread(self.stockfish_thread))
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def check_stockfish_thread(self, stockfish_thread):
        if stockfish_thread and stockfish_thread.is_alive():
            self.root.after(
                100, lambda: self.check_stockfish_thread(stockfish_thread))
        else:
            self.update_score_display()

    def reset_game(self):
        result = self.board.result()

        if result == "1-0":
            game_outcome = 'win'
            self.scores['white'] += 1
        elif result == "0-1":
            game_outcome = 'loss'
            self.scores['black'] += 1
        else:
            game_outcome = 'draw'
            self.scores['draw'] += 1

        self.update_score_display()

        game_data = {
            'result': game_outcome,
            'moves': [(move.uci(), self.board.piece_at(move.from_square).piece_type)
                    if self.board.piece_at(move.from_square)
                    else (move.uci(), None)
                    for move in self.board.move_stack]
        }

        self.ai_instance.save_game_data(game_data)
        self.board.reset()
        self.draw_board()

    def highlight_square(self, row, col):
        frame = self.root.grid_slaves(row=row, column=col)[0]
        color = 'gray' if (row + col) % 2 == 0 else 'lightgray'
        frame.config(bg=color)

    def clear_highlights(self):
        for row in range(8):
            for col in range(8):
                self.update_square(col, row)

    def highlight_legal_moves(self, position):
        self.clear_highlights()
        for move in self.board.legal_moves:
            if move.from_square == position:
                row, col = 7 - (move.to_square // 8), move.to_square % 8
                self.highlight_square(row, col)

    def ai_vs_ai(self, teach_mode=False):
        ai_moves = []

        while not self.board.is_game_over():
            move = self.ai.choose_move(self.board)

            if move and move in self.board.legal_moves:
                self.board.push(move)
                print(f"Making AI move: {move.uci()}")

                if not teach_mode:
                    self.update_square(move.from_square %
                                    8, 7 - (move.from_square // 8))
                    self.update_square(move.to_square %
                                    8, 7 - (move.to_square // 8))

                ai_moves.append(move) 

                self.root.after(self.teaching_speed_limit if self.teaching else self.ai_delay,
                                lambda: self.batch_update_ai_moves(ai_moves, teach_mode=teach_mode))
            else:
                print("AI cannot find a legal move.")
                self.reset_game_and_continue_ai()

            while not self.board.is_game_over() and self.board.turn == chess.BLACK:
                move = self.ai.choose_move(self.board)
                ai_moves.append(move)
                self.board.push(move)

            if ai_moves:
                self.root.after(self.teaching_speed_limit if self.teaching else self.ai_delay,
                                lambda: self.batch_update_ai_moves(ai_moves, teach_mode=teach_mode))

    def batch_update_ai_moves(self, moves, teach_mode=False):
        for move in moves:
            if move in self.board.legal_moves:
                self.board.push(move)
                print(f"Making AI move: {move.uci()}")

                if not teach_mode:
                    self.update_square(move.from_square %
                                    8, 7 - (move.from_square // 8))
                    self.update_square(move.to_square %
                                    8, 7 - (move.to_square // 8))

        self.root.after(self.teaching_speed_limit if self.teaching else self.ai_delay,
                        lambda: self.ai_vs_ai(teach_mode=teach_mode))


    def reset_game_and_continue_ai(self):
        self.reset_game()
        self.ai_vs_ai()
    
    def start_teaching_mode(self):

        python_path = sys.executable

        script_path = os.path.join(
            os.path.dirname(__file__), 'chesstraining.py')

        subprocess.Popen([python_path, script_path])
        sys.exit()
        
    def human_vs_ai(self):
        self.teaching = False
        self.ai_mode = False
        try:
            self.teaching_window.destroy()
        except tk.TclError:
            pass
        self.reset_game()

    def save_game_data(self, game_data):
        self.ai.save_game_data(game_data)


    def load_game_data(self):
        self.ai.load_game_data()


def start_program():
    root = tk.Tk()
    root.title("Chess App")
    ai_instance = AI()
    app = chessapp(root, ai_instance)
    root.after(100, app.check_stockfish_thread, app.stockfish_thread)
    root.mainloop()
    root.update_idletasks()
    root.update()


if __name__ == "__main__":
    start_program()