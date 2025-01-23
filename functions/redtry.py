import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Le Pendule")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Load assets
man_img = pygame.image.load("man.png")
man_img = pygame.transform.scale(man_img, (50, 100))
cup_img = pygame.image.load("cup.png")
cup_img = pygame.transform.scale(cup_img, (100, 100))

# Initialize game variables
words_easy = ["cat", "dog", "sun", "book", "star"]
words_hard = ["elephant", "mountain", "triangle", "computer", "penguin"]
difficulty = "easy"
selected_word = ""
guessed_letters = []
max_attempts = 7
attempts = 0

# Game states
START_MENU = 0
PLAYING = 1
END_SCREEN = 2
game_state = START_MENU

# Helper functions
def display_message(message, color, y_offset=0):
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text, text_rect)

def draw_man(x, y):
    screen.blit(man_img, (x, y))

def draw_word():
    display_word = " ".join([letter if letter in guessed_letters else "_" for letter in selected_word])
    text = font.render(display_word, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(text, text_rect)

def reset_game():
    global selected_word, guessed_letters, attempts
    guessed_letters = []
    attempts = 0
    word_list = words_easy if difficulty == "easy" else words_hard
    selected_word = random.choice(word_list)

# Main loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and game_state == PLAYING:
            if event.unicode.isalpha():
                guess = event.unicode.lower()
                if guess not in guessed_letters:
                    guessed_letters.append(guess)
                    if guess not in selected_word:
                        attempts += 1

    if game_state == START_MENU:
        display_message("Le Pendule", BLUE, -50)
        easy_button = small_font.render("Easy", True, BLACK)
        hard_button = small_font.render("Hard", True, BLACK)
        screen.blit(easy_button, (WIDTH // 2 - 100, HEIGHT // 2))
        screen.blit(hard_button, (WIDTH // 2 + 50, HEIGHT // 2))

        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if WIDTH // 2 - 100 <= mouse_pos[0] <= WIDTH // 2 - 50 and HEIGHT // 2 <= mouse_pos[1] <= HEIGHT // 2 + 30:
                difficulty = "easy"
                reset_game()
                game_state = PLAYING
            elif WIDTH // 2 + 50 <= mouse_pos[0] <= WIDTH // 2 + 100 and HEIGHT // 2 <= mouse_pos[1] <= HEIGHT // 2 + 30:
                difficulty = "hard"
                reset_game()
                game_state = PLAYING

    elif game_state == PLAYING:
        draw_word()
        draw_man(WIDTH // 2 - 25, HEIGHT - 150)
        if "_" not in [letter if letter in guessed_letters else "_" for letter in selected_word]:
            game_state = END_SCREEN
        elif attempts >= max_attempts:
            game_state = END_SCREEN

    elif game_state == END_SCREEN:
        if attempts >= max_attempts:
            display_message("You Lose!", RED)
        else:
            display_message("You Win!", GOLD)
        display_message("Press R to Restart", BLACK, 50)

        if pygame.key.get_pressed()[pygame.K_r]:
            game_state = START_MENU

    pygame.display.flip()

pygame.quit()