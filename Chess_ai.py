import chess
import random
import json
import pickle
import hashlib
import os


class AI:
    PIECE_VALUES = {
        chess.PAWN: 10,
        chess.KNIGHT: 30,
        chess.BISHOP: 30,
        chess.ROOK: 50,
        chess.QUEEN: 90,
        chess.KING: 900
    }

    def __init__(self, num_games=1000):
        self.q_table = {}
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.2
        self.num_games = num_games

    def board_hash(self, fen_str):
        hash_object = hashlib.sha256(fen_str.encode())
        return hash_object.hexdigest()

    def q_value(self, board, move):
        state_hash = self.board_hash(board)
        return self.q_table.get((state_hash, move.uci()), 0)

    def update_q_value(self, board, move, reward, new_board):
        state_hash = self.board_hash(board)
        new_state_hash = self.board_hash(new_board)

        max_future_q = max([self.q_value(new_board, future_move)
                           for future_move in new_board.legal_moves], default=0)
        current_q = self.q_value(board, move)
        self.q_table[(state_hash, move.uci())] = current_q + \
            self.alpha * (reward + self.gamma * max_future_q - current_q)

    def make_ai_move(self, board):
        return self.choose_move(board)

    def choose_move(self, board):
        state = board.fen()
        legal_moves = list(board.legal_moves)

        if random.uniform(0, 1) < self.epsilon:
            return random.choice(legal_moves)

        q_values = {move: self.q_value(state, move) for move in legal_moves}
        max_q_value = max(q_values.values(), default=0)
        best_moves = [move for move, q_value in q_values.items()
                    if q_value == max_q_value]

        return random.choice(best_moves)

    CENTRAL_SQUARES = [chess.D4, chess.E4, chess.D5, chess.E5]

    def evaluate_position(self, board):
        evaluation = 0

        for move in board.legal_moves:
            if board.is_capture(move) and not board.gives_check(move):
                board.push(move)
                if not board.is_attacked_by(not board.turn, move.to_square):
                    evaluation += self.PIECE_VALUES[board.piece_at(move.to_square).piece_type]
                board.pop()
        
        for square in self.CENTRAL_SQUARES:
            piece = board.piece_at(square)
            if piece:
                if piece.piece_type == chess.PAWN:
                    evaluation += 5
                elif piece.piece_type == chess.KNIGHT:
                    evaluation += 10
        
        evaluation += 0.1 * len(list(board.legal_moves))
        
        if board.king(chess.WHITE) in self.CENTRAL_SQUARES:
            evaluation -= 50
        if board.king(chess.BLACK) in self.CENTRAL_SQUARES:
            evaluation += 50
        
        return evaluation

    def learn_from_data(self, board, move, new_board):
        state = board.fen()
        new_state = new_board.fen()

        if new_board.is_checkmate():
            reward = -1000 if new_board.turn == chess.WHITE else 1000
        else:
            material_value = sum([self.PIECE_VALUES[piece.piece_type] for piece in new_board.pieces(chess.WHITE, True)]) - \
                             sum([self.PIECE_VALUES[piece.piece_type] for piece in new_board.pieces(chess.BLACK, True)])
            positional_value = self.evaluate_position(new_board)
            
            reward = material_value + positional_value

        self.update_q_value(state, move, reward, new_state)

    def save_q_table(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, path):
        with open(path, 'rb') as f:
            self.q_table = pickle.load(f)
    
def save_game_data(self, game_data):
    game_data_str = json.dumps(game_data)
    game_hash = hashlib.sha256(game_data_str.encode()).hexdigest()

    directory_path = os.path.join(os.getcwd(), 'game_data')
    os.makedirs(directory_path, exist_ok=True)

    game_data_file_path = os.path.join(directory_path, f'game_data_{game_hash}.json')
    hash_file_path = os.path.join(directory_path, 'game_hashes.txt')

    print(f"Saving Game Data to: {game_data_file_path}")
    print(f"Saving Game Hash to: {hash_file_path}")

    with open(hash_file_path, 'a') as hash_file:
        hash_file.write(game_hash + '\n')

    with open(game_data_file_path, 'w') as data_file:
        json.dump(game_data, data_file)

    print("Game Data Saved Successfully.")


    def retrieve_game_data(self, game_hash):
        game_data_file_path = f'game_data_{game_hash}.json'
        try:
            with open(game_data_file_path, 'r') as data_file:
                game_data = json.load(data_file)
            return game_data
        except FileNotFoundError:
            return None

    def load_game_data(self):
        try:
            with open('game_hashes.txt', 'r') as hash_file:
                unique_hashes = set(hash_file.read().splitlines())
        except FileNotFoundError:
            unique_hashes = set()

        for game_hash in unique_hashes:
            game_data = self.retrieve_game_data(game_hash)

            if game_data:
                self.process_game_data(game_data)

    def process_game_data(self, game_data):
        result = game_data['result']
        moves = game_data['moves']

        print(f"Processed game data - Result: {result}, Moves: {moves}")
