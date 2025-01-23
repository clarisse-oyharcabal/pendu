import pygame
import math
import random

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Le Pendule")

# Colors
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load images
sea_img = pygame.image.load("sea.png")
platform_img = pygame.image.load("laplateforme.png")
man_img = pygame.image.load("man.png")
wave_img = pygame.image.load("flot.png")
pendulum_img = pygame.image.load("pend.png")
fish_img = pygame.image.load("fish.png")
star_img = pygame.image.load("star.png")

# Resize man image to make it smaller
man_img = pygame.transform.scale(man_img, (30, 50))  # Adjusted size
fish_img = pygame.transform.scale(fish_img, (60, 100))  # Fish is twice the size of the man

# Fonts
font = pygame.font.Font(None, 36)

# Word lists for difficulty levels
easy_words = [
    ("algorithm", "A step-by-step procedure for solving a problem."),
    ("binary", "A system of numerical notation with base 2."),
    ("code", "Instructions written in a programming language."),
    ("data", "Information processed or stored by a computer."),
    ("debug", "To find and fix errors in code."),
    ("encrypt", "To convert data into a code to prevent unauthorized access."),
    ("file", "A collection of data stored in a computer."),
    ("function", "A block of code that performs a specific task."),
    ("input", "Data provided to a computer program."),
    ("loop", "A sequence of instructions that repeats until a condition is met."),
    # Add 90 more words with hints...
]

complex_words = [
    ("asymptotic", "Describes the behavior of a function as it approaches a limit."),
    ("heuristic", "A problem-solving approach that uses practical methods."),
    ("polymorphism", "The ability of a function to operate on multiple types."),
    ("recursion", "A function that calls itself."),
    ("syntax", "The set of rules that define the structure of a language."),
    ("tuple", "An immutable sequence of elements."),
    ("virtualization", "Creating a virtual version of something, like an operating system."),
    ("abstraction", "The concept of hiding complex details while showing only essential features."),
    ("cache", "A hardware or software component that stores data for faster access."),
    ("compiler", "A program that translates code from one language to another."),
    # Add 90 more words with hints...
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
        self.max_failures = 6

        self.initial_pivot = [WIDTH // 2, 100]
        self.pivot = self.initial_pivot.copy()
        self.rod_length = 300
        self.pendulum_angle = math.pi / 4
        self.pendulum_velocity = 0
        self.gravity = 0.005
        self.strike_triggered = False

        self.platform_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 200, 200, 20)  # Platform above waves
        self.man = Man(
            self.platform_rect.x + self.platform_rect.width // 2 - 15,  # Adjusted position
            self.platform_rect.y - man_img.get_height(),  # Feet on the platform
            self.platform_rect.width
        )
        self.man_falling = False

        self.sea_y = HEIGHT - sea_img.get_height() + 50  # Waves slightly lower
        self.wave_x = 0
        self.wave_speed = 2

        self.stars = [star_img.get_rect(topleft=(50 + i * 50, 20)) for i in range(self.max_failures)]
        self.fish_y = HEIGHT  # Fish starts below the screen
        self.fish_speed = 5

        self.clock = pygame.time.Clock()

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
            for i, char in enumerate(self.word):
                if char == letter:
                    self.guessed_word[i] = letter
        else:
            self.failures += 1
            if self.failures < self.max_failures:
                self.strike_triggered = True  # Pendulum strikes only after a wrong guess
                self.man.move()  # Move the man closer to the edge
            else:
                self.man_falling = True

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
                self.pendulum_angle = math.pi / 4
                self.pendulum_velocity = 0

        if self.man_falling:
            self.man.fall()
            if self.man.y > HEIGHT - fish_img.get_height():
                self.fish_y -= self.fish_speed  # Fish moves up to eat the man

    def draw(self, screen):
        screen.fill(SKY_BLUE)

        # Draw sea
        screen.blit(sea_img, (0, self.sea_y))

        # Draw waves
        screen.blit(wave_img, (self.wave_x, self.sea_y - wave_img.get_height()))
        screen.blit(wave_img, (self.wave_x + wave_img.get_width(), self.sea_y - wave_img.get_height()))
        self.wave_x -= self.wave_speed
        if self.wave_x <= -wave_img.get_width():
            self.wave_x = 0

        # Draw platform
        screen.blit(platform_img, self.platform_rect.topleft)

        # Draw pendulum
        pendulum_x = self.pivot[0] + self.rod_length * math.sin(self.pendulum_angle)
        pendulum_y = self.pivot[1] + self.rod_length * math.cos(self.pendulum_angle)
        pygame.draw.line(screen, WHITE, self.pivot, (pendulum_x, pendulum_y), 2)
        screen.blit(pendulum_img, (pendulum_x - pendulum_img.get_width() // 2, pendulum_y))

        # Draw man
        self.man.draw(screen)

        # Draw stars
        for i in range(self.max_failures - self.failures):
            screen.blit(star_img, self.stars[i])

        # Draw fish
        if self.man_falling and self.man.y > HEIGHT - fish_img.get_height():
            screen.blit(fish_img, (self.man.x, self.fish_y))

        # Draw guessed word
        guessed_text = font.render(" ".join(self.guessed_word), True, WHITE)
        screen.blit(guessed_text, (50, HEIGHT - 50))

        # Draw hint
        hint_text = font.render(f"Hint: {self.hint}", True, WHITE)
        screen.blit(hint_text, (50, HEIGHT - 100))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update_pendulum()
            self.draw(screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

def main_menu():
    screen.fill(SKY_BLUE)
    title_text = font.render("Le Pendule", True, WHITE)
    easy_text = font.render("Easy", True, WHITE)
    hard_text = font.render("Hard", True, WHITE)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, 300))
    screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, 400))

    pygame.display.flip()

    while True:
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
                        return
                    elif 400 <= y <= 450:
                        game = PendulumGame("hard")
                        game.run()
                        return

if __name__ == "__main__":
    main_menu()