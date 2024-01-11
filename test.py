import pygame
import sys
import os
import chess
import io
import random

pygame.init()

WIDTH, HEIGHT = 520, 520
GRID_SIZE = 8
SQUARE_SIZE = WIDTH // GRID_SIZE
BORDER_SIZE = 0
WHITE = (255, 255, 255)
BROWN = (175, 135, 100)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")

class MockChessPiece:
    def __init__(self, symbol, color):
        self.symbol = lambda: symbol
        self.color = color

image_cache = {}

def get_piece_image(piece):
    image_name = piece_to_image_name(piece)
    if image_name not in image_cache:
        image_path = os.path.join("ChessAiApp\\Icons", image_name)
        loaded_image = pygame.image.load(image_path)
        loaded_image = pygame.transform.scale(
            loaded_image, (SQUARE_SIZE, SQUARE_SIZE))
        image_cache[image_name] = loaded_image
    return image_cache[image_name]

def piece_to_image_name(piece):
    return f"{piece.symbol().lower()}{'W' if piece.color == 'white' else 'B'}.png"

def make_random_move(board, side):
    legal_moves = [str(move) for move in board.legal_moves]
    return random.choice(legal_moves)

board = chess.Board()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE + BORDER_SIZE,
                                             row * SQUARE_SIZE + BORDER_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                mock_piece = MockChessPiece(
                    piece.symbol(), "white" if piece.color == chess.WHITE else "brown")
                piece_img = get_piece_image(mock_piece)

                piece_position = (
                    col * SQUARE_SIZE + BORDER_SIZE,
                    row * SQUARE_SIZE + BORDER_SIZE
                )

                screen.blit(pygame.transform.scale(piece_img, (SQUARE_SIZE, SQUARE_SIZE)),
                            piece_position)