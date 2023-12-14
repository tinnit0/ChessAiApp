from concurrent.futures import ProcessPoolExecutor, as_completed
from queue import Queue
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

    game_outcome = 'win' if board.result(
    ) == "1-0" else 'loss' if board.result() == "0-1" else 'draw'
    game_data = {
        'result': game_outcome,
        'moves': [(move.uci(), board.piece_at(move.from_square).piece_type)
                  if board.piece_at(move.from_square)
                  else (move.uci(), None)
                  for move in board.move_stack]
    }

    try:
        ai_instance.save_game_data(game_data)
        print(f"Game {game_num} completed with outcome: {game_outcome}")
    except Exception as e:
        print(f"Error saving game data in game {game_num}: {e}")

    return game_data


def train_ai_parallel(ai_instance, num_games, num_processes, progress_queue):
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = {executor.submit(
            play_game, ai_instance, game_num): game_num for game_num in range(num_games)}

        for i, future in enumerate(as_completed(futures)):
            game_num = futures[future]
            try:
                game_data = future.result()
                progress_queue.put(
                    (i, f"Game {game_num} completed with outcome: {game_data['result']}", 100))
            except Exception as e:
                progress_queue.put((i, f"Error in game {game_num}: {e}", 0))

    print("All games completed.")