# On importe les librairie
import pygame
import sys
import random 

# On initialise Pygame
pygame.init()


# Paramètres de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#taille de la fenêtre
pygame.display.set_caption("Jeu du Pendulé") #titre de la fenêtre

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Police de caractère 
font = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 36)

# Charger les mots à deviner depuis le fichier
def load_words():
    with open('mots.txt', 'r') as file:
        words = file.read().splitlines()
    return words

# Fonction pour choisir un mot aléatoire
def choose_word():
    words = load_words()
    return random.choice(words).upper()

# Fonction pour afficher du texte à l'écran
def draw_text(text, font, color, x, y):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Fonction principale du jeu
def game_loop():
    word = choose_word()  # Choisir un mot aléatoire
    guessed_letters = []  # Lettres déjà devinées
    incorrect_guesses = 0  # Nombre d'erreurs
    max_incorrect_guesses = 7  # Le nombre maximum d'erreurs avant de perdre

    while True:
        screen.fill(WHITE)  # Remplir l'écran avec du blanc

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                letter = pygame.key.name(event.key).upper()
                if letter.isalpha() and len(letter) == 1 and letter not in guessed_letters:
                    guessed_letters.append(letter)
                    if letter not in word:
                        incorrect_guesses += 1

        # Afficher les lettres devinées
        display_word = ''
        for letter in word:
            if letter in guessed_letters:
                display_word += letter + ' '
            else:
                display_word += '_ '

        draw_text("Mot à deviner : " + display_word, font, BLACK, 20, 100)

        # Afficher les lettres incorrectes
        incorrect_letters = [letter for letter in guessed_letters if letter not in word]
        draw_text("Lettres incorrectes : " + ' '.join(incorrect_letters), font_small, RED, 20, 200)

        # Afficher les erreurs et le pendu
        draw_text(f"Erreurs: {incorrect_guesses}/{max_incorrect_guesses}", font_small, BLACK, 20, 300)

        # Afficher le dessin du pendu (simple)
        if incorrect_guesses >= 1:
            pygame.draw.circle(screen, BLACK, (500, 150), 30)  # Tête
        if incorrect_guesses >= 2:
            pygame.draw.line(screen, BLACK, (500, 180), (500, 250), 5)  # Corps
        if incorrect_guesses >= 3:
            pygame.draw.line(screen, BLACK, (500, 200), (470, 230), 5)  # Bras gauche
        if incorrect_guesses >= 4:
            pygame.draw.line(screen, BLACK, (500, 200), (530, 230), 5)  # Bras droit
        if incorrect_guesses >= 5:
            pygame.draw.line(screen, BLACK, (500, 250), (470, 300), 5)  # Jambe gauche
        if incorrect_guesses >= 6:
            pygame.draw.line(screen, BLACK, (500, 250), (530, 300), 5)  # Jambe droite
        if incorrect_guesses >= 7:
            draw_text("GAME OVER!", font, RED, 320, 450)

        # Vérifier si le joueur a gagné
        if all(letter in guessed_letters for letter in word):
            draw_text("Gagné ! Le mot était : " + word, font, BLACK, 200, 450)

        # Mettre à jour l'affichage
        pygame.display.flip()

        # Si le joueur a perdu ou gagné, on attend qu'il ferme la fenêtre
        if incorrect_guesses >= max_incorrect_guesses or all(letter in guessed_letters for letter in word):
            pygame.time.wait(2000)  # Attendre 2 secondes avant de quitter
            break

# Lancer le jeu
game_loop()