import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pendulum Strike Game")

# Colors
SKY_BLUE = (135, 206, 235)
DARK_BLUE = (0, 0, 139)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load custom images
try:
    platform_image = pygame.image.load("platform.png")  # Replace with your platform image file
    background_image = pygame.image.load("background.jpg")  # Replace with your background image file
except FileNotFoundError:
    print("Error: Custom images not found. Using solid colors instead.")
    platform_image = None
    background_image = None

class Man:
    def __init__(self, x, y, platform_width):
        self.start_x = x
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.steps = 0
        self.platform_width = platform_width
        self.move_distance = platform_width * 0.2  # 20% of the platform width
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = -1  # -1 for left, 1 for right

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x + self.width // 2, self.y + 20), 15)
        pygame.draw.line(screen, RED, 
            (self.x + self.width // 2, self.y + 20), 
            (self.x + self.width // 2, self.y + self.height), 2)
        pygame.draw.line(screen, RED, 
            (self.x + self.width // 2, self.y + 35), 
            (self.x + self.width // 2 - 15, self.y + 50), 2)
        pygame.draw.line(screen, RED, 
            (self.x + self.width // 2, self.y + 35), 
            (self.x + self.width // 2 + 15, self.y + 50), 2)
        pygame.draw.line(screen, RED, 
            (self.x + self.width // 2, self.y + self.height), 
            (self.x + self.width // 2 - 10, self.y + self.height + 20), 2)
        pygame.draw.line(screen, RED, 
            (self.x + self.width // 2, self.y + self.height), 
            (self.x + self.width // 2 + 10, self.y + self.height + 20), 2)

    def move(self):
        self.x += self.direction * self.move_distance
        self.steps += 1

    def fall(self):
        self.velocity_y += 0.5
        self.x += self.velocity_x
        self.y += self.velocity_y

class PendulumGame:
    def __init__(self):
        self.initial_pivot = [WIDTH // 2, 100]
        self.pivot = self.initial_pivot.copy()
        self.rod_length = 300
        self.pendulum_angle = math.pi / 4
        self.pendulum_velocity = 0
        self.gravity = 0.005

        self.platform_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 150, 200, 20)
        self.man = Man(
            self.platform_rect.x + self.platform_rect.width // 2 - 20, 
            self.platform_rect.y - 100,
            self.platform_rect.width
        )
        self.man_falling = False

        self.sea_y = HEIGHT
        self.sea_speed = 5

        self.strike_button_rect = pygame.Rect(10, 10, 150, 40)  # Strike button
        self.stop_button_rect = pygame.Rect(170, 10, 150, 40)   # Stop button
        self.strike_triggered = False
        self.game_running = True  # Flag to control game state
        self.font = pygame.font.Font(None, 36)

        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.strike_button_rect.collidepoint(event.pos):
                    self.strike_triggered = True
                if self.stop_button_rect.collidepoint(event.pos):
                    self.game_running = False  # Stop the game
        return True

    def update_pendulum(self):
        if self.strike_triggered and self.man.steps < 3:
            self.pendulum_acceleration = -self.gravity * math.sin(self.pendulum_angle)
            self.pendulum_velocity += self.pendulum_acceleration
            self.pendulum_angle += self.pendulum_velocity
            self.pendulum_velocity *= 0.99

            pendulum_x = self.pivot[0] + self.rod_length * math.sin(self.pendulum_angle)
            pendulum_y = self.pivot[1] + self.rod_length * math.cos(self.pendulum_angle)

            man_rect = pygame.Rect(self.man.x, self.man.y, self.man.width, self.man.height)
            if man_rect.collidepoint((pendulum_x, pendulum_y)):
                self.man.move()
                
                # Move the pivot point the same distance as the man
                self.pivot[0] += self.man.direction * self.man.move_distance
                
                # Reinitialize pendulum
                self.pendulum_angle = math.pi / 4
                self.pendulum_velocity = 0
                
                self.strike_triggered = False

        if self.man.steps >= 3 and not self.man_falling:
            self.man_falling = True
            self.man.velocity_x = -3  # Fall to the left
            self.man.velocity_y = -5

        if self.man_falling:
            self.man.fall()
            self.sea_y -= self.sea_speed
            if self.sea_y < HEIGHT - 100:
                self.sea_y = HEIGHT

    def draw(self, screen):
        # Draw background
        if background_image:
            screen.blit(background_image, (0, 0))  # Draw custom background
        else:
            screen.fill(SKY_BLUE)  # Fallback to solid color

        # Draw Strike button
        pygame.draw.rect(screen, (65, 105, 225), self.strike_button_rect)
        strike_text = self.font.render("Strike!", True, WHITE)
        screen.blit(strike_text, (self.strike_button_rect.x + 10, self.strike_button_rect.y + 5))

        # Draw Stop button
        pygame.draw.rect(screen, (65, 105, 225), self.stop_button_rect)
        stop_text = self.font.render("Stop", True, WHITE)
        screen.blit(stop_text, (self.stop_button_rect.x + 10, self.stop_button_rect.y + 5))

        pendulum_x = self.pivot[0] + self.rod_length * math.sin(self.pendulum_angle)
        pendulum_y = self.pivot[1] + self.rod_length * math.cos(self.pendulum_angle)
        
        pygame.draw.line(screen, WHITE, self.pivot, (pendulum_x, pendulum_y), 2)
        pygame.draw.polygon(screen, WHITE, [
            (pendulum_x, pendulum_y + 50),
            (pendulum_x - 25, pendulum_y),
            (pendulum_x + 25, pendulum_y)
        ])

        # Draw platform
        if platform_image:
            screen.blit(platform_image, (self.platform_rect.x, self.platform_rect.y))  # Draw custom platform
        else:
            pygame.draw.rect(screen, (65, 105, 225), self.platform_rect)  # Fallback to solid color

        self.man.draw(screen)
        pygame.draw.rect(screen, DARK_BLUE, (0, self.sea_y, WIDTH, HEIGHT - self.sea_y))

    def run(self):
        running = True
        while running and self.game_running:  # Stop the loop if game_running is False
            running = self.handle_events()
            self.update_pendulum()
            self.draw(screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = PendulumGame()
    game.run()