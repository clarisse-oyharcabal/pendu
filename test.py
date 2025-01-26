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
status_1_image = pygame.image.load("img/status_1.png")  # Charger l'image combinée
status_2_image = pygame.image.load("img/status_2.png")  # Charger l'image combinée
status_3_image = pygame.image.load("img/status_3.png")  # Charger l'image combinée
logow_image = pygame.image.load("img/logow.png")  # Charger l'image logow.png

# Redimensionnement des images
sky = pygame.transform.scale(sky, (800, 450))
sea = pygame.transform.scale(sea, (800, 150))
plateforme = pygame.transform.scale(plateforme, (410, 161))
flot = pygame.transform.scale(flot, (800, 48))
man = pygame.transform.scale(man, (56, 80))
pend = pygame.transform.scale(pend, (70, 280))
fish = pygame.transform.scale(fish, (150, 150))
le_image = pygame.transform.scale(le_image, (115, 82))
pendule_image = pygame.transform.scale(pendule_image, (473, 105))

# Redimensionner status_1.png, status_2.png et status_3.png pour qu'ils correspondent à la zone combinée
status_1_width = pendule_image.get_width()  # Largeur de pendule.png
status_1_height = pendule_image.get_height()  # Hauteur de pendule.png
status_1_image = pygame.transform.scale(status_1_image, (int(status_1_width * 1.3), int(status_1_height * 1.45)))
status_2_image = pygame.transform.scale(status_2_image, (int(status_1_width * 1.35), int(status_1_height * 1.45)))
status_3_image = pygame.transform.scale(status_3_image, (int(status_1_width * 1.34), int(status_1_height * 1.44)))

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (188, 202, 233)
ROUGE = (255, 69, 0)
GRIS = (150, 150, 150)

# Charger et jouer le fond sonore
pygame.mixer.music.load("snd/mer.ogg")  # Assurez-vous que le fichier mer.ogg est présent
pygame.mixer.music.play(-1)  # Jouer en boucle

# Variables globales pour stocker l'état final de l'animation
animation_finished = False  # Indique si l'animation est terminée
final_pend_y = -10  # Position finale de pend.png
final_status_image = status_3_image  # Image finale (status_3)

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

    hint_text = "Ajouter un mot..."  # Texte d'indication initial
    clock = pygame.time.Clock()

    # Variables pour le curseur clignotant
    cursor_visible = True
    cursor_timer = pygame.time.get_ticks()

    # Étape actuelle : 0 pour ajouter un mot, 1 pour donner un indice
    current_step = 0

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enregistrer le mot ou l'indice
                    if user_text.strip():  # Vérifie si le texte n'est pas vide
                        if current_step == 0:
                            # Enregistrer le mot
                            with open("txt/mots.txt", "a") as file:
                                file.write(user_text.strip() + "\n")
                            # Passer à l'étape suivante : donner un indice
                            current_step = 1
                            hint_text = "Donner un indice..."
                            user_text = ""  # Réinitialiser le texte de l'utilisateur
                        elif current_step == 1:
                            # Enregistrer l'indice
                            with open("txt/indices.txt", "a") as file:
                                file.write(user_text.strip() + "\n")
                            input_active = False  # Retourner au menu principal
                    else:
                        input_active = False  # Retourner au menu principal si le texte est vide
                elif event.key == pygame.K_BACKSPACE:  # Effacer un caractère
                    user_text = user_text[:-1]
                else:  # Ajouter un caractère
                    user_text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Vérifier si le bouton "OK" est cliqué
                if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                    if user_text.strip():  # Enregistrer le mot ou l'indice si non vide
                        if current_step == 0:
                            # Enregistrer le mot
                            with open("txt/mots.txt", "a") as file:
                                file.write(user_text.strip() + "\n")
                            # Passer à l'étape suivante : donner un indice
                            current_step = 1
                            hint_text = "Donner un indice..."
                            user_text = ""  # Réinitialiser le texte de l'utilisateur
                        elif current_step == 1:
                            # Enregistrer l'indice
                            with open("txt/indices.txt", "a") as file:
                                file.write(user_text.strip() + "\n")
                            input_active = False  # Retourner au menu principal
                    else:
                        input_active = False  # Retourner au menu principal si le texte est vide

        # Redessiner tous les éléments existants
        screen.blit(sky, (0, 0))
        screen.blit(sea, (0, 450))
        screen.blit(flot, (0, 450 - 48 + 20))
        screen.blit(plateforme, (200, 450 - 161))
        screen.blit(logow_image, (10, 10))  # Afficher logow.png en haut à gauche
        screen.blit(final_status_image, (255 - 140, 146 + 30))  # Afficher status_3 directement
        screen.blit(fish, (screen_width - 170, 360 + 10 * math.sin(pygame.time.get_ticks() / 300)))
        screen.blit(pend, (560, final_pend_y))  # Afficher pend.png à sa position finale

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
            text_surface = hint_font.render(user_text, True, ROUGE)

        screen.blit(text_surface, (input_box_x + 10, input_box_y + (input_box_height - text_surface.get_height()) // 2))

        # Dessiner le curseur si nécessaire
        cursor_x = input_box_x + 10 + (text_surface.get_width() if user_text else 0)
        if cursor_visible:
            pygame.draw.line(screen, ROUGE, (cursor_x, input_box_y + 10), (cursor_x, input_box_y + input_box_height - 10), 2)

        # Dessiner le bouton "OK"
        ok_color = BLUE if button_x <= pygame.mouse.get_pos()[0] <= button_x + button_width and button_y <= pygame.mouse.get_pos()[1] <= button_y + button_height else WHITE
        pygame.draw.rect(screen, ok_color, (button_x, button_y, button_width, button_height), border_radius=10)
        pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height), 2, border_radius=10)
        ok_text = button_font.render("OK", True, BLACK)
        screen.blit(ok_text, (button_x + (button_width - ok_text.get_width()) // 2, button_y + (button_height - ok_text.get_height()) // 2))

        pygame.display.update()
        clock.tick(30)

    # Retour au menu principal sans réinitialiser l'animation
    return

# Fonction pour le menu principal
def main_menu():
    global animation_finished, final_pend_y, final_status_image

    # Si l'animation est déjà terminée, afficher directement l'état final
    if animation_finished:
        while True:
            screen.blit(sky, (0, 0))
            screen.blit(sea, (0, 450))
            screen.blit(flot, (0, 450 - 48 + 20))
            screen.blit(plateforme, (200, 450 - 161))
            screen.blit(logow_image, (10, 10))  # Afficher logow.png en haut à gauche
            screen.blit(final_status_image, (255 - 140, 146 + 30))  # Afficher status_3 directement
            screen.blit(fish, (screen_width - 170, 360 + 10 * math.sin(pygame.time.get_ticks() / 300)))
            screen.blit(pend, (560, final_pend_y))  # Afficher pend.png à sa position finale

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
                add_word()  # Appeler la fonction add_word

            # Ajouter le bouton "Tableau des scores" en dessous de logow.png
            score_button_x = 10  # Position X en dessous de logow.png
            score_button_y = logow_image.get_height() + 40  # Position Y en dessous de logow.png
            if draw_button("Tableau des scores", score_button_x, score_button_y, button_width, button_height, WHITE, ROUGE, button_font, screen):
                pass  # Pour l'instant, il ne mène à rien

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
    else:
        # Sinon, exécuter l'animation normale
        le_x = -le_image.get_width()  # Départ à gauche
        pendule_x = screen_width  # Départ à droite
        man_y = -man.get_height()  # Départ en haut
        man_x = 580
        man_fallen = False
        fish_visible = False
        transition_to_status_1 = False  # Variable pour gérer la transition

        # Variables pour l'animation de pend.png et status
        pend_x = 560  # Position initiale de pend.png (plus à droite)
        pend_y = -pend.get_height() - 20   # Départ en haut
        pend_speed = 10  # Vitesse de descente de pend.png (augmentée pour accélérer)
        status_transition = False  # Pour gérer la transition entre status_1.png et status_2.png
        status_final = False  # Pour gérer la transition entre status_2.png et status_3.png
        pend_stopped = False  # Variable pour indiquer que pend.png s'est arrêté

        # Variables pour le délai de 2 secondes
        status_1_start_time = 0  # Temps auquel status_1.png commence à être affiché
        status_1_delay = 2000  # Délai de 2 secondes (en millisecondes)

        clock = pygame.time.Clock()

        while True:
            screen.blit(sky, (0, 0))
            screen.blit(sea, (0, 450))
            screen.blit(flot, (0, 450 - 48 + 20))
            screen.blit(plateforme, (200, 450 - 161))
            screen.blit(logow_image, (10, 10))  # Afficher logow.png en haut à gauche

            # Animation d'apparition pour "LE" et "PENDULE"
            if le_x < 95:
                le_x += 10
            if pendule_x > 255:
                pendule_x -= 10

            # Animation de descente pour "man"
            if le_x >= 95 and pendule_x <= 255 and not man_fallen:
                if man_y < 80:
                    man_y += 5 + 2 * math.sin(pygame.time.get_ticks() / 300)
                else:
                    man_y = 80
                    man_fallen = True
                    transition_to_status_1 = True  # Activer la transition
                    status_1_start_time = pygame.time.get_ticks()  # Enregistrer le temps de début

            # Afficher les éléments individuels ou status_1.png
            if not transition_to_status_1:
                screen.blit(le_image, (le_x, 176))
                screen.blit(pendule_image, (pendule_x, 154))
                screen.blit(man, (man_x, man_y))
            else:
                # Afficher status_1.png une fois la transition activée
                if not status_transition:
                    screen.blit(status_1_image, (255 - 150, 146 - 40))  # Décalé de 50 pixels à gauche et 30 pixels vers le haut

                    # Attendre 2 secondes avant de faire descendre pend.png
                    if pygame.time.get_ticks() - status_1_start_time >= status_1_delay:
                        status_transition = True  # Activer la transition vers status_2.png

                # Faire descendre pend.png
                if status_transition and pend_y < -1:  # Nouvelle limite de descente (pend.png s'arrête plus haut)
                    pend_y += pend_speed

                # Transition vers status_2.png
                if status_transition and not status_final:
                    screen.blit(status_2_image, (255 - 150, 146 - 10))  # Remplacer status_1.png par status_2.png

                    # Transition progressive vers status_3.png
                    if pend_y < 0:  # Limite de descente avant la transition finale
                        pend_y += pend_speed
                    else:
                        status_final = True  # Activer la transition finale

                # Transition finale vers status_3.png
                if status_final:
                    screen.blit(final_status_image, (255 - 140, 146 + 30))  # Remplacer status_2.png par status_3.png

                    # Arrêter pend.png en haut à droite
                    if pend_y < 0:  # Limite de descente finale
                        pend_y += pend_speed
                    else:
                        pend_y = final_pend_y  # Arrêter pend.png
                        pend_stopped = True  # Indiquer que pend.png s'est arrêté
                        animation_finished = True  # Marquer l'animation comme terminée

            # Afficher "fish" et les boutons uniquement lorsque pend.png s'est arrêté
            if pend_stopped:
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
                    add_word()  # Appeler la fonction add_word

                # Ajouter le bouton "Tableau des scores" en dessous de logow.png
                score_button_x = 10  # Position X en dessous de logow.png
                score_button_y = logow_image.get_height() + 40  # Position Y en dessous de logow.png
                if draw_button("Tableau des scores", score_button_x, score_button_y, button_width, button_height, WHITE, ROUGE, button_font, screen):
                    pass  # Pour l'instant, il ne mène à rien

                if fish_visible:
                    fish_y = 360 + 10 * math.sin(pygame.time.get_ticks() / 300)
                    screen.blit(fish, (screen_width - 170, fish_y))

                # Faire osciller pend.png légèrement une fois qu'il a atteint sa position finale
                if pend_stopped:
                    pend_y_offset = 5 * math.sin(pygame.time.get_ticks() / 300)  # Oscillation légère
                    screen.blit(pend, (pend_x, pend_y + pend_y_offset))

            # Ne pas afficher pend.png dans la partie status_transition si pend_stopped est actif
            if not pend_stopped and status_transition:
                screen.blit(pend, (pend_x, pend_y))

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