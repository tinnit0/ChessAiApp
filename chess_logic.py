from concurrent.futures import ProcessPoolExecutor, as_completed
import chess

def play_game(self, ai_instance, game_num):
    board = chess.Board()

    while not board.is_game_over():
        move = ai_instance.choose_move(board)
        if move in board.legal_moves:
            board.push(move)
        else:
            print(f"Illegal move attempted by AI in game {
                    game_num}: {move.uci()}")
            break

    game_outcome = 'win' if board.result(
    ) == "1-0" else 'loss' if board.result() == "0-1" else 'draw'
    game_data = {
        'result': game_outcome,
        'moves': [(move.uci(), board.piece_at(move.from_square).piece_type) if board.piece_at(
            move.from_square) else (move.uci(), None) for move in board.move_stack]
    }

    try:
        ai_instance.save_game_data(game_data)
        print(f"Game {game_num} completed with outcome: {game_outcome}")
    except Exception as e:
        print(f"Error saving game data in game {game_num}: {e}")

    return game_data

def train_ai_parallel(self, ai_instance, num_games, num_processes):
    game_data_list = []

    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = {executor.submit(
            self.play_game, ai_instance, game_num): game_num for game_num in range(num_games)}

        for future in as_completed(futures):
            game_num = futures[future]
            try:
                game_data = future.result()
                game_data_list.append(game_data)
                print(f"Game {game_num} completed with outcome: {
                        game_data['result']}")
            except Exception as e:
                print(f"Error in game {game_num}: {e}")

    print("All games completed.")
    return game_data_list
