import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Le Pendu")

# Chargement des images
background = pygame.image.load("img/background.png")
sky = pygame.image.load("img/sky.png")
sea = pygame.image.load("img/sea.png")
plateforme = pygame.image.load("img/plateforme.png")
flot = pygame.image.load("img/flot.png")
man = pygame.image.load("img/man.png")
pend = pygame.image.load("img/pend.png")  # Charger pend.png avec transparence

# Redimensionnement des images
sky = pygame.transform.scale(sky, (800, 450))  # sky: 450 x 800
sea = pygame.transform.scale(sea, (800, 150))  # sea: 150 x 800
plateforme = pygame.transform.scale(plateforme, (410, 161))  # plateforme: 161 x 410
flot = pygame.transform.scale(flot, (800, 48))  # flot: 48 x largeur infinie
man = pygame.transform.scale(man, (66, 100))  # man: 100 x 66
pend = pygame.transform.scale(pend, (90, 344))  # Redimensionner pend.png à 90x344

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Police
font = pygame.font.Font(None, 40)  # Police plus petite pour le titre
button_font = pygame.font.Font(None, 30)  # Police plus petite pour les boutons
small_font = pygame.font.Font(None, 32)  # Police plus petite pour les champs de texte

# Fonction pour dessiner les boutons plus esthétiques
def draw_button(text, x, y, width, height, color, hover_color, font, screen):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Vérifier si le curseur est au-dessus du bouton
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height), border_radius=15)  # Bouton arrondi
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius=15)  # Bouton arrondi

    # Rendu du texte du bouton
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surf, text_rect)
    return False

# Fonction pour le menu principal avec un fond plus joli et des boutons esthétiques
def main_menu():
    while True:
        # Utilise l'image sky comme fond
        screen.blit(sky, (0, 0))  # Utiliser 'sky' comme fond

        # Titre centré
        title = font.render("Le Pendu", True, BLACK)
        screen.blit(title, (screen_width / 2 - title.get_width() / 2, 50))

        # Dessiner les boutons avec une taille plus petite et plus esthétique
        if draw_button("Niveau Facile", 300, 200, 180, 45, WHITE, (200, 200, 200), button_font, screen):
            return "facile"
        if draw_button("Niveau Difficile", 300, 300, 180, 45, WHITE, (200, 200, 200), button_font, screen):
            return "difficile"

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

# Fonction pour demander le prénom
def get_name():
    input_box = pygame.Rect(300, 250, 200, 50)  # Position et taille de la boîte de saisie
    color_inactive = pygame.Color('lightskyblue3')  # Couleur de la boîte inactive
    color_active = pygame.Color('dodgerblue2')  # Couleur de la boîte active
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):  # Vérifie si la boîte est cliquée
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:  # Appuyer sur Entrée pour valider
                        done = True
                    elif event.key == pygame.K_BACKSPACE:  # Gestion de la suppression
                        text = text[:-1]
                    else:
                        text += event.unicode  # Ajoute le caractère tapé

        # Fond : sky.png
        screen.blit(sky, (0, 0))

        # Titre "What's your name ?"
        title_surface = small_font.render("What's your name ?", True, BLACK)
        title_rect = title_surface.get_rect(center=(screen_width // 2, 150))  # Centrer le titre
        screen.blit(title_surface, title_rect)

        # Boîte de saisie
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)  # Largeur dynamique de la boîte
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

    return text

# Fonction pour charger un mot aléatoire depuis le fichier mots.txt
def load_random_word():
    with open("txt/mots.txt", "r") as file:
        words = file.readlines()
    return random.choice(words).strip().lower()

# Fonction pour afficher le mot avec la première et la dernière lettre visibles
def display_word(word, guessed_letters):
    displayed_word = ""
    for i, letter in enumerate(word):
        if i == 0 or i == len(word) - 1 or letter in guessed_letters:
            displayed_word += letter + " "
        else:
            displayed_word += "_ "
    return displayed_word.strip()

# Fonction pour la boucle principale du jeu
def game_loop():
    flot_width = screen_width  # Largeur de flot.png (identique à la largeur de l'écran)
    flot_speed = -1  # Vitesse de défilement (négative pour aller vers la gauche)
    flot_x1 = 0  # Position X de la première image flot.png
    flot_x2 = flot_width  # Position X de la deuxième image flot.png

    word = load_random_word()
    guessed_letters = set()
    attempts = 6

    while True:
        # Dessine les éléments de fond
        screen.blit(sky, (0, 0))  # sky: 450 x 800
        screen.blit(sea, (0, 450))  # sea: 150 x 800 (positionné en bas)

        # Dessine les deux copies de flot.png pour l'effet de défilement infini
        screen.blit(flot, (flot_x1, 450 - 48 + 20))  # flot: 48 x largeur infinie (20 pixels plus bas)
        screen.blit(flot, (flot_x2, 450 - 48 + 20))  # Deuxième image

        # Dessine la plateforme et le personnage
        screen.blit(plateforme, (200, 450 - 161))  # plateforme: 161 x 410 (centrée sur sea)
        screen.blit(man, (220, 450 - 161 - 100))  # man: 100 x 66 (sur la plateforme)

        # Affiche pend.png avec les nouvelles coordonnées (x=161, y=-77)
        screen.blit(pend, (150, -77))  # Pend avec les nouvelles dimensions et position

        # Déplace les images
        flot_x1 += flot_speed
        flot_x2 += flot_speed

        # Réinitialise la position des images quand elles sortent de l'écran
        if flot_x1 + flot_width < 0:  # Si la première image sort complètement à gauche
            flot_x1 = flot_width  # Replace-la à droite
        if flot_x2 + flot_width < 0:  # Si la deuxième image sort complètement à gauche
            flot_x2 = flot_width  # Replace-la à droite

        # Affiche le mot à deviner
        displayed_word = display_word(word, guessed_letters)
        word_surface = font.render(displayed_word, True, BLACK)
        screen.blit(word_surface, (screen_width // 2 - word_surface.get_width() // 2, 500))

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    letter = event.unicode.lower()
                    if letter not in guessed_letters:
                        guessed_letters.add(letter)
                        if letter not in word:
                            attempts -= 1

        # Vérifie si le joueur a gagné ou perdu
        if all(letter in guessed_letters for letter in word):
            result_surface = font.render("Félicitations, vous avez gagné !", True, BLACK)
            screen.blit(result_surface, (screen_width // 2 - result_surface.get_width() // 2, 550))
            pygame.display.update()
            pygame.time.wait(3000)
            return
        if attempts == 0:
            result_surface = font.render(f"Perdu ! Le mot était {word}", True, BLACK)
            screen.blit(result_surface, (screen_width // 2 - result_surface.get_width() // 2, 550))
            pygame.display.update()
            pygame.time.wait(3000)
            return

        # Met à jour l'affichage
        pygame.display.update()

# Fonction principale
def main():
    niveau = main_menu()
    if niveau == "facile":
        name = get_name()  # Appelle la fonction pour demander le prénom
        print(f"Bienvenue, {name}!")
        game_loop()  # Lance le jeu après avoir obtenu le prénom

if __name__ == "__main__":
    main()
