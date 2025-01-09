import pygame
import sys
import time
import json

# Charger les traductions
def load_translations():
    with open('translations.json', "r", encoding="utf-8") as file:
        return json.load(file)

# Définir la langue actuelle
translations = load_translations()
current_language = "Français"

# Fonction pour obtenir une traduction
def t(key):
    return translations[current_language].get(key, key)


# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Katarenga")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Polices
font = pygame.font.Font(None, 40)
button_font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 20)

# État global des paramètres
settings = {
    "volume": 0.5,
    "language": "Français",
    "fullscreen": False
}

# Animation de chargement
def loading_screen(message="Chargement..."):
    screen.fill(GRAY)
    text = font.render(message, True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    time.sleep(1)  # Simulation de chargement

# Fonction pour dessiner les boutons
def draw_button(text, x, y, width, height, color, hover_color):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    if button_rect.collidepoint((mouse_x, mouse_y)):
        pygame.draw.rect(screen, hover_color, button_rect)
    else:
        pygame.draw.rect(screen, color, button_rect)

    text_surface = button_font.render(text, True, WHITE)
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

    return button_rect

# Menu Paramètres
def settings_menu():
    global settings, current_language
    running = True
    language_options = list(translations.keys())
    language_index = language_options.index(current_language)

    while running:
        screen.fill(WHITE)

        # Titre
        title_text = font.render(t("settings"), True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Langue
        language_label = button_font.render(t("language") + ":", True, BLACK)
        screen.blit(language_label, (200, 200))
        current_language_text = small_font.render(current_language, True, BLACK)
        screen.blit(current_language_text, (350, 200))
        next_language_button = draw_button(">", 450, 195, 40, 40, BLUE, RED)

        # Bouton Retour
        back_button = draw_button(t("back"), 10, SCREEN_HEIGHT - 60, 100, 40, BLUE, RED)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Changer de langue
                if next_language_button.collidepoint(event.pos):
                    language_index = (language_index + 1) % len(language_options)
                    current_language = language_options[language_index]

                # Retour
                if back_button.collidepoint(event.pos):
                    loading_screen(t("back") + "...")
                    return

        pygame.display.flip()

# Démarrage du jeu
def start_game(player1_name, player2_name, game_name):
    running = True

    while running:
        screen.fill(WHITE)

        # Titre du jeu
        title_text = font.render(f"{game_name}", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Affichage des joueurs
        player_text1 = small_font.render(f"Joueur 1 : {player1_name}", True, BLACK)
        player_text2 = small_font.render(f"Joueur 2 : {player2_name}", True, BLACK)
        screen.blit(player_text1, (SCREEN_WIDTH // 2 - player_text1.get_width() // 2, 200))
        screen.blit(player_text2, (SCREEN_WIDTH // 2 - player_text2.get_width() // 2, 250))

        # Bouton Retour
        back_button = draw_button("Retour", 10, SCREEN_HEIGHT - 60, 100, 40, BLUE, RED)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    loading_screen("Retour...")
                    return

        pygame.display.flip()

# Saisie des noms des joueurs
def player_names(game_name):
    running = True
    player1_name = ""
    player2_name = ""
    input_active1 = True
    input_active2 = False

    while running:
        screen.fill(WHITE)

        # Titre
        title_text = font.render(f"{game_name}", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Instructions
        instruction_text = small_font.render("Entrez les noms des joueurs sans espaces ni caractères spéciaux.", True, BLACK)
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 100))

        # Zones de texte pour les noms
        input_rect1 = pygame.Rect(250, 200, 300, 50)
        input_rect2 = pygame.Rect(250, 300, 300, 50)
        pygame.draw.rect(screen, GREEN if input_active1 else GRAY, input_rect1, 2)
        pygame.draw.rect(screen, GREEN if input_active2 else GRAY, input_rect2, 2)

        # Texte des zones de saisie
        player1_display = font.render(player1_name if player1_name else "Joueur 1", True, BLACK)
        player2_display = font.render(player2_name if player2_name else "Joueur 2", True, BLACK)
        screen.blit(player1_display, (input_rect1.x + 10, input_rect1.y + 10))
        screen.blit(player2_display, (input_rect2.x + 10, input_rect2.y + 10))

        # Bouton Retour
        back_button = draw_button("Retour", 10, SCREEN_HEIGHT - 60, 100, 40, BLUE, RED)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Activer ou désactiver les zones de saisie
                if input_rect1.collidepoint((mouse_x, mouse_y)):
                    input_active1 = True
                    input_active2 = False
                elif input_rect2.collidepoint((mouse_x, mouse_y)):
                    input_active1 = False
                    input_active2 = True

                # Retour
                if back_button.collidepoint(event.pos):
                    loading_screen("Retour...")
                    return

            if event.type == pygame.KEYDOWN:
                if input_active1:
                    if event.key == pygame.K_BACKSPACE:
                        player1_name = player1_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        input_active1 = False
                        input_active2 = True
                    elif event.unicode.isalnum():  # Empêche les espaces et caractères spéciaux
                        player1_name += event.unicode
                elif input_active2:
                    if event.key == pygame.K_BACKSPACE:
                        player2_name = player2_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        # Validation des noms
                        if not player1_name:
                            player1_name = "Joueur 1"
                        if not player2_name:
                            player2_name = "Joueur 2"
                        
                        # Ajouter des suffixes si les noms sont identiques
                        if player1_name == player2_name:
                            player1_name += "(1)"
                            player2_name += "(2)"
                        
                        # Afficher les noms dans la console
                        print(f"Jeu sélectionné : {game_name}")
                        print(f"Joueur 1 : {player1_name}")
                        print(f"Joueur 2 : {player2_name}")
                        return
                    elif event.unicode.isalnum():  # Empêche les espaces et caractères spéciaux
                        player2_name += event.unicode

        pygame.display.flip()

def main_menu():
    running = True
    while running:
        screen.fill(BLUE)

        # Titre
        title_text = font.render(t("title"), True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Boutons
        start_button = draw_button(t("play_game"), 300, 200, 200, 50, GREEN, RED)
        settings_button = draw_button(t("settings"), 300, 300, 200, 50, GREEN, RED)
        quit_button = draw_button(t("quit"), 300, 400, 200, 50, GREEN, RED)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_selection()
                if settings_button.collidepoint(event.pos):
                    settings_menu()
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

# Sélection de jeu
def game_selection():
    running = True
    while running:
        screen.fill(GRAY)

        # Titre
        title_text = font.render("Choisissez un jeu", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Boutons de jeu
        katarenga_button = draw_button("Katarenga", 150, 200, 200, 100, GREEN, RED)
        congress_button = draw_button("Congress", 400, 200, 200, 100, GREEN, RED)
        isolation_button = draw_button("Isolation", 275, 350, 200, 100, GREEN, RED)

        # Bouton Retour
        back_button = draw_button("Retour", 10, SCREEN_HEIGHT - 60, 100, 40, BLUE, RED)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    loading_screen("Retour...")
                    return
                if katarenga_button.collidepoint(event.pos):
                    loading_screen("Chargement...")
                    player_names("Katarenga")
                if congress_button.collidepoint(event.pos):
                    loading_screen("Chargement...")
                    player_names("Congress")
                if isolation_button.collidepoint(event.pos):
                    loading_screen("Chargement...")
                    player_names("Isolation")

        pygame.display.flip()

# Lancer le programme
if __name__ == "__main__":
    main_menu()
