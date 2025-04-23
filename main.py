import pygame
import sys

def main():
    # Initialize pygame
    pygame.init()

    # Set window size
    WIDTH, HEIGHT = 640, 640
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

    # Set window title
    pygame.display.set_caption("Chess Tactics Trainer")

    # Set background color
    WHITE = (255, 255, 255)

    # Run the game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill screen with white
        WINDOW.fill(WHITE)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
