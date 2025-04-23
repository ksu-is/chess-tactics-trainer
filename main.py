import pygame
import sys
import chess
import json
import random

# === CONFIG ===
SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
HIGHLIGHT = (255, 255, 0)
FONT_SIZE = 48
FEEDBACK_FONT_SIZE = 32

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
def draw_board(win, font, board, feedback, selected=None):
    for row in range(8):
        for col in range(8):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(win, color, rect)

            if selected == (row, col):
                pygame.draw.rect(win, HIGHLIGHT, rect, 4)

            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            if piece:
                symbol = piece.symbol()
                text = font.render(UNICODE_PIECES[symbol], True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                win.blit(text, text_rect)

    if feedback:
        feedback_font = pygame.font.SysFont("Segoe UI", FEEDBACK_FONT_SIZE)
        msg = feedback_font.render(feedback, True, (0, 128, 0) if feedback == "Correct!" else (200, 0, 0))
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

def main():
    pygame.init()
    win = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption("Chess Tactics Trainer")
    font = pygame.font.SysFont("Segoe UI Symbol", FONT_SIZE)

    board, solution_move = load_random_puzzle()

    selected = None
    from_square = None
    feedback = ""

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
                        pygame.time.wait(500)  # brief pause before switching
                        board, solution_move = load_random_puzzle()
                        feedback = ""
                    else:
                        feedback = "Try again!"

                    selected = None
                    from_square = None

        draw_board(win, font, board, feedback, selected)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
