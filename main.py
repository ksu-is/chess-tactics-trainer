import pygame
import sys

# Constants
SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)

def draw_board(window):
    for row in range(8):
        for col in range(8):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(window, color, rect)

def main():
    pygame.init()
    window = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption("Chess Tactics Trainer")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board(window)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
