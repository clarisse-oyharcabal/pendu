import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pondule")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Load assets
try:
    man_img = pygame.image.load("man.png")
    man_img = pygame.transform.scale(man_img, (50, 100))
except FileNotFoundError:
    print("Erreur : Le fichier 'man.png' est introuvable. Utilisation d'une image de remplacement.")
    man_img = pygame.Surface((50, 100))
    man_img.fill(BLUE)

try:
    cup_img = pygame.image.load("cup.png")
    cup_img = pygame.transform.scale(cup_img, (100, 100))
except FileNotFoundError:
    print("Erreur : Le fichier 'cup.png' est introuvable. Utilisation d'une image de remplacement.")
    cup_img = pygame.Surface((100, 100))
    cup_img.fill(RED)

# Game variables
words_easy = ["cat", "dog", "sun", "book", "star"]
words_hard = ["elephant", "mountain", "triangle", "computer", "penguin"]
max_attempts = 7

# Game states
START_MENU = 0
PLAYING = 1
END_SCREEN = 2

# Pendulum variables
pendulum_angle = 0  # Angle of the pendulum
pendulum_speed = 5  # Speed of the pendulum swing
pendulum_direction = 1  # Direction of the pendulum swing (1 for right, -1 for left)
character_x = WIDTH // 2 - 25  # Initial X position of the character
character_y = HEIGHT - 150  # Initial Y position of the character
platform_y = HEIGHT - 100  # Y position of the platform

class Game:
    def __init__(self):
        self.difficulty = "easy"
        self.selected_word = ""
        self.guessed_letters = []
        self.attempts = 0
        self.game_state = START_MENU
        self.reset_game()

    def reset_game(self):
        self.guessed_letters = []
        self.attempts = 0
        word_list = words_easy if self.difficulty == "easy" else words_hard
        self.selected_word = random.choice(word_list)
        global character_x, pendulum_angle
        character_x = WIDTH // 2 - 25  # Reset character position
        pendulum_angle = 0  # Reset pendulum angle

    def display_message(self, message, color, y_offset=0):
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
        screen.blit(text, text_rect)

    def draw_man(self, x, y):
        screen.blit(man_img, (x, y))

    def draw_word(self):
        display_word = " ".join([letter if letter in self.guessed_letters else "_" for letter in self.selected_word])
        text = font.render(display_word, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(text, text_rect)

    def draw_pendulum(self):
        global pendulum_angle, pendulum_direction, character_x

        # Update pendulum angle
        pendulum_angle += pendulum_speed * pendulum_direction
        if pendulum_angle > 45 or pendulum_angle < -45:
            pendulum_direction *= -1  # Reverse direction

        # Draw pendulum
        pivot_x = WIDTH // 2
        pivot_y = 50
        pendulum_length = 200
        end_x = pivot_x + pendulum_length * pygame.math.Vector2().from_polar((1, pendulum_angle))[0]
        end_y = pivot_y + pendulum_length * pygame.math.Vector2().from_polar((1, pendulum_angle))[1]
        pygame.draw.line(screen, BLACK, (pivot_x, pivot_y), (end_x, end_y), 5)
        pygame.draw.circle(screen, RED, (int(end_x), int(end_y)), 10)

        # Move character based on pendulum angle
        if self.attempts > 0:
            character_x += pendulum_direction * 2  # Move character horizontally

    def handle_start_menu(self):
        self.display_message("Pondule", BLUE, -50)
        easy_button = small_font.render("Easy", True, BLACK)
        hard_button = small_font.render("Hard", True, BLACK)
        screen.blit(easy_button, (WIDTH // 2 - 100, HEIGHT // 2))
        screen.blit(hard_button, (WIDTH // 2 + 50, HEIGHT // 2))

        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if WIDTH // 2 - 100 <= mouse_pos[0] <= WIDTH // 2 - 50 and HEIGHT // 2 <= mouse_pos[1] <= HEIGHT // 2 + 30:
                self.difficulty = "easy"
                self.reset_game()
                self.game_state = PLAYING
            elif WIDTH // 2 + 50 <= mouse_pos[0] <= WIDTH // 2 + 100 and HEIGHT // 2 <= mouse_pos[1] <= HEIGHT // 2 + 30:
                self.difficulty = "hard"
                self.reset_game()
                self.game_state = PLAYING

    def handle_playing(self, event):
        if event.type == pygame.KEYDOWN:
            if event.unicode.isalpha():
                guess = event.unicode.lower()
                if guess not in self.guessed_letters:
                    self.guessed_letters.append(guess)
                    if guess not in self.selected_word:
                        self.attempts += 1

    def handle_end_screen(self):
        if self.attempts >= max_attempts:
            self.display_message("You Lose!", RED)
        else:
            self.display_message("You Win!", GOLD)
        self.display_message("Press R to Restart", BLACK, 50)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.game_state = START_MENU

    def run(self):
        running = True
        clock = pygame.time.Clock()  # Add a clock to control the frame rate

        while running:
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif self.game_state == PLAYING:
                    self.handle_playing(event)

            if self.game_state == START_MENU:
                self.handle_start_menu()
            elif self.game_state == PLAYING:
                self.draw_word()
                self.draw_pendulum()
                self.draw_man(character_x, character_y)
                pygame.draw.rect(screen, GREEN, (0, platform_y, WIDTH, 20))  # Draw platform

                # Check if character falls off the platform
                if character_x < 0 or character_x > WIDTH - 50:
                    self.game_state = END_SCREEN

                if "_" not in [letter if letter in self.guessed_letters else "_" for letter in self.selected_word]:
                    self.game_state = END_SCREEN
                elif self.attempts >= max_attempts:
                    self.game_state = END_SCREEN
            elif self.game_state == END_SCREEN:
                self.handle_end_screen()

            pygame.display.flip()
            clock.tick(30)  # Limit the frame rate to 30 FPS

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()