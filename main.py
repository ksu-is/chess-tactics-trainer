import pygame
import sys
import chess
import json
import random

# === CONFIG ===
SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8
FONT_SIZE = 48
LABEL_FONT_SIZE = 20
FEEDBACK_FONT_SIZE = 32
HIGHLIGHT = (255, 255, 0)
CORRECT_HIGHLIGHT = (0, 255, 0)

# === THEMES ===
LIGHT_THEME = {
    "light": (240, 217, 181),
    "dark": (181, 136, 99),
    "text": (0, 0, 0),
    "bg": (255, 255, 255)
}

DARK_THEME = {
    "light": (100, 100, 100),
    "dark": (50, 50, 50),
    "text": (255, 255, 255),
    "bg": (30, 30, 30)
}

current_theme = LIGHT_THEME

UNICODE_PIECES = {
    "r": "♜", "n": "♞", "b": "♝", "q": "♛", "k": "♚", "p": "♟",
    "R": "♖", "N": "♘", "B": "♗", "Q": "♕", "K": "♔", "P": "♙"
}

# Load puzzles once
with open("puzzles.json", "r") as f:
    PUZZLES = json.load(f)

def load_random_puzzle():
    puzzle = random.choice(PUZZLES)
    board = chess.Board(puzzle["fen"])
    solution = puzzle["move"]
    return board, solution

# === HELPERS ===
def draw_board(win, piece_font, label_font, board, feedback, theme, selected=None, correct_squares=None):
    win.fill(theme["bg"])

    for row in range(8):
        for col in range(8):
            color = theme["light"] if (row + col) % 2 == 0 else theme["dark"]
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(win, color, rect)

            # Coordinates
            if col == 0:
                label = label_font.render(str(8 - row), True, theme["text"])
                win.blit(label, (5, row * SQUARE_SIZE + 5))
            if row == 7:
                label = label_font.render(chr(ord('a') + col), True, theme["text"])
                win.blit(label, (col * SQUARE_SIZE + SQUARE_SIZE - 20, BOARD_SIZE - 20))

            if selected == (row, col):
                pygame.draw.rect(win, HIGHLIGHT, rect, 4)

            if correct_squares and (row, col) in correct_squares:
                pygame.draw.rect(win, CORRECT_HIGHLIGHT, rect, 4)

            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            if piece:
                symbol = piece.symbol()
                text = piece_font.render(UNICODE_PIECES[symbol], True, theme["text"])
                text_rect = text.get_rect(center=rect.center)
                win.blit(text, text_rect)

    if feedback:
        feedback_font = pygame.font.SysFont("Segoe UI", FEEDBACK_FONT_SIZE)
        msg = feedback_font.render(feedback, True, (0, 200, 0) if feedback == "Correct!" else (200, 0, 0))
        win.blit(msg, (20, BOARD_SIZE - 40))

def get_square_from_pos(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return (row, col)

def square_to_chess_notation(row, col):
    file = chr(ord('a') + col)
    rank = str(8 - row)
    return file + rank

def chess_notation_to_row_col(square):
    col = ord(square[0]) - ord('a')
    row = 8 - int(square[1])
    return (row, col)

def main():
    global current_theme

    pygame.init()
    win = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption("Chess Tactics Trainer")
    piece_font = pygame.font.SysFont("Segoe UI Symbol", FONT_SIZE)
    label_font = pygame.font.SysFont("Segoe UI", LABEL_FONT_SIZE)

    board, solution_move = load_random_puzzle()

    selected = None
    from_square = None
    feedback = ""
    correct_squares = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_square_from_pos(pygame.mouse.get_pos())
                square = square_to_chess_notation(row, col)

                if not from_square:
                    from_square = square
                    selected = (row, col)
                else:
                    to_square = square
                    user_uci = from_square + to_square

                    try:
                        move_obj = board.parse_san(solution_move)
                        correct_uci = move_obj.uci()
                    except:
                        correct_uci = ""

                    if user_uci == correct_uci:
                        feedback = "Correct!"
                        pygame.time.wait(500)
                        board, solution_move = load_random_puzzle()
                        feedback = ""
                        correct_squares = None
                    else:
                        feedback = "Try again!"
                        move_obj = board.parse_san(solution_move)
                        correct_squares = [
                            chess_notation_to_row_col(chess.square_name(move_obj.from_square)),
                            chess_notation_to_row_col(chess.square_name(move_obj.to_square))
                        ]
                        # Show highlight immediately
                        draw_board(win, piece_font, label_font, board, feedback, current_theme, selected, correct_squares)
                        pygame.display.flip()
                        pygame.time.wait(1000)
                        correct_squares = None

                    selected = None
                    from_square = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    current_theme = DARK_THEME if current_theme == LIGHT_THEME else LIGHT_THEME

        draw_board(win, piece_font, label_font, board, feedback, current_theme, selected, correct_squares)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
