from concurrent.futures import ProcessPoolExecutor, as_completed
import chess
from chess_ai import AI


def play_game(ai_instance, game_num):
    board = chess.Board()

    while not board.is_game_over():
        move = ai_instance.choose_move(board)
        if move in board.legal_moves:
            board.push(move)
        else:
            print(
                f"Illegal move attempted by AI in game {game_num}: {move.uci()}")
            break

    if board.result() == "1-0":
        game_outcome = 'win'
    elif board.result() == "0-1":
        game_outcome = 'loss'
    else:
        game_outcome = 'draw'

    game_data = {
        'result': game_outcome,
        'moves': [(move.uci(), board.piece_at(move.from_square).piece_type)
                  if board.piece_at(move.from_square)
                  else (move.uci(), None)
                  for move in board.move_stack]
    }

    ai_instance.save_game_data(game_data)

    print(f"Game {game_num} completed with outcome: {game_outcome}")
    return game_data

def train_ai_parallel(num_games, num_processes, ai_instance):
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = {executor.submit(
            play_game, ai_instance, game_num): game_num for game_num in range(num_games)}
        for future in as_completed(futures):
            game_num = futures[future]
            try:
                game_data = future.result()
                print(
                    f"Game {game_num} completed with outcome: {game_data['result']}")
            except Exception as e:
                print(f"Error in game {game_num}: {e}")

    print("All games completed.")

if __name__ == "__main__":
    train_ai_parallel(num_games=10, num_processes=4)
