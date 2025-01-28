<<<<<<< HEAD
# Import necessary libraries 
import pygame
import sys
import math
import os
import subprocess

# Initialize Pygame
pygame.init()

# File paths
FONT_PATH = "fonts/consolab.ttf"
SKY_IMAGE_PATH = "img/sky.png"
SEA_IMAGE_PATH = "img/sea.png"
PLATEFORME_IMAGE_PATH = "img/plateforme.png"
FLOT_IMAGE_PATH = "img/flot.png"
MAN_IMAGE_PATH = "img/man.png"
PEND_IMAGE_PATH = "img/pend.png"
FISH_IMAGE_PATH = "img/fish.png"
LE_IMAGE_PATH = "img/LE.png"
PENDULE_IMAGE_PATH = "img/PENDULE.png"
STATUS_1_IMAGE_PATH = "img/status_1.png"
STATUS_2_IMAGE_PATH = "img/status_2.png"
STATUS_3_IMAGE_PATH = "img/status_3.png"
LOGOW_IMAGE_PATH = "img/logow.png"
MUSIC_PATH = "snd/mer.ogg"
WORDS_FILE_PATH = "txt/mots.txt"
HINTS_FILE_PATH = "txt/indices.txt"

# Check if the font file exists
# Font
font_path = "fonts/consolab.ttf"
if not os.path.exists(FONT_PATH):
    print("Error: Font file not found.")
    pygame.quit()
    sys.exit()

# Load the font
FONT = pygame.font.Font(FONT_PATH, 28)
BUTTON_FONT = pygame.font.Font(FONT_PATH, 18)
SMALL_FONT = pygame.font.Font(FONT_PATH, 20)
HINT_FONT = pygame.font.Font(FONT_PATH, 26)

# Window configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
sky = pygame.image.load(SKY_IMAGE_PATH)
sea = pygame.image.load(SEA_IMAGE_PATH)
plateforme = pygame.image.load(PLATEFORME_IMAGE_PATH)
flot = pygame.image.load(FLOT_IMAGE_PATH)
man = pygame.image.load(MAN_IMAGE_PATH)
pend = pygame.image.load(PEND_IMAGE_PATH)
fish = pygame.image.load(FISH_IMAGE_PATH)
le_image = pygame.image.load(LE_IMAGE_PATH)
pendule_image = pygame.image.load(PENDULE_IMAGE_PATH)
status_1_image = pygame.image.load(STATUS_1_IMAGE_PATH)
status_2_image = pygame.image.load(STATUS_2_IMAGE_PATH)
status_3_image = pygame.image.load(STATUS_3_IMAGE_PATH)
logow_image = pygame.image.load(LOGOW_IMAGE_PATH)

# Resize images
sky = pygame.transform.scale(sky, (800, 450))
sea = pygame.transform.scale(sea, (800, 150))
plateforme = pygame.transform.scale(plateforme, (410, 161))
flot = pygame.transform.scale(flot, (800, 48))
man = pygame.transform.scale(man, (56, 80))
pend = pygame.transform.scale(pend, (70, 280))
fish = pygame.transform.scale(fish, (150, 150))
le_image = pygame.transform.scale(le_image, (115, 82))
pendule_image = pygame.transform.scale(pendule_image, (473, 105))

# Resize status images
status_1_width = pendule_image.get_width()
status_1_height = pendule_image.get_height()
status_1_image = pygame.transform.scale(status_1_image, (int(status_1_width * 1.3), int(status_1_height * 1.45)))
status_2_image = pygame.transform.scale(status_2_image, (int(status_1_width * 1.35), int(status_1_height * 1.45)))
status_3_image = pygame.transform.scale(status_3_image, (int(status_1_width * 1.34), int(status_1_height * 1.44)))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (188, 202, 233)
RED = (255, 73, 47)
GRAY = (150, 150, 150)

# Load and play background music
pygame.mixer.music.load(MUSIC_PATH)
pygame.mixer.music.play(-1)

# Global variables for animation
animation_finished = False
final_pend_y = -10
final_status_image = status_3_image


def draw_button(text, x, y, width, height, color, hover_color, font, screen):
    """Draw a button with a hover effect."""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height), border_radius=15)
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius=15)

    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surf, text_rect)
    return False


def add_word():
    """Allow the user to add a word and a hint."""
    global animation_finished, final_pend_y, final_status_image

    input_active = True
    user_text = ""
    input_box_width = 350
    input_box_height = 50
    input_box_x = (200 + (plateforme.get_width() - input_box_width) // 2)
    input_box_y = (450 - 161 + (plateforme.get_height() - input_box_height) // 2) - 30

    button_width = 100
    button_height = 40
    button_x = input_box_x + (input_box_width - button_width) // 2
    button_y = 450 + (150 - button_height) // 2

    hint_text = "Add a word..."
    clock = pygame.time.Clock()

    cursor_visible = True
    cursor_timer = pygame.time.get_ticks()

    current_step = 0

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_text.strip():
                        if current_step == 0:
                            with open(WORDS_FILE_PATH, "a") as file:
                                file.write(user_text.strip() + "\n")
                            current_step = 1
                            hint_text = "Provide a hint..."
                            user_text = ""
                        elif current_step == 1:
                            with open(HINTS_FILE_PATH, "a") as file:
                                file.write(user_text.strip() + "\n")
                            input_active = False
                    else:
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                    if user_text.strip():
                        if current_step == 0:
                            with open(WORDS_FILE_PATH, "a") as file:
                                file.write(user_text.strip() + "\n")
                            current_step = 1
                            hint_text = "Provide a hint..."
                            user_text = ""
                        elif current_step == 1:
                            with open(HINTS_FILE_PATH, "a") as file:
                                file.write(user_text.strip() + "\n")
                            input_active = False
                    else:
                        input_active = False

        screen.blit(sky, (0, 0))
        screen.blit(sea, (0, 450))
        screen.blit(flot, (0, 450 - 48 + 20))
        screen.blit(plateforme, (200, 450 - 161))
        screen.blit(logow_image, (10, 10))
        screen.blit(final_status_image, (255 - 140, 146 + 30))
        screen.blit(fish, (SCREEN_WIDTH - 170, 360 + 10 * math.sin(pygame.time.get_ticks() / 300)))
        screen.blit(pend, (560, final_pend_y))

        if pygame.time.get_ticks() - cursor_timer > 500:
            cursor_visible = not cursor_visible
            cursor_timer = pygame.time.get_ticks()

        pygame.draw.rect(screen, BLUE, (input_box_x, input_box_y, input_box_width, input_box_height))
        pygame.draw.rect(screen, WHITE, (input_box_x, input_box_y, input_box_width, input_box_height), 2)

        if user_text == "":
            text_surface = HINT_FONT.render(hint_text, True, GRAY)
        else:
            text_surface = HINT_FONT.render(user_text, True, RED)

        screen.blit(text_surface, (input_box_x + 10, input_box_y + (input_box_height - text_surface.get_height()) // 2))

        cursor_x = input_box_x + 10 + (text_surface.get_width() if user_text else 0)
        if cursor_visible:
            pygame.draw.line(screen, RED, (cursor_x, input_box_y + 10), (cursor_x, input_box_y + input_box_height - 10), 2)

        ok_color = BLUE if button_x <= pygame.mouse.get_pos()[0] <= button_x + button_width and button_y <= pygame.mouse.get_pos()[1] <= button_y + button_height else WHITE
        pygame.draw.rect(screen, ok_color, (button_x, button_y, button_width, button_height), border_radius=10)
        pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height), 2, border_radius=10)
        ok_text = BUTTON_FONT.render("OK", True, BLACK)
        screen.blit(ok_text, (button_x + (button_width - ok_text.get_width()) // 2, button_y + (button_height - ok_text.get_height()) // 2))

        pygame.display.update()
        clock.tick(30)
        

def main_menu():
    """Display the main menu and handle interactions."""
    global animation_finished, final_pend_y, final_status_image

    if animation_finished:
        while True:
            screen.blit(sky, (0, 0))
            screen.blit(sea, (0, 450))
            screen.blit(flot, (0, 450 - 48 + 20))
            screen.blit(plateforme, (200, 450 - 161))
            screen.blit(logow_image, (10, 10))

            button_width = 180
            button_height = 45
            button_gap = 20
            button_y = SCREEN_HEIGHT - button_height - 30
            button_x1 = (SCREEN_WIDTH - 3 * button_width - 2 * button_gap) / 4
            button_x2 = button_x1 + button_width + button_gap
            button_x3 = button_x2 + button_width + button_gap

            if draw_button("Easy Level", button_x1, button_y, button_width, button_height, WHITE, BLUE, BUTTON_FONT, screen):
                subprocess.run(["python", "le_Pendule2.py"])

            if draw_button("Hard Level", button_x2, button_y, button_width, button_height, WHITE, BLUE, BUTTON_FONT, screen):
                subprocess.run(["python", "le_Pendule2.py"])

            if draw_button("Add a Word", button_x3, button_y, button_width, button_height, WHITE, BLUE, BUTTON_FONT, screen):
                add_word()

            score_button_x = 10
            score_button_y = logow_image.get_height() + 40
            if draw_button("Scoreboard", score_button_x, score_button_y, button_width, button_height, WHITE, RED, BUTTON_FONT, screen):
                pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
    else:
        le_x = -le_image.get_width()
        pendule_x = SCREEN_WIDTH
        man_y = -man.get_height()
        man_x = 580
        man_fallen = False
        fish_visible = False
        transition_to_status_1 = False

        pend_x = 560
        pend_y = -pend.get_height() - 20
        pend_speed = 10
        status_transition = False
        status_final = False
        pend_stopped = False

        status_1_start_time = 0
        status_1_delay = 2000

        clock = pygame.time.Clock()

        while True:
            screen.blit(sky, (0, 0))
            screen.blit(sea, (0, 450))
            screen.blit(flot, (0, 450 - 48 + 20))
            screen.blit(plateforme, (200, 450 - 161))
            screen.blit(logow_image, (10, 10))

            if le_x < 95:
                le_x += 10
            if pendule_x > 255:
                pendule_x -= 10

            if le_x >= 95 and pendule_x <= 255 and not man_fallen:
                if man_y < 80:
                    man_y += 5 + 2 * math.sin(pygame.time.get_ticks() / 300)
                else:
                    man_y = 80
                    man_fallen = True
                    transition_to_status_1 = True
                    status_1_start_time = pygame.time.get_ticks()

            if not transition_to_status_1:
                screen.blit(le_image, (le_x, 176))
                screen.blit(pendule_image, (pendule_x, 154))
                screen.blit(man, (man_x, man_y))
            else:
                if not status_transition:
                    screen.blit(status_1_image, (255 - 150, 146 - 40))

                    if pygame.time.get_ticks() - status_1_start_time >= status_1_delay:
                        status_transition = True

                if status_transition and pend_y < -1:
                    pend_y += pend_speed

                if status_transition and not status_final:
                    screen.blit(status_2_image, (255 - 150, 146 - 10))

                    if pend_y < 0:
                        pend_y += pend_speed
                    else:
                        status_final = True

                if status_final:
                    screen.blit(final_status_image, (255 - 140, 146 + 30))

                    if pend_y < 0:
                        pend_y += pend_speed
                    else:
                        pend_y = final_pend_y
                        pend_stopped = True
                        animation_finished = True

            if pend_stopped:
                fish_visible = True

                button_width = 180
                button_height = 45
                button_gap = 20
                button_y = SCREEN_HEIGHT - button_height - 30
                button_x1 = (SCREEN_WIDTH - 3 * button_width - 2 * button_gap) / 4
                button_x2 = button_x1 + button_width + button_gap
                button_x3 = button_x2 + button_width + button_gap

                if draw_button("Easy Level", button_x1, button_y, button_width, button_height, WHITE, BLUE, BUTTON_FONT, screen):
                    subprocess.run(["python", "le_Pendule2.py"])

                if draw_button("Hard Level", button_x2, button_y, button_width, button_height, WHITE, BLUE, BUTTON_FONT, screen):
                    return "difficile"
                if draw_button("Add a Word", button_x3, button_y, button_width, button_height, WHITE, BLUE, BUTTON_FONT, screen):
                    add_word()

                score_button_x = 10
                score_button_y = logow_image.get_height() + 40
                if draw_button("Scoreboard", score_button_x, score_button_y, button_width, button_height, WHITE, RED, BUTTON_FONT, screen):
                    pass

                if fish_visible:
                    fish_y = 360 + 10 * math.sin(pygame.time.get_ticks() / 300)
                    screen.blit(fish, (SCREEN_WIDTH - 170, fish_y))

                if pend_stopped:
                    pend_y_offset = 5 * math.sin(pygame.time.get_ticks() / 300)
                    screen.blit(pend, (pend_x, pend_y + pend_y_offset))

            if not pend_stopped and status_transition:
                screen.blit(pend, (pend_x, pend_y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            clock.tick(60)

def main():
    """Main function to run the game."""
    main_menu()

if __name__ == "__main__":
=======
# Import necessary libraries 
import pygame
import sys
import math
import os
import subprocess

# Initialize Pygame
pygame.init()

# File paths
FONT_PATH = "fonts/consolab.ttf"
SKY_IMAGE_PATH = "img/sky.png"
SEA_IMAGE_PATH = "img/sea.png"
PLATEFORME_IMAGE_PATH = "img/plateforme.png"
FLOT_IMAGE_PATH = "img/flot.png"
MAN_IMAGE_PATH = "img/man.png"
PEND_IMAGE_PATH = "img/pend.png"
FISH_IMAGE_PATH = "img/fish.png"
LE_IMAGE_PATH = "img/LE.png"
PENDULE_IMAGE_PATH = "img/PENDULE.png"
STATUS_1_IMAGE_PATH = "img/status_1.png"
STATUS_2_IMAGE_PATH = "img/status_2.png"
STATUS_3_IMAGE_PATH = "img/status_3.png"
LOGOW_IMAGE_PATH = "img/logow.png"
MUSIC_PATH = "snd/mer.ogg"
WORDS_FILE_PATH = "txt/mots.txt"
HINTS_FILE_PATH = "txt/indices.txt"

# Check if the font file exists
# Font
font_path = "fonts/consolab.ttf"
if not os.path.exists(FONT_PATH):
    print("Error: Font file not found.")
    pygame.quit()
    sys.exit()

# Load the font
FONT = pygame.font.Font(FONT_PATH, 28)
BUTTON_FONT = pygame.font.Font(FONT_PATH, 18)
SMALL_FONT = pygame.font.Font(FONT_PATH, 20)
HINT_FONT = pygame.font.Font(FONT_PATH, 26)

# Window configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
sky = pygame.image.load(SKY_IMAGE_PATH)
sea = pygame.image.load(SEA_IMAGE_PATH)
plateforme = pygame.image.load(PLATEFORME_IMAGE_PATH)
flot = pygame.image.load(FLOT_IMAGE_PATH)
man = pygame.image.load(MAN_IMAGE_PATH)
pend = pygame.image.load(PEND_IMAGE_PATH)
fish = pygame.image.load(FISH_IMAGE_PATH)
le_image = pygame.image.load(LE_IMAGE_PATH)
pendule_image = pygame.image.load(PENDULE_IMAGE_PATH)
status_1_image = pygame.image.load(STATUS_1_IMAGE_PATH)
status_2_image = pygame.image.load(STATUS_2_IMAGE_PATH)
status_3_image = pygame.image.load(STATUS_3_IMAGE_PATH)
logow_image = pygame.image.load(LOGOW_IMAGE_PATH)

# Resize images
sky = pygame.transform.scale(sky, (800, 450))
sea = pygame.transform.scale(sea, (800, 150))
plateforme = pygame.transform.scale(plateforme, (410, 161))
flot = pygame.transform.scale(flot, (800, 48))
man = pygame.transform.scale(man, (56, 80))
pend = pygame.transform.scale(pend, (70, 280))
fish = pygame.transform.scale(fish, (150, 150))
le_image = pygame.transform.scale(le_image, (115, 82))
pendule_image = pygame.transform.scale(pendule_image, (473, 105))

# Resize status images
status_1_width = pendule_image.get_width()
status_1_height = pendule_image.get_height()
status_1_image = pygame.transform.scale(status_1_image, (int(status_1_width * 1.3), int(status_1_height * 1.45)))
status_2_image = pygame.transform.scale(status_2_image, (int(status_1_width * 1.35), int(status_1_height * 1.45)))
status_3_image = pygame.transform.scale(status_3_image, (int(status_1_width * 1.34), int(status_1_height * 1.44)))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (188, 202, 233)
RED = (255, 73, 47)
GRAY = (150, 150, 150)

# Load and play background music
pygame.mixer.music.load(MUSIC_PATH)
pygame.mixer.music.play(-1)

# Global variables for animation
animation_finished = False
final_pend_y = -10
final_status_image = status_3_image


def draw_button(text, x, y, width, height, color, hover_color, font, screen):
    """Draw a button with a hover effect."""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height), border_radius=15)
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius=15)

    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surf, text_rect)
    return False


def add_word():
    """Allow the user to add a word and a hint."""
    global animation_finished, final_pend_y, final_status_image

    input_active = True
    user_text = ""
    input_box_width = 350
    input_box_height = 50
    input_box_x = (200 + (plateforme.get_width() - input_box_width) // 2)
    input_box_y = (450 - 161 + (plateforme.get_height() - input_box_height) // 2) - 30

    button_width = 100
    button_height = 40
    button_x = input_box_x + (input_box_width - button_width) // 2
    button_y = 450 + (150 - button_height) // 2

    hint_text = "Add a word..."
    clock = pygame.time.Clock()

    cursor_visible = True
    cursor_timer = pygame.time.get_ticks()

    current_step = 0

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_text.strip():
                        if current_step == 0:
                            with open(WORDS_FILE_PATH, "a") as file:
                                file.write(user_text.strip() + "\n")
                            current_step = 1
                            hint_text = "Provide a hint..."
                            user_text = ""
                        elif current_step == 1:
                            with open(HINTS_FILE_PATH, "a") as file:
                                file.write(user_text.strip() + "\n")
                            input_active = False
                    else:
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                    if user_text.strip():
                        if current_step == 0:
                            with open(WORDS_FILE_PATH, "a") as file:
                                file.write(user_text.strip() + "\n")
                            current_step = 1
                            hint_text = "Provide a hint..."
                            user_text = ""
                        elif current_step == 1:
                            with open(HINTS_FILE_PATH, "a") as file:
                                file.write(user_text.strip() + "\n")
                            input_active = False
                    else:
                        input_active = False

        screen.blit(sky, (0, 0))
        screen.blit(sea, (0, 450))
        screen.blit(flot, (0, 450 - 48 + 20))
        screen.blit(plateforme, (200, 450 - 161))
        screen.blit(logow_image, (10, 10))
        screen.blit(final_status_image, (255 - 140, 146 + 30))
        screen.blit(fish, (SCREEN_WIDTH - 170, 360 + 10 * math.sin(pygame.time.get_ticks() / 300)))
        screen.blit(pend, (560, final_pend_y))

        if pygame.time.get_ticks() - cursor_timer > 500:
            cursor_visible = not cursor_visible
            cursor_timer = pygame.time.get_ticks()

        pygame.draw.rect(screen, BLUE, (input_box_x, input_box_y, input_box_width, input_box_height))
        pygame.draw.rect(screen, WHITE, (input_box_x, input_box_y, input_box_width, input_box_height), 2)

        if user_text == "":
            text_surface = HINT_FONT.render(hint_text, True, GRAY)
        else:
            text_surface = HINT_FONT.render(user_text, True, RED)

        screen.blit(text_surface, (input_box_x + 10, input_box_y + (input_box_height - text_surface.get_height()) // 2))

        cursor_x = input_box_x + 10 + (text_surface.get_width() if user_text else 0)
        if cursor_visible:
            pygame.draw.line(screen, RED, (cursor_x, input_box_y + 10), (cursor_x, input_box_y + input_box_height - 10), 2)

        ok_color = BLUE if button_x <= pygame.mouse.get_pos()[0] <= button_x + button_width and button_y <= pygame.mouse.get_pos()[1] <= button_y + button_height else WHITE
        pygame.draw.rect(screen, ok_color, (button_x, button_y, button_width, button_height), border_radius=10)
        pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height), 2, border_radius=10)
        ok_text = BUTTON_FONT.render("OK", True, BLACK)
        screen.blit(ok_text, (button_x + (button_width - ok_text.get_width()) // 2, button_y + (button_height - ok_text.get_height()) // 2))

        pygame.display.update()
        clock.tick(30)
        

def main_menu():
    """Display the main menu and handle interactions."""
    global animation_finished, final_pend_y, final_status_image

    if animation_finished:
        while True:
            screen.blit(sky, (0, 0))
            screen.blit(sea, (0, 450))
            screen.blit(flot, (0, 450 - 48 + 20))
            screen.blit(plateforme, (200, 450 - 161))
            screen.blit(logow_image, (10, 10))

            button_width = 180
            button_height = 45
            button_gap = 20
            button_y = SCREEN_HEIGHT - button_height - 30
            button_x1 = (SCREEN_WIDTH - 3 * button_width - 2 * button_gap) / 4
            button_x2 = button_x1 + button_width + button_gap
            button_x3 = button_x2 + button_width + button_gap

            if draw_button("Easy Level", button_x1, button_y, button_width, button_height, WHITE, BLUE, BUTTON_FONT, screen):
                subprocess.run(["python", "le_Pendule2.py"])

            if draw_button("Hard Level", button_x2, button_y, button_width, button_height, WHITE, BLUE, BUTTON_FONT, screen):
                subprocess.run(["python", "le_Pendule2.py"])

            if draw_button("Add a Word", button_x3, button_y, button_width, button_height, WHITE, BLUE, BUTTON_FONT, screen):
                add_word()

            score_button_x = 10
            score_button_y = logow_image.get_height() + 40
            if draw_button("Scoreboard", score_button_x, score_button_y, button_width, button_height, WHITE, RED, BUTTON_FONT, screen):
                pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
    else:
        le_x = -le_image.get_width()
        pendule_x = SCREEN_WIDTH
        man_y = -man.get_height()
        man_x = 580
        man_fallen = False
        fish_visible = False
        transition_to_status_1 = False

        pend_x = 560
        pend_y = -pend.get_height() - 20
        pend_speed = 10
        status_transition = False
        status_final = False
        pend_stopped = False

        status_1_start_time = 0
        status_1_delay = 2000

        clock = pygame.time.Clock()

        while True:
            screen.blit(sky, (0, 0))
            screen.blit(sea, (0, 450))
            screen.blit(flot, (0, 450 - 48 + 20))
            screen.blit(plateforme, (200, 450 - 161))
            screen.blit(logow_image, (10, 10))

            if le_x < 95:
                le_x += 10
            if pendule_x > 255:
                pendule_x -= 10

            if le_x >= 95 and pendule_x <= 255 and not man_fallen:
                if man_y < 80:
                    man_y += 5 + 2 * math.sin(pygame.time.get_ticks() / 300)
                else:
                    man_y = 80
                    man_fallen = True
                    transition_to_status_1 = True
                    status_1_start_time = pygame.time.get_ticks()

            if not transition_to_status_1:
                screen.blit(le_image, (le_x, 176))
                screen.blit(pendule_image, (pendule_x, 154))
                screen.blit(man, (man_x, man_y))
            else:
                if not status_transition:
                    screen.blit(status_1_image, (255 - 150, 146 - 40))

                    if pygame.time.get_ticks() - status_1_start_time >= status_1_delay:
                        status_transition = True

                if status_transition and pend_y < -1:
                    pend_y += pend_speed

                if status_transition and not status_final:
                    screen.blit(status_2_image, (255 - 150, 146 - 10))

                    if pend_y < 0:
                        pend_y += pend_speed
                    else:
                        status_final = True

                if status_final:
                    screen.blit(final_status_image, (255 - 140, 146 + 30))

                    if pend_y < 0:
                        pend_y += pend_speed
                    else:
                        pend_y = final_pend_y
                        pend_stopped = True
                        animation_finished = True

            if pend_stopped:
                fish_visible = True

                button_width = 180
                button_height = 45
                button_gap = 20
                button_y = SCREEN_HEIGHT - button_height - 30
                button_x1 = (SCREEN_WIDTH - 3 * button_width - 2 * button_gap) / 4
                button_x2 = button_x1 + button_width + button_gap
                button_x3 = button_x2 + button_width + button_gap

                if draw_button("Easy Level", button_x1, button_y, button_width, button_height, WHITE, BLUE, BUTTON_FONT, screen):
                    subprocess.run(["python", "le_Pendule2.py"])

                if draw_button("Hard Level", button_x2, button_y, button_width, button_height, WHITE, BLUE, BUTTON_FONT, screen):
                    return "difficile"
                if draw_button("Add a Word", button_x3, button_y, button_width, button_height, WHITE, BLUE, BUTTON_FONT, screen):
                    add_word()

                score_button_x = 10
                score_button_y = logow_image.get_height() + 40
                if draw_button("Scoreboard", score_button_x, score_button_y, button_width, button_height, WHITE, RED, BUTTON_FONT, screen):
                    pass

                if fish_visible:
                    fish_y = 360 + 10 * math.sin(pygame.time.get_ticks() / 300)
                    screen.blit(fish, (SCREEN_WIDTH - 170, fish_y))

                if pend_stopped:
                    pend_y_offset = 5 * math.sin(pygame.time.get_ticks() / 300)
                    screen.blit(pend, (pend_x, pend_y + pend_y_offset))

            if not pend_stopped and status_transition:
                screen.blit(pend, (pend_x, pend_y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            clock.tick(60)

def main():
    """Main function to run the game."""
    main_menu()

if __name__ == "__main__":
>>>>>>> e2ef18dd9070e47b64f50bddbcd7fd0cda1d3de5
    main()