# Module importation
import pygame
import sys

# Screen size constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

# Game main function
def main():
    pygame.init()
    # Window creation & title
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("The galaxy hangman")
    
    # Load the background image
    background = pygame.image.load("img/background.png")
    
    # Indicate surface positions
    screen.blit(background, (0, 0))
    
    # Main game loop
    while True:
        # Possible keyboard and mouse inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        # Update the screen
        pygame.display.flip()

if __name__ == "__main__":
    main()
