import tkinter as tk
from PIL import Image, ImageTk
import chess
import os
from tkinter import messagebox
from chess_ai import AI
import chess.engine
import threading    


class chess_control:
    def __init__(self, chessapp_instance):
        self.chessapp = chessapp_instance
        self.root = self.chessapp.root
        self.board = chess.Board()
        self.ai_instance = AI()

    def player_vs_ai():
        
    def run_stockfish_moves(self, stockfish):
        while not self.board.is_game_over():
            result = stockfish.play(self.board, chess.engine.Limit(time=0.1))
            self.board.push(result.move)

            from_square = result.move.from_square
            to_square = result.move.to_square

            row_from, col_from = 7 - (from_square // 8), from_square % 8
            row_to, col_to = 7 - (to_square // 8), to_square % 8

            self.chess_control.update_square(col_from, row_from)
            self.chess_control.update_square(col_to, row_to)

            self.root.update_idletasks()
            self.root.update()
            self.chess_control.update_square(row_to, col_to)

    def start_ai_vs_stockfish(self):
        try:
            stockfish_rating = 1000
            stockfish_path = "C:\\Project\\ChessAiApp\\stockfish"
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

            self.root.after(100, lambda: self.run_stockfish_moves(stockfish))
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def ai_vs_ai(self, teach_mode=False):
        ai_moves = []

        while not self.board.is_game_over():
            move = self.ai.choose_move(self.board)

            if move and move in self.board.legal_moves:
                self.board.push(move)
                print(f"Making AI move: {move.uci()}")

                if not teach_mode:
                    self.chess_control.update_square(move.from_square %
                                                    8, 7 - (move.from_square // 8))
                    self.chess_control.update_square(move.to_square %
                                                    8, 7 - (move.to_square // 8))

                ai_moves.append(move)

                self.root.after(self.teaching_speed_limit if self.teaching else self.ai_delay,
                                lambda: self.chess_control.batch_update_ai_moves(ai_moves, teach_mode=teach_mode))
            else:
                print("AI cannot find a legal move.")
                self.chess_control.reset_game_and_continue_ai()

            while not self.board.is_game_over() and self.board.turn == chess.BLACK:
                move = self.ai.choose_move(self.board)
                ai_moves.append(move)
                self.board.push(move)

            if ai_moves:
                self.root.after(self.teaching_speed_limit if self.teaching else self.ai_delay,
                                lambda: self.chess_control.batch_update_ai_moves(ai_moves, teach_mode=teach_mode))
