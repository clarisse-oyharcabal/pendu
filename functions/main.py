# Module importation
import pygame
import sys

# Screen size constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WATER_BLUE = (0, 98, 255)
SKY_BLUE = (188, 202, 233)
GREEN = (0, 152, 143)
ORANGE = (231, 74, 52)
VIOLET = (157, 97, 255)
BLACK = (00, 00, 00)
WHITE = (255, 255, 255)

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
