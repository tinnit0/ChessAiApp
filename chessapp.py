import pygame
import tkinter
import sys
#from chess_control import start_ai_vs_stockfish, player_vs_ai
from chess_ai import AI
from chesstraining import trainingapp

root = tkinter.Tk()
  
board = [['  ' for i in range(8)] for i in range(8)]
WINDOW_HEIGHT = 600
WINDOW_WIDTH = WINDOW_HEIGHT
FRAME_THICKNESS = 0
WIDTH = WINDOW_HEIGHT - 2 * FRAME_THICKNESS
ai = AI()

WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


##options_list = ["1 Player", "2 Players", "AI vs Stockfish (1000)", "Trainingmode", "Reset board"]

value_inside = tkinter.StringVar(root)


#question_menu = tkinter.OptionMenu(root, value_inside, *options_list)
#question_menu.pack()

#move_sound = pygame.mixer.Sound(
#    'ChessAiApp\\sounds\\move-self.mp3')
#capture_sound = pygame.mixer.Sound(
#    'ChessAiApp\\sounds\\capture.mp3')
#castling_sound = pygame.mixer.Sound(
#    'ChessAiApp\\sounds\\castle.mp3')
#promoting_sound = pygame.mixer.Sound(
#    'ChessAiApp\\sounds\\promote.mp3')
#checking_sound = pygame.mixer.Sound(
#    'ChessAiApp\\sounds\\move-check.mp3')

class Piece:
    def __init__(self, team, type, image, killable=False):
        self.team = team
        self.type = type
        self.killable = killable
        self.image = image

bp = Piece('b', 'p', 'ChessAiApp//icons//pB.png')
wp = Piece('w', 'p', 'ChessAiApp//icons//pW.png')
bk = Piece('b', 'k', 'ChessAiApp//icons//kB.png')
wk = Piece('w', 'k', 'ChessAiApp//icons//kW.png')
br = Piece('b', 'r', 'ChessAiApp//icons//rB.png')
wr = Piece('w', 'r', 'ChessAiApp//icons//rW.png')
bb = Piece('b', 'b', 'ChessAiApp//icons//bB.png')
wb = Piece('w', 'b', 'ChessAiApp//icons//bW.png')
bq = Piece('b', 'q', 'ChessAiApp//icons//qB.png')
wq = Piece('w', 'q', 'ChessAiApp//icons//qW.png')
bkn = Piece('b', 'kn', 'ChessAiApp//icons//nB.png')
wkn = Piece('w', 'kn', 'ChessAiApp//icons//nW.png')


starting_order = {(0, 0): pygame.image.load(br.image), (1, 0): pygame.image.load(bkn.image),
                  (2, 0): pygame.image.load(bb.image), (3, 0): pygame.image.load(bk.image),
                  (4, 0): pygame.image.load(bq.image), (5, 0): pygame.image.load(bb.image),
                  (6, 0): pygame.image.load(bkn.image), (7, 0): pygame.image.load(br.image),
                  (0, 1): pygame.image.load(bp.image), (1, 1): pygame.image.load(bp.image),
                  (2, 1): pygame.image.load(bp.image), (3, 1): pygame.image.load(bp.image),
                  (4, 1): pygame.image.load(bp.image), (5, 1): pygame.image.load(bp.image),
                  (6, 1): pygame.image.load(bp.image), (7, 1): pygame.image.load(bp.image),

                  (0, 2): None, (1, 2): None, (2, 2): None, (3, 2): None,
                  (4, 2): None, (5, 2): None, (6, 2): None, (7, 2): None,
                  (0, 3): None, (1, 3): None, (2, 3): None, (3, 3): None,
                  (4, 3): None, (5, 3): None, (6, 3): None, (7, 3): None,
                  (0, 4): None, (1, 4): None, (2, 4): None, (3, 4): None,
                  (4, 4): None, (5, 4): None, (6, 4): None, (7, 4): None,
                  (0, 5): None, (1, 5): None, (2, 5): None, (3, 5): None,
                  (4, 5): None, (5, 5): None, (6, 5): None, (7, 5): None,

                  (0, 6): pygame.image.load(wp.image), (1, 6): pygame.image.load(wp.image),
                  (2, 6): pygame.image.load(wp.image), (3, 6): pygame.image.load(wp.image),
                  (4, 6): pygame.image.load(wp.image), (5, 6): pygame.image.load(wp.image),
                  (6, 6): pygame.image.load(wp.image), (7, 6): pygame.image.load(wp.image),
                  (0, 7): pygame.image.load(wr.image), (1, 7): pygame.image.load(wkn.image),
                  (2, 7): pygame.image.load(wb.image), (3, 7): pygame.image.load(wk.image),
                  (4, 7): pygame.image.load(wq.image), (5, 7): pygame.image.load(wb.image),
                  (6, 7): pygame.image.load(wkn.image), (7, 7): pygame.image.load(wr.image), }


def create_board(board):
    board[0] = [Piece('b', 'r', 'b_rook.png'), Piece('b', 'kn', 'b_knight.png'), Piece('b', 'b', 'b_bishop.png'),
                Piece('b', 'q', 'b_queen.png'), Piece(
                    'b', 'k', 'b_king.png'), Piece('b', 'b', 'b_bishop.png'),
                Piece('b', 'kn', 'b_knight.png'), Piece('b', 'r', 'b_rook.png')]

    board[7] = [Piece('w', 'r', 'w_rook.png'), Piece('w', 'kn', 'w_knight.png'), Piece('w', 'b', 'w_bishop.png'),
                Piece('w', 'q', 'w_queen.png'), Piece(
                    'w', 'k', 'w_king.png'), Piece('w', 'b', 'w_bishop.png'),
                Piece('w', 'kn', 'w_knight.png'), Piece('w', 'r', 'w_rook.png')]

    for i in range(8):
        board[1][i] = Piece('b', 'p', 'b_pawn.png')
        board[6][i] = Piece('w', 'p', 'w_pawn.png')
    return board


def on_board(position):
    if position[0] > -1 and position[1] > -1 and position[0] < 8 and position[1] < 8:
        return True


def redirect_options(option):
    #if option == "1 Player":
        #player_vs_ai()
    if option == "2 Players":
        reset_board() #reopen the game
    #elif option == "AI vs Stockfish (1000)":
        #start_ai_vs_stockfish()
    elif option == "Trainingmode":
        trainingapp()
    elif option == "Reset board":
        reset_board()

def reset_board():
    global starting_order
    starting_order = {(0, 0): pygame.image.load(br.image), (1, 0): pygame.image.load(bkn.image),
                      (2, 0): pygame.image.load(bb.image), (3, 0): pygame.image.load(bk.image),
                      (4, 0): pygame.image.load(bq.image), (5, 0): pygame.image.load(bb.image),
                      (6, 0): pygame.image.load(bkn.image), (7, 0): pygame.image.load(br.image),
                      (0, 1): pygame.image.load(bp.image), (1, 1): pygame.image.load(bp.image),
                      (2, 1): pygame.image.load(bp.image), (3, 1): pygame.image.load(bp.image),
                      (4, 1): pygame.image.load(bp.image), (5, 1): pygame.image.load(bp.image),
                      (6, 1): pygame.image.load(bp.image), (7, 1): pygame.image.load(bp.image),

                      (0, 2): None, (1, 2): None, (2, 2): None, (3, 2): None,
                      (4, 2): None, (5, 2): None, (6, 2): None, (7, 2): None,
                      (0, 3): None, (1, 3): None, (2, 3): None, (3, 3): None,
                      (4, 3): None, (5, 3): None, (6, 3): None, (7, 3): None,
                      (0, 4): None, (1, 4): None, (2, 4): None, (3, 4): None,
                      (4, 4): None, (5, 4): None, (6, 4): None, (7, 4): None,
                      (0, 5): None, (1, 5): None, (2, 5): None, (3, 5): None,
                      (4, 5): None, (5, 5): None, (6, 5): None, (7, 5): None,

                      (0, 6): pygame.image.load(wp.image), (1, 6): pygame.image.load(wp.image),
                      (2, 6): pygame.image.load(wp.image), (3, 6): pygame.image.load(wp.image),
                      (4, 6): pygame.image.load(wp.image), (5, 6): pygame.image.load(wp.image),
                      (6, 6): pygame.image.load(wp.image), (7, 6): pygame.image.load(wp.image),
                      (0, 7): pygame.image.load(wr.image), (1, 7): pygame.image.load(wkn.image),
                      (2, 7): pygame.image.load(wb.image), (3, 7): pygame.image.load(wk.image),
                      (4, 7): pygame.image.load(wq.image), (5, 7): pygame.image.load(wb.image),
                      (6, 7): pygame.image.load(wkn.image), (7, 7): pygame.image.load(wr.image), }

    print("Chess board has been reset.")

def convert_to_readable(board):
    output = ''

    for i in board:
        for j in i:
            try:
                output += j.team + j.type + ', '
            except:
                output += j + ', '
        output += '\n'
    return output

def deselect():
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == 'x ':
                board[row][column] = '  '
            else:
                try:
                    board[row][column].killable = False
                except:
                    pass
    return convert_to_readable(board)


def highlight(board):
    highlighted = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'x ':
                highlighted.append((i, j))
            else:
                try:
                    if board[i][j].killable:
                        highlighted.append((i, j))
                except:
                    pass
    return highlighted


def check_team(moves, index):
    row, col = index
    if moves % 2 == 0:
        if board[row][col].team == 'w':
            return True
    else:
        if board[row][col].team == 'b':
            return True


def select_moves(piece, index, moves):
    reset_legal_moves()

    if check_team(moves, index):
        if piece.type == 'p':
            if piece.team == 'b':
                pawn_moves_b(index)
            else:
                pawn_moves_w(index)

        if piece.type == 'k':
            king_moves(index)

        if piece.type == 'r':
            rook_moves(index)

        if piece.type == 'b':
            bishop_moves(index)

        if piece.type == 'q':
            queen_moves(index)

        if piece.type == 'kn':
            knight_moves(index)

    return highlight(board)

def pawn_moves_b(index):
    if index[0] == 1:
        if board[index[0] + 2][index[1]] == '  ' and board[index[0] + 1][index[1]] == '  ':
            board[index[0] + 2][index[1]] = 'x '
    bottom3 = [[index[0] + 1, index[1] + i] for i in range(-1, 2)]

    for positions in bottom3:
        if on_board(positions):
            if bottom3.index(positions) % 2 == 0:
                try:
                    if board[positions[0]][positions[1]].team != 'b':
                        board[positions[0]][positions[1]].killable = True
                        legal_moves.append((positions[0], positions[1]))
                except:
                    pass
            else:
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                    legal_moves.append((positions[0], positions[1]))


def pawn_moves_w(index):
    if index[0] == 6:
        if board[index[0] - 2][index[1]] == '  ' and board[index[0] - 1][index[1]] == '  ':
            board[index[0] - 2][index[1]] = 'x '
    top3 = [[index[0] - 1, index[1] + i] for i in range(-1, 2)]

    for positions in top3:
        if on_board(positions):
            if top3.index(positions) % 2 == 0:
                try:
                    if board[positions[0]][positions[1]].team != 'w':
                        board[positions[0]][positions[1]].killable = True
                except:
                    pass
            else:
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
    return board

def king_moves(index):
    for y in range(3):
        for x in range(3):
            if on_board((index[0] - 1 + y, index[1] - 1 + x)):
                if board[index[0] - 1 + y][index[1] - 1 + x] == '  ':
                    board[index[0] - 1 + y][index[1] - 1 + x] = 'x '
                else:
                    if board[index[0] - 1 + y][index[1] - 1 + x].team != board[index[0]][index[1]].team:
                        board[index[0] - 1 + y][index[1] - 1 + x].killable = True
    return board

def rook_moves(index):
    cross = [[[index[0] + i, index[1]] for i in range(1, 8 - index[0])],
             [[index[0] - i, index[1]] for i in range(1, index[0] + 1)],
             [[index[0], index[1] + i] for i in range(1, 8 - index[1])],
             [[index[0], index[1] - i] for i in range(1, index[1] + 1)]]

    for direction in cross:
        for positions in direction:
            if on_board(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    if board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                        board[positions[0]][positions[1]].killable = True
                    break
    return board
def bishop_moves(index):
    diagonals = [[[index[0] + i, index[1] + i] for i in range(1, 8)],
                 [[index[0] + i, index[1] - i] for i in range(1, 8)],
                 [[index[0] - i, index[1] + i] for i in range(1, 8)],
                 [[index[0] - i, index[1] - i] for i in range(1, 8)]]

    for direction in diagonals:
        for positions in direction:
            if on_board(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    if board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                        board[positions[0]][positions[1]].killable = True
                    break
    return board

def queen_moves(index):
    board = rook_moves(index)
    board = bishop_moves(index)
    return board

def knight_moves(index):
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i ** 2 + j ** 2 == 5:
                if on_board((index[0] + i, index[1] + j)):
                    if board[index[0] + i][index[1] + j] == '  ':
                        board[index[0] + i][index[1] + j] = 'x '
                    else:
                        if board[index[0] + i][index[1] + j].team != board[index[0]][index[1]].team:
                            board[index[0] + i][index[1] + j].killable = True
    return board


legal_moves = []


def reset_legal_moves():
    global legal_moves
    legal_moves = []

pygame.init()
pygame.display.set_caption("Chess")
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)


class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.occupied = None
        

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour,
                         (self.x, self.y, WIDTH // 8, WIDTH // 8))

    def setup(self, WIN):
        if starting_order[(self.row, self.col)]:
            if starting_order[(self.row, self.col)] == None:
                pass
            else:
                scale_factor = 0.8
                scaled_width = int(WIDTH // 8 * scale_factor)
                scaled_height = int(WIDTH // 8 * scale_factor)
                scaled_image = pygame.transform.scale(
                    starting_order[(self.row, self.col)], (scaled_width, scaled_height))

                x_offset = (WIDTH // 8 - scaled_width) // 2
                y_offset = (WIDTH // 8 - scaled_height) // 2

                WIN.blit(scaled_image, (self.x + x_offset, self.y + y_offset))


def show_context_menu(options, pos):
    menu = tkinter.Menu(root, tearoff=0)
    for option in options:
        menu.add_command(
            label=option, command=lambda: print("Selected:", option))
    menu.post(pos[0] + root.winfo_rootx(), pos[1] + root.winfo_rooty())

def make_grid(rows, width):
    grid = []
    gap = WIDTH // rows
    print(gap)
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j, i, gap)
            grid[i].append(node)
            if (i+j) % 2 == 1:
                grid[i][j].colour = GREY
    return grid

def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
            spot.setup(win)
    pygame.display.update()

def Find_Node(pos, WIDTH):
    interval = WIDTH / 8
    y, x = pos
    rows = y // interval
    columns = x // interval
    return int(rows), int(columns)

def display_potential_moves(positions, grid):
    for i in positions:
        x, y = i
        grid[x][y].colour = BLUE

def Do_Move(OriginalPos, FinalPosition, WIN):
    starting_order[FinalPosition] = starting_order[OriginalPos]
    starting_order[OriginalPos] = None


def remove_highlight(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i+j) % 2 == 0:
                grid[i][j].colour = WHITE
            else:
                grid[i][j].colour = GREY
    return grid

create_board(board)


def main(WIN, WIDTH):
    moves = 0
    selected = False
    piece_to_move = []
    grid = make_grid(8, WINDOW_WIDTH)
    while True:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if moves % 2 == 1:
                legal_moves = list(board.legal_moves)
                ai_move = ai.choose_move(board, legal_moves)
                board.push(ai_move)
                print(convert_to_readable(board))

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                y, x = Find_Node(pos, WIDTH)
                if event.button == 1:
                    if not selected:
                        try:
                            possible = select_moves(
                                (board[x][y]), (x, y), moves)
                            for positions in possible:
                                row, col = positions
                                grid[row][col].colour = BLUE
                            piece_to_move = x, y
                            selected = True
                        except:
                            piece_to_move = []
                            print('Can\'t select')
                    else:
                        try:
                            if board[x][y].killable == True:
                                row, col = piece_to_move
                                board[x][y] = board[row][col]
                                board[row][col] = '  '
                                deselect()
                                remove_highlight(grid)
                                Do_Move((col, row), (y, x), WIN)
                                moves += 1
                                print(convert_to_readable(board))
                            else:
                                deselect()
                                remove_highlight(grid)
                                selected = False
                                print("Deselected")
                        except:
                            if board[x][y] == 'x ':
                                row, col = piece_to_move
                                board[x][y] = board[row][col]
                                board[row][col] = '  '
                                deselect()
                                remove_highlight(grid)
                                Do_Move((col, row), (y, x), WIN)
                                moves += 1
                                print(convert_to_readable(board))
                            else:
                                deselect()
                                remove_highlight(grid)
                                selected = False
                                print("Invalid move")
                        selected = False

                #elif event.button == 3:
                    #show_context_menu(options_list, pos)

            update_display(WIN, grid, 8, WIDTH)


if __name__ == "__main__":
    main(WIN, WINDOW_WIDTH)
    root.mainloop()
