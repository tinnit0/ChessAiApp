import pygame
import chess
import time
from Chess_ai import AI
from chess_control import chess_control
from Chess_board import draw_chessboard
import pygame.mixer
import random


# deselect, win / lose / draw, stockfish, knoppen correct maken
pygame.init()
pygame.mixer.init()  
capture_sound = pygame.mixer.Sound('sounds/capture.mp3')
castle_sound = pygame.mixer.Sound('sounds/castle.mp3')
movecheck_sound = pygame.mixer.Sound('sounds/move-check.mp3')
moveself_sound = pygame.mixer.Sound('sounds/move-self.mp3')
promote_sound = pygame.mixer.Sound('sounds/promote.mp3')

WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
BROWN = (244, 164, 96)
HIGHLIGHT_COLOR = (0, 255, 0, 100)
chess_ai = AI()
board = chess.Board()
current_player_color = chess.WHITE

pieces = {
    'r': pygame.image.load('icons/rB.png'),
    'n': pygame.image.load('icons/nB.png'),
    'b': pygame.image.load('icons/bB.png'),
    'q': pygame.image.load('icons/QB.png'),
    'k': pygame.image.load('icons/kB.png'),        
    'p': pygame.image.load('icons/pB.png'),
    'R': pygame.image.load('icons/rW.png'),
    'N': pygame.image.load('icons/nW.png'),
    'B': pygame.image.load('icons/bW.png'),
    'Q': pygame.image.load('icons/QW.png'),
    'K': pygame.image.load('icons/kW.png'),
    'P': pygame.image.load('icons/pW.png'),
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

def play_sound(sound):
    sound.play()
    
def play_capture_sound():
    capture_sound.play()

def play_castle_sound():
    castle_sound.play()

def play_movecheck_sound():
    movecheck_sound.play()

def play_moveself_sound():
    moveself_sound.play()

def play_promote_sound():
    promote_sound.play()

def game_over():
    pass

def handle_promotion(move):
    global player_turn
    if chess.square_rank(move.to_square) in [0, 7]:
        piece_at_square = board.piece_at(move.to_square)
        if piece_at_square is not None and piece_at_square.piece_type == chess.PAWN:
            if chess.square_rank(move.to_square) == 0:
                promotion_piece = input("Choose promotion piece (Q, R, B, N): ").upper()
                if promotion_piece in ['Q', 'R', 'B', 'N']:
                    promotion_piece = chess.Piece.from_symbol(promotion_piece)
                    promotion_move = chess.Move(move.from_square, move.to_square, promotion_piece)
                    board.push(promotion_move)
            else:
                promotion_piece = chess.QUEEN
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


def ai_make_move():
    global player_turn
    if not player_turn:
        move = chess_ai.choose_move(board)
        print(f"AI chose a move: {move.uci()}")
        time.sleep(1)
        board.push(move)
        player_turn = True

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
        pass
            
chess_control_instance = chess_control(chess_control)
running = True
player_turn = random.choice([True, False])
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
            elif options_button.collidepoint(event.pos):
                invert_colors = not invert_colors
            elif player_turn:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // SQUARE_SIZE
                    row = 7 - event.pos[1] // SQUARE_SIZE
                    square = chess.square(col, row)
                    piece = board.piece_at(square)
                

                    if not selecting:
                        if current_player_color == chess.WHITE:
                            selecting = True
                            selected_square = square
                            legal_moves = set([move.to_square for move in board.legal_moves if move.from_square == selected_square])
                    else:
                        if square in legal_moves:
                            move = chess.Move(selected_square, square)
                            if move in board.legal_moves:
                                if board.is_capture(move):
                                    play_sound(capture_sound)
                                elif board.is_castling(move):
                                    play_sound(castle_sound)
                                elif board.is_check():
                                    play_sound(movecheck_sound)
                                else:
                                    play_sound(moveself_sound)
                                handle_promotion(move)
                                board.push(move)
                                player_turn = False
                                selecting = False
                                selected_square = None
                                legal_moves = set()
                            else:
                                selecting = False
                                selected_square = None
                                legal_moves = set()
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
                    else:
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
        time.sleep(0.5)
        ai_move = chess_ai.choose_move(board)
        captured_piece = board.piece_at(ai_move.to_square)
        if captured_piece:
            play_sound(capture_sound)
        elif board.is_castling(ai_move):
            play_sound(castle_sound)
        elif board.is_check():
            play_sound(movecheck_sound)
        else:
            play_sound(moveself_sound)
        board.push(ai_move)
        player_turn = True if current_player_color == chess.WHITE else False

pygame.quit()