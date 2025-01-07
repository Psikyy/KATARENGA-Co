import pygame
import sys
import time

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
    global settings
    running = True
    volume_rect = pygame.Rect(300, 150, 200, 10)
    language_options = ["Français", "English", "Español"]
    language_index = language_options.index(settings["language"])

    while running:
        screen.fill(WHITE)

        # Titre
        title_text = font.render("Paramètres", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Curseur Volume
        volume_label = button_font.render("Volume :", True, BLACK)
        screen.blit(volume_label, (200, 140))
        pygame.draw.rect(screen, DARK_GRAY, volume_rect)
        pygame.draw.rect(screen, GREEN, pygame.Rect(volume_rect.x, volume_rect.y, int(settings["volume"] * volume_rect.width), volume_rect.height))

        # Texte Volume
        volume_text = small_font.render(f"{int(settings['volume'] * 100)}%", True, BLACK)
        screen.blit(volume_text, (volume_rect.x + volume_rect.width + 10, volume_rect.y - 5))

        # Langue
        language_label = button_font.render("Langue :", True, BLACK)
        screen.blit(language_label, (200, 200))
        current_language = small_font.render(settings["language"], True, BLACK)
        screen.blit(current_language, (350, 200))
        next_language_button = draw_button(">", 450, 195, 40, 40, BLUE, RED)

        # Plein écran
        fullscreen_label = button_font.render("Plein écran :", True, BLACK)
        screen.blit(fullscreen_label, (200, 270))
        fullscreen_button = draw_button("Activer" if not settings["fullscreen"] else "Désactiver", 350, 260, 150, 40, BLUE, RED)

        # Bouton Retour
        back_button = draw_button("Retour", 10, SCREEN_HEIGHT - 60, 100, 40, BLUE, RED)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Ajuster le volume
                if volume_rect.collidepoint((mouse_x, mouse_y)):
                    settings["volume"] = (mouse_x - volume_rect.x) / volume_rect.width

                # Changer de langue
                if next_language_button.collidepoint(event.pos):
                    language_index = (language_index + 1) % len(language_options)
                    settings["language"] = language_options[language_index]

                # Basculer en mode plein écran
                if fullscreen_button.collidepoint(event.pos):
                    settings["fullscreen"] = not settings["fullscreen"]
                    if settings["fullscreen"]:
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    else:
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

                # Retour
                if back_button.collidepoint(event.pos):
                    loading_screen("Retour...")
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
                        # Les deux noms sont saisis, on peut afficher dans la console
                        if not player1_name:
                            player1_name = "Joueur 1"
                        if not player2_name:
                            player2_name = "Joueur 2"
                        print(f"Jeu sélectionné : {game_name}")
                        print(f"Joueur 1 : {player1_name}")
                        print(f"Joueur 2 : {player2_name}")
                        return
                    elif event.unicode.isalnum():  # Empêche les espaces et caractères spéciaux
                        player2_name += event.unicode

        pygame.display.flip()

# Menu principal
def main_menu():
    running = True
    while running:
        screen.fill(BLUE)

        # Titre
        title_text = font.render("Katarenga", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Boutons
        start_button = draw_button("Lancer le jeu", 300, 200, 200, 50, GREEN, RED)
        settings_button = draw_button("Paramètres", 300, 300, 200, 50, GREEN, RED)
        quit_button = draw_button("Quitter", 300, 400, 200, 50, GREEN, RED)

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
