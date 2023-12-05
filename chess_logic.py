
import chess
from chess_ai import AI
from multiprocessing import Manager, Pool
from functools import partial


def play_game(args):
    ai, game_num, num_games, save_callback = args
    board = chess.Board()
    while not board.is_game_over():
        move = ai.choose_move(board)
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
    save_callback(game_num)

    return game_data


def train_ai_parallel(ai, num_games=1000, num_processes=4):
    progress = Manager().Value('i', 0)
    game_data_list = Manager().list()
    
    def save_game_data_callback(game_num, game_data_list):
        if game_num % 10 == 0:
            print(f"Completed {game_num} games out of {num_games}")

        game_data_list.append(game_num)

    partial_callback = partial(
        save_game_data_callback, game_data_list=game_data_list)

    with Pool(num_processes) as pool:
        pool.starmap(play_game, [
            (ai, i, num_games, partial_callback) for i in range(num_games)
        ])

    pool.close()
    pool.join()

    for game_data in game_data_list:
        ai.save_game_data(game_data)

    print("All games completed.")
