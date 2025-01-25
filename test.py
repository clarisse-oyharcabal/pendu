import pygame
import sys
import math
import os

# Initialisation de Pygame
pygame.init()

# Police
font_path = "fonts/consolab.ttf"
if not os.path.exists(font_path):
    print("Erreur : Le fichier de police n'a pas été trouvé.")
    pygame.quit()
    sys.exit()
else:
    font = pygame.font.Font(font_path, 28)
    button_font = pygame.font.Font(font_path, 18)
    small_font = pygame.font.Font(font_path, 20)

hint_font = pygame.font.Font(font_path, 26)

# Configuration de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Chargement des images
sky = pygame.image.load("img/sky.png")
sea = pygame.image.load("img/sea.png")
plateforme = pygame.image.load("img/plateforme.png")
flot = pygame.image.load("img/flot.png")
man = pygame.image.load("img/man.png")
pend = pygame.image.load("img/pend.png")
fish = pygame.image.load("img/fish.png")
le_image = pygame.image.load("img/LE.png")
pendule_image = pygame.image.load("img/PENDULE.png")

# Redimensionnement des images
sky = pygame.transform.scale(sky, (800, 450))
sea = pygame.transform.scale(sea, (800, 150))
plateforme = pygame.transform.scale(plateforme, (410, 161))
flot = pygame.transform.scale(flot, (800, 48))
man = pygame.transform.scale(man, (66, 100))
pend = pygame.transform.scale(pend, (90, 344))
fish = pygame.transform.scale(fish, (150, 150))
le_image = pygame.transform.scale(le_image, (119, 86))
pendule_image = pygame.transform.scale(pendule_image, (477, 109))

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (188, 202, 233)
ROUGE = (255, 0, 0)
GRIS = (150, 150, 150)

# Fonction pour dessiner les boutons
def draw_button(text, x, y, width, height, color, hover_color, font, screen):
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

# Fonction pour ajouter un mot
def add_word():
    input_active = True
    user_text = ""
    input_box_width = 350
    input_box_height = 50
    input_box_x = (200 + (plateforme.get_width() - input_box_width) // 2)
    input_box_y = (450 - 161 + (plateforme.get_height() - input_box_height) // 2) - 30

    hint_text = "Ajouter un mot..."  # Texte d'indication
    clock = pygame.time.Clock()

    # Variables pour le curseur clignotant
    cursor_visible = True
    cursor_timer = pygame.time.get_ticks()

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enregistrer le mot
                    if user_text.strip():  # Vérifie si le mot n'est pas vide
                        with open("mots.txt", "a") as file:
                            file.write(user_text.strip() + "\n")
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:  # Effacer un caractère
                    user_text = user_text[:-1]
                else:  # Ajouter un caractère
                    user_text += event.unicode

        # Redessiner tous les éléments existants
        screen.blit(sky, (0, 0))
        screen.blit(sea, (0, 450))
        screen.blit(flot, (0, 450 - 48 + 20))
        screen.blit(plateforme, (200, 450 - 161))
        screen.blit(man, (585, 80))
        fish_y = 330 + 10 * math.sin(pygame.time.get_ticks() / 300)
        screen.blit(fish, (screen_width - 170, fish_y))
        screen.blit(le_image, (95, 168))
        screen.blit(pendule_image, (255, 146))

        # Gérer le clignotement du curseur
        if pygame.time.get_ticks() - cursor_timer > 500:
            cursor_visible = not cursor_visible
            cursor_timer = pygame.time.get_ticks()

        # Afficher la barre d'insertion
        pygame.draw.rect(screen, BLUE, (input_box_x, input_box_y, input_box_width, input_box_height))
        pygame.draw.rect(screen, WHITE, (input_box_x, input_box_y, input_box_width, input_box_height), 2)

        # Gérer le texte d'indication ou le texte de l'utilisateur
        if user_text == "":
            text_surface = hint_font.render(hint_text, True, GRIS)   # Texte grisé
        else:
            text_surface = small_font.render(user_text, True, ROUGE)
        
        screen.blit(text_surface, (input_box_x + 10, input_box_y + 5)) 

        # Dessiner le curseur si nécessaire
        if cursor_visible:
            cursor_x = input_box_x + 10 + text_surface.get_width()
            pygame.draw.line(screen, ROUGE, (input_box_x + 10, input_box_y + 5), (input_box_x + 10, input_box_y + 25), 2)

        pygame.display.update()
        clock.tick(30)

# Fonction pour le menu principal avec animation
def main_menu():
    le_x = -le_image.get_width()  # Départ à gauche
    pendule_x = screen_width  # Départ à droite
    man_y = -man.get_height()  # Départ en haut
    man_x = 585
    man_fallen = False
    fish_visible = False

    clock = pygame.time.Clock()

    while True:
        screen.blit(sky, (0, 0))
        screen.blit(sea, (0, 450))
        screen.blit(flot, (0, 450 - 48 + 20))
        screen.blit(plateforme, (200, 450 - 161))

        # Animation d'apparition pour "LE" et "PENDULE"
        if le_x < 95:
            le_x += 10
        if pendule_x > 255:
            pendule_x -= 10

        screen.blit(le_image, (le_x, 168))
        screen.blit(pendule_image, (pendule_x, 146))

        # Animation de descente pour "man"
        if le_x >= 95 and pendule_x <= 255 and not man_fallen:
            if man_y < 80:
                man_y += 5 + 2 * math.sin(pygame.time.get_ticks() / 300)
            else:
                man_y = 80
                man_fallen = True

        screen.blit(man, (man_x, man_y))

        # Afficher "fish" et les boutons après la descente de "man"
        if man_fallen:
            fish_visible = True

            # Boutons
            button_width = 180
            button_height = 45
            button_gap = 20
            button_y = screen_height - button_height - 30
            button_x1 = (screen_width - 3 * button_width - 2 * button_gap) / 4
            button_x2 = button_x1 + button_width + button_gap
            button_x3 = button_x2 + button_width + button_gap

            if draw_button("Niveau Facile", button_x1, button_y, button_width, button_height, WHITE, BLUE, button_font, screen):
                return "facile"
            if draw_button("Niveau Difficile", button_x2, button_y, button_width, button_height, WHITE, BLUE, button_font, screen):
                return "difficile"
            if draw_button("Ajouter un mot", button_x3, button_y, button_width, button_height, WHITE, BLUE, button_font, screen):
                add_word()

            if fish_visible:
                fish_y = 330 + 10 * math.sin(pygame.time.get_ticks() / 300)
                screen.blit(fish, (screen_width - 170, fish_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)

# Fonction principale
def main():
    main_menu()

if __name__ == "__main__":
    main()