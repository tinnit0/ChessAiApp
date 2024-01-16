from PIL import Image, ImageTk
import chess
import os
from tkinter import messagebox
from Chess_ai import AI
import chess.engine
import threading
from Chess_board import draw_chessboard
import subprocess
import pygame
from queue import Queue

class chess_control:
    def __init__(self, chessapp_instance):
        self.chessapp_instance = chessapp_instance
        self.board = chess.Board()
        self.chess_ai = AI()
        self.stockfish_queue = Queue()

    def handle_option_selection(self, option):
        global board, player_turn, running
        if option == "Player vs AI" or option == "AI vs Stockfish":
            draw_chessboard()
            player_turn = True
            if option == "AI vs Stockfish":
                self.start_ai_vs_stockfish()
        elif option == "Training":
            self.launch_training_app()
        elif option == "Reset Board":
            draw_chessboard()
            player_turn = True

    def launch_training_app(self):
        subprocess.Popen(["python", "ChessAiApp\\chesstraining.py"])
        pygame.quit()

    def run_stockfish_moves(self, stockfish):
        global player_turn, running

        while not self.board.is_game_over():
            if not player_turn:
                result = stockfish.play(self.board, chess.engine.Limit(time=1.0))
                if result:
                    self.board.push(result.move)
                    player_turn = True
                    draw_chessboard()
                    self.stockfish_queue.put(True)

    def start_ai_vs_stockfish(self):
        try:
            stockfish_rating = 1000
            stockfish_path = "C:\\Users\\leusi\\Documents\\GitHub\\ChessAiApp\\stockfish\\"
            stockfish_executable = os.path.join(stockfish_path, "stockfish-windows-x86-64-avx2.exe")

            if not os.path.exists(stockfish_executable):
                raise FileNotFoundError(f"Stockfish executable not found: {stockfish_executable}")

            stockfish = chess.engine.SimpleEngine.popen_uci(stockfish_executable)

            self.board = chess.Board()
            player_turn = True


            stockfish_thread = threading.Thread(target=self.run_stockfish_moves, args=(stockfish,))
            stockfish_thread.start()

            while not self.board.is_game_over():
                if player_turn:
                    result = stockfish.play(self.board, chess.engine.Limit(time=1.0))
                    if result:
                        self.board.push(result.move)
                        self.stockfish_queue.get()
                    else:
                        break
                else:
                    ai_move = self.chess_ai.choose_move(self.board)
                    self.board.push(ai_move)

                player_turn = not player_turn  # Switch turns

                draw_chessboard()
            stockfish_thread.join()
             
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")