import chess
import random
import json
import pickle
import hashlib
import os
import torch
import numpy as np
import chess


class AI:
    PIECE_VALUES = {
        chess.PAWN: 10,
        chess.KNIGHT: 30,
        chess.BISHOP: 30,
        chess.ROOK: 50,
        chess.QUEEN: 90,
        chess.KING: 900
    }

    CENTRAL_SQUARES = [chess.D4, chess.E4, chess.D5, chess.E5]

    def __init__(self, num_games=1000, gamedata_folder='ChessAiApp\\gamedata', batch_size=64, epsilon=0.5, color=chess.WHITE):
        self.board = chess.Board()
        self.q_table = {}
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = epsilon
        self.num_games = num_games
        self.gamedata_folder = gamedata_folder
        self.batch_size = batch_size
        self.batch_data = []
        self.color = color

        q_table_path = os.path.join(self.gamedata_folder, 'q_table.pkl')

        os.makedirs(self.gamedata_folder, exist_ok=True)

        if os.path.exists(q_table_path):
            self.load_q_table(q_table_path)
        else:
            print("No existing Q-table found. Creating a new one.")
            self.save_q_table(q_table_path)

        self.load_q_table('ChessAiApp\\gamedata\\q_table.pkl')

    def board_hash(self, fen_str):
        hash_object = hashlib.sha256(fen_str.encode())
        return hash_object.hexdigest()

    def q_value(self, board, move):
        state_hash = self.board_hash(board.fen())
        return self.q_table.get((state_hash, move.uci()), 0)

    def update_q_values_batch(self):
        for state, move, reward, new_state in self.batch_data:
            self.update_q_value(state, move, reward, new_state)
        self.batch_data = []

    def make_ai_move(self, board):
        return self.choose_move(board)

    def choose_move(self, board, training_mode=False):
        legal_moves = list(board.legal_moves)

        if random.uniform(0, 1) < self.epsilon:
            chosen_move = random.choice(legal_moves)
            if training_mode:
                print(f"AI chose a random move during training: {
                      chosen_move.uci()}")
            return chosen_move

        history_q_values = [self.q_value(board, move) for move in legal_moves]
        if any(history_q_values):
            q_values = {move: self.q_value(board, move)
                        for move in legal_moves}
            max_q_value = max(q_values.values(), default=0)
            best_moves = [move for move, q_value in q_values.items()
                          if q_value == max_q_value]
            chosen_move = random.choice(best_moves)
            if training_mode:
                print(f"AI chose the best move from history during training: {
                      chosen_move.uci()}")
            return chosen_move

        chosen_move = random.choice(legal_moves)
        if training_mode:
            print(f"AI chose a random move during training: {
                  chosen_move.uci()}")
        return chosen_move

    def evaluate_position(self, board):
        evaluation = torch.tensor(0.0)

        for move in board.legal_moves:
            if board.is_capture(move) and not board.gives_check(move):
                new_board = board.copy()
                new_board.push(move)
                if not new_board.is_attacked_by(not new_board.turn, move.to_square):
                    evaluation += self.PIECE_VALUES[new_board.piece_at(
                        move.to_square).piece_type]

        for square in self.CENTRAL_SQUARES:
            piece = board.piece_at(square)
            if piece:
                if piece.piece_type == chess.PAWN:
                    evaluation += torch.tensor(5.0)
                elif piece.piece_type == chess.KNIGHT:
                    evaluation += torch.tensor(10.0)

        for color in [chess.WHITE, chess.BLACK]:
            for square in board.pieces(color, chess.PAWN):
                evaluation += torch.tensor(
                    5.0) if color == chess.WHITE else torch.tensor(-5.0)

            for square in board.pieces(color, chess.KNIGHT):
                evaluation += torch.tensor(
                    10.0) if color == chess.WHITE else torch.tensor(-10.0)

            evaluation += torch.sum(torch.tensor(self.PIECE_VALUES[piece.piece_type]) * (
                torch.tensor(1) if piece.color == chess.WHITE else torch.tensor(-1)) for piece in board.pieces)

        white_king_square = board.king(chess.WHITE)
        black_king_square = board.king(chess.BLACK)
        evaluation += -50 * torch.tensor(
            white_king_square in self.CENTRAL_SQUARES) + 50 * torch.tensor(black_king_square in self.CENTRAL_SQUARES)

        return evaluation

    def learn_from_data(self, board, move, new_board):
        state = board.fen()
        new_state = new_board.fen()

        if new_board.is_checkmate():
            reward = -1000 if new_board.turn == chess.WHITE else 1000
        else:
            material_value = torch.tensor(sum([self.PIECE_VALUES[piece.piece_type] for piece in new_board.pieces(chess.WHITE, True)]) -
                                          sum([self.PIECE_VALUES[piece.piece_type]
                                               for piece in new_board.pieces(chess.BLACK, True)]))
            positional_value = torch.tensor(self.evaluate_position(new_board))

            reward = material_value + positional_value

        self.batch_data.append((state, move, reward.item(), new_state))

        if len(self.batch_data) >= self.batch_size:
            self.update_q_values_batch()

    def save_q_table(self, q_table_path):
        with open(q_table_path, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, q_table_path):
        if os.path.exists(q_table_path) and os.path.getsize(q_table_path) > 0:
            with open(q_table_path, 'rb') as f:
                self.q_table = pickle.load(f)
        else:
            print(
                f"Q-table file '{q_table_path}' is empty or does not exist. Initializing a new Q-table.")
            self.q_table = {}

        print(f"Q-table loaded from {q_table_path}")

    def save_q_table(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.q_table, f)
        print(f"Q-table saved to {path}")

    def load_game_data(self):
        hash_file_path = 'ChessAiApp\\gamedata\\game_hashes.txt'

        try:
            with open(hash_file_path, 'r') as hash_file:
                unique_hashes = set(hash_file.read().splitlines())
        except FileNotFoundError:
            unique_hashes = set()
            with open(hash_file_path, 'w'):
                pass

        for game_hash in unique_hashes:
            game_data = self.retrieve_game_data(game_hash)

            if game_data:
                self.process_game_data(game_data)

    def save_game_data(self, game_data):
        game_data_str = json.dumps(game_data)
        game_hash = hashlib.sha256(game_data_str.encode()).hexdigest()

        hash_file_path = 'ChessAiApp\\gamedata\\game_hashes.txt'
        game_data_file_path = 'ChessAiApp\\gamedata\\game_data.json'

        if game_data['result'] in ['win', 'loss'] or random.random() < 0.1:
            with open(hash_file_path, 'a') as hash_file:
                hash_file.write(game_hash + '\n')

            with open(game_data_file_path, 'a') as game_data_file:
                game_data_file.write(game_data_str + '\n')

            print(f"Game data saved - Hash: {game_hash}")
