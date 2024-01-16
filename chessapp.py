import pygame
import chess
import time
from Chess_ai import AI
from chess_control import chess_control
from Chess_board import draw_chessboard
from chess import Move, QUEEN

pygame.init()

WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
BROWN = (244, 164, 96)
HIGHLIGHT_COLOR = (0, 255, 0, 100)
chess_ai = AI()
board = chess.Board()

pieces = {
    'r': pygame.image.load('ChessAiApp/icons/rB.png'),
    'n': pygame.image.load('ChessAiApp/icons/nB.png'),
    'b': pygame.image.load('ChessAiApp/icons/bB.png'),
    'q': pygame.image.load('ChessAiApp/icons/QB.png'),
    'k': pygame.image.load('ChessAiApp/icons/kB.png'),
    'p': pygame.image.load('ChessAiApp/icons/pB.png'),
    'R': pygame.image.load('ChessAiApp/icons/rW.png'),
    'N': pygame.image.load('ChessAiApp/icons/nW.png'),
    'B': pygame.image.load('ChessAiApp/icons/bW.png'),
    'Q': pygame.image.load('ChessAiApp/icons/QW.png'),
    'K': pygame.image.load('ChessAiApp/icons/kW.png'),
    'P': pygame.image.load('ChessAiApp/icons/pW.png'),
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chessboard")

selecting = False
selected_square = None
legal_moves = set()

font = pygame.font.Font(None, 27)
options_button = pygame.Rect(10, 10, 80, 30)
options_text = font.render("Options", True, (150, 150, 150))

options_menu = pygame.Rect(150, 50, 300, 200)
menu_font = pygame.font.Font(None, 30)
options_text_list = ["2 Player", "Player vs AI", "AI vs Stockfish", "Training", "Reset Board"]
option_rects = [pygame.Rect(options_menu.left + 10, options_menu.top + 10 + i * 40, options_menu.width - 20, 30) for i in range(len(options_text_list))]


def handle_promotion(move):
    if chess.square_rank(move.to_square) in [0, 7] and board.piece_at(move.to_square).piece_type == chess.PAWN:
        promotion_piece = QUEEN
        promotion_move = chess.Move(move.from_square, move.to_square, promotion_piece)
        board.push(promotion_move)

def draw_pieces():
   for row in range(8):
        for col in range(8):
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece is not None:
                img = pieces[piece.symbol()]

                center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2

                img_rect = img.get_rect(center=(center_x, center_y))

                screen.blit(img, img_rect)

def draw_legal_moves(square):
    for move in board.legal_moves:
        if move.from_square == square:
            col, row = chess.square_file(move.to_square), 7 - chess.square_rank(move.to_square)
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

def ai_make_move(self):
    if not self.player_turn:
        move = self.chess_ai.choose_move(self.board)
        print(f"AI chose a move: {move.uci()}")
        # Add a delay of 1 second before making the move
        time.sleep(1)
        self.board.push(move)
        self.player_turn = True

def draw_options_menu():
    pygame.draw.rect(screen, (100, 100, 100), options_menu)
    for i, option_rect in enumerate(option_rects):
        pygame.draw.rect(screen, (150, 150, 150), option_rect)
        text = menu_font.render(options_text_list[i], True, WHITE)
        screen.blit(text, (option_rect.left + 10, option_rect.centery - text.get_height() // 2))

def handle_options_click(pos):
    global options_menu_open
    for i, option_rect in enumerate(option_rects):
        if option_rect.collidepoint(pos):
            chess_control_instance.handle_option_selection(options_text_list[i])
            options_menu_open = False

    def handle_option_selection(self, option):
        global board, player_turn
        if option == "Player vs AI" or option == "AI vs Stockfish":
            self.reset_board()
            player_turn = True
            if option == "AI vs Stockfish":
                self.start_ai_vs_stockfish()
        elif option == "Training":
            # rederect naar chesstraining
            pass
        elif option == "Reset Board":
            self.reset_board()
            player_turn = True
            
chess_control_instance = chess_control(chess_control)
running = True
player_turn = True
options_menu_open = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if options_button.collidepoint(event.pos):
                options_menu_open = not options_menu_open
            elif options_menu_open:
                handle_options_click(event.pos)
            elif player_turn:
                col = event.pos[0] // SQUARE_SIZE
                row = 7 - event.pos[1] // SQUARE_SIZE
                square = chess.square(col, row)
                piece = board.piece_at(square)

                if not selecting:
                    if piece is not None and piece.color == chess.WHITE:
                        selecting = True
                        selected_square = square
                        legal_moves = set([move.to_square for move in board.legal_moves if move.from_square == selected_square])
                else:
                    if square in legal_moves:
                        move = chess.Move(selected_square, square)
                        if move in board.legal_moves:
                            handle_promotion(move)
                            board.push(move)
                            player_turn = False
                            selecting = False
                            selected_square = None
                            legal_moves = set()

    draw_chessboard()
    draw_pieces()
    if selecting:
        draw_legal_moves(selected_square)

    pygame.draw.rect(screen, (100, 100, 100), options_button)
    screen.blit(options_text, (options_button.left + 5, options_button.top + 5))

    if options_menu_open:
        draw_options_menu()

    pygame.display.flip()

    if not player_turn and not board.is_game_over() and not options_menu_open:
        ai_move = chess_ai.make_ai_move(board)
        board.push(ai_move)
        player_turn = True

pygame.quit()