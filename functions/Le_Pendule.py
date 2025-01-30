import pygame
import math
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Le Pendule")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
def load_image(path, size=None):
    try:
        image = pygame.image.load(path)
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except FileNotFoundError as e:
        print(f"Error loading image: {e}")
        sys.exit()

# Load all images
background_img = load_image("sky.png")
platform_img = load_image("laplateforme.png")
sea_img = load_image("sea.png")
man_img = load_image("man.png", (80, 120))  # Resized man
wave_img = load_image("flot.png")
pendulum_img = load_image("pend.png", (50, 200))  # Resized pendulum
fish_img = load_image("fish.png", (60, 100))  # Resized fish
heart_plain = load_image("heartbp.png", (30, 30))  # Blue plain heart
heart_empty_blue = load_image("heartbv.png", (30, 30))  # Blue empty heart
heart_plain_red = load_image("heartrp.png", (30, 30))  # Red plain heart
heart_empty_red = load_image("heartrv.png", (30, 30))  # Red empty heart

# Fonts
font = pygame.font.Font(None, 36)

# Sound effects
def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"Error loading sound: {e}")
        return None

pygame.mixer.init()
pygame.mixer.music.load("background_music.mp3")  # Background music
pygame.mixer.music.play(-1)  # Loop indefinitely
correct_sound = load_sound("correct.wav")
incorrect_sound = load_sound("incorrect.wav")
strike_sound = load_sound("strike.wav")
splash_sound = load_sound("splash.wav")
win_sound = load_sound("win.wav")
lose_sound = load_sound("lose.wav")

# Word lists for difficulty levels
easy_words = [
    ("algorithm", "A step-by-step procedure for solving a problem."),
    ("binary", "A system of numerical notation with base 2."),
    ("code", "Instructions written in a programming language."),
    ("data", "Information processed or stored by a computer."),
    ("debug", "To find and fix errors in code."),
    # Add more words...
]

complex_words = [
    ("asymptotic", "Describes the behavior of a function as it approaches a limit."),
    ("heuristic", "A problem-solving approach that uses practical methods."),
    ("polymorphism", "The ability of a function to operate on multiple types."),
    ("recursion", "A function that calls itself."),
    ("syntax", "The set of rules that define the structure of a language."),
    # Add more words...
]

class Man:
    def __init__(self, x, y, platform_width):
        self.x = x
        self.y = y
        self.width = man_img.get_width()
        self.height = man_img.get_height()
        self.platform_width = platform_width
        self.move_distance = platform_width * 0.2  # 20% of the platform width
        self.direction = -1  # -1 for left, 1 for right
        self.falling = False
        self.velocity_x = 0
        self.velocity_y = 0

    def draw(self, screen):
        screen.blit(man_img, (self.x, self.y))

    def move(self):
        self.x += self.direction * self.move_distance

    def fall(self):
        self.velocity_y += 0.5
        self.x += self.velocity_x
        self.y += self.velocity_y

class PendulumGame:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.words = easy_words if difficulty == "easy" else complex_words
        self.word, self.hint = random.choice(self.words)
        self.guessed_word = ["_"] * len(self.word)
        self.failures = 0
        self.max_failures = 5  # 5 strikes before the man falls

        # Adjust platform position (centered)
        self.platform_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 300, 200, 20)

        # Adjust pendulum pivot and rod length
        self.initial_pivot = [WIDTH // 2, self.platform_rect.y - 200]  # Pivot point above the platform
        self.pivot = self.initial_pivot.copy()
        self.rod_length = 250  # Shorter rod length for better alignment

        self.pendulum_angle = math.pi / 4  # Initial angle (swinging to the left)
        self.pendulum_velocity = 0
        self.gravity = 0.005  # Gravity for pendulum swing
        self.strike_triggered = False
        self.strike_timer = 0

        # Position the man in the center of the platform
        self.man = Man(
            self.platform_rect.x + self.platform_rect.width // 2 - 40,  # Adjusted position
            self.platform_rect.y - man_img.get_height(),  # Feet on the platform
            self.platform_rect.width
        )
        self.man_falling = False

        self.sea_y = HEIGHT - sea_img.get_height() + 50  # Waves slightly lower
        self.wave_x = 0
        self.wave_speed = 2

        self.hearts = [heart_plain] * 5  # 5 hearts
        self.fish_y = HEIGHT  # Fish starts below the screen
        self.fish_speed = 5

        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()  # Timer for the game

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    self.process_guess(event.unicode.lower())
        return True

    def process_guess(self, letter):
        if letter in self.word:
            if correct_sound:
                pygame.mixer.music.pause()  # Pause background music
                correct_sound.play()
                while pygame.mixer.get_busy():  # Wait for sound to finish
                    pygame.time.delay(100)
                pygame.mixer.music.unpause()  # Resume background music
            for i, char in enumerate(self.word):
                if char == letter:
                    self.guessed_word[i] = letter
            if "_" not in self.guessed_word:  # Player wins
                self.man_falling = False
                if win_sound:
                    pygame.mixer.music.pause()
                    win_sound.play()
                    while pygame.mixer.get_busy():
                        pygame.time.delay(100)
                    pygame.mixer.music.unpause()
                self.man.y -= 10  # Man jumps on the pendulum
                self.show_end_screen(win=True)
                return
        else:
            if incorrect_sound:
                pygame.mixer.music.pause()
                incorrect_sound.play()
                while pygame.mixer.get_busy():
                    pygame.time.delay(100)
                pygame.mixer.music.unpause()
            self.failures += 1
            if self.failures < self.max_failures:
                self.strike_triggered = True  # Pendulum strikes only after a wrong guess
                self.man.move()  # Move the man closer to the edge
                self.pivot[0] += self.man.direction * self.man.move_distance  # Move pendulum pivot
                self.hearts[self.failures - 1] = heart_empty_blue if self.failures <= 3 else heart_empty_red
            else:
                self.man_falling = True
                if splash_sound:
                    pygame.mixer.music.pause()
                    splash_sound.play()
                    while pygame.mixer.get_busy():
                        pygame.time.delay(100)
                    pygame.mixer.music.unpause()
                self.show_end_screen(win=False)

    def update_pendulum(self):
        if self.strike_triggered:
            self.pendulum_acceleration = -self.gravity * math.sin(self.pendulum_angle)
            self.pendulum_velocity += self.pendulum_acceleration
            self.pendulum_angle += self.pendulum_velocity
            self.pendulum_velocity *= 0.99

            pendulum_x = self.pivot[0] + self.rod_length * math.sin(self.pendulum_angle)
            pendulum_y = self.pivot[1] + self.rod_length * math.cos(self.pendulum_angle)

            man_rect = pygame.Rect(self.man.x, self.man.y, self.man.width, self.man.height)
            if man_rect.collidepoint((pendulum_x, pendulum_y)):
                self.strike_triggered = False
                self.pendulum_angle = math.pi / 4  # Reset to initial angle
                self.pendulum_velocity = 0
                if self.failures == self.max_failures:
                    self.man_falling = True  # Make the man fall on the last strike
                    if strike_sound:
                        pygame.mixer.music.pause()
                        strike_sound.play()
                        while pygame.mixer.get_busy():
                            pygame.time.delay(100)
                        pygame.mixer.music.unpause()

        if self.man_falling:
            self.man.fall()
            if self.man.y > HEIGHT - fish_img.get_height():
                self.fish_y = self.man.y - fish_img.get_height()  # Fish moves up to eat the man
                if lose_sound:
                    pygame.mixer.music.pause()
                    lose_sound.play()
                    while pygame.mixer.get_busy():
                        pygame.time.delay(100)
                    pygame.mixer.music.unpause()
                self.show_end_screen(win=False)

    def draw(self, screen):
        screen.blit(background_img, (0, 0))  # Draw background

        # Draw sea
        screen.blit(sea_img, (0, self.sea_y))

        # Draw waves (flot.png)
        screen.blit(wave_img, (self.wave_x, self.sea_y - wave_img.get_height()))
        screen.blit(wave_img, (self.wave_x + wave_img.get_width(), self.sea_y - wave_img.get_height()))
        self.wave_x -= self.wave_speed
        if self.wave_x <= -wave_img.get_width():
            self.wave_x = 0

        # Draw platform
        screen.blit(platform_img, self.platform_rect.topleft)

        # Draw pendulum (using the pendulum image directly)
        pendulum_x = self.pivot[0] + self.rod_length * math.sin(self.pendulum_angle)
        pendulum_y = self.pivot[1] + self.rod_length * math.cos(self.pendulum_angle)
        screen.blit(pendulum_img, (pendulum_x - pendulum_img.get_width() // 2, pendulum_y))

        # Draw man
        self.man.draw(screen)

        # Draw hearts (5 hearts)
        for i, heart in enumerate(self.hearts):
            screen.blit(heart, (50 + i * 50, 20))  # Adjusted position

        # Draw fish
        if self.man_falling and self.man.y > HEIGHT - fish_img.get_height():
            screen.blit(fish_img, (self.man.x, self.fish_y))

        # Draw guessed word
        guessed_text = font.render(" ".join(self.guessed_word), True, WHITE)
        screen.blit(guessed_text, (50, HEIGHT - 50))

        # Draw hint
        hint_text = font.render(f"Hint: {self.hint}", True, WHITE)
        screen.blit(hint_text, (50, HEIGHT - 100))

    def show_end_screen(self, win):
        screen.fill(BLACK)
        if win:
            end_text = font.render("You Win! The word was:", True, WHITE)
            word_text = font.render(self.word, True, WHITE)
            hint_text = font.render(f"Hint: {self.hint}", True, WHITE)
        else:
            end_text = font.render("You Lose! The word was:", True, WHITE)
            word_text = font.render(self.word, True, WHITE)
            hint_text = font.render(f"Hint: {self.hint}", True, WHITE)

        screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(word_text, (WIDTH // 2 - word_text.get_width() // 2, HEIGHT // 2))
        screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT // 2 + 50))

        # Draw options
        continue_text = font.render("Press C to Continue", True, WHITE)
        menu_text = font.render("Press M for Main Menu", True, WHITE)
        screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 100))
        screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 150))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:  # Continue with a new word
                        return "continue"
                    if event.key == pygame.K_m:  # Return to main menu
                        return "menu"

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update_pendulum()
            self.draw(screen)
            pygame.display.flip()
            self.clock.tick(60)

            if self.failures >= self.max_failures or "_" not in self.guessed_word:
                result = self.show_end_screen(win=("_" not in self.guessed_word))
                if result == "continue":
                    self.__init__(self.difficulty)  # Restart the game with a new word
                elif result == "menu":
                    return

def main_menu():
    while True:
        screen.blit(background_img, (0, 0))
        title_text = font.render("Le Pendule", True, WHITE)
        easy_text = font.render("Easy", True, WHITE)
        hard_text = font.render("Hard", True, WHITE)

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
        screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, 300))
        screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WIDTH // 2 - 50 <= x <= WIDTH // 2 + 50:
                    if 300 <= y <= 350:
                        game = PendulumGame("easy")
                        game.run()
                    elif 400 <= y <= 450:
                        game = PendulumGame("hard")
                        game.run()

if __name__ == "__main__":
    main_menu()