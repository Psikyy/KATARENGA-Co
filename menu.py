# menu.py
import pygame
import sys
import time
import json
import os
from Katarenga import genererQuart, Init_Board

# Charger les traductions
def load_translations():
    try:
        with open('translations.json', "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Fichier de traductions non trouvé.")
        return {"Français": {}}

# Sauvegarder les paramètres
def save_settings():
    with open('settings.json', 'w', encoding='utf-8') as file:
        json.dump(settings, file)

# Charger les paramètres
def load_settings():
    try:
        with open('settings.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"volume": 0.5, "language": "Français", "fullscreen": False}

# Définir la langue actuelle
translations = load_translations()
settings = load_settings()
current_language = settings["language"]

# Fonction pour obtenir une traduction
def t(key):
    return translations[current_language].get(key, key)

# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 100  # Taille d'une case en pixels
BOARD_SIZE = 8
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Katarenga")

def draw_board(screen, selected_quadrants):
    """
    Dessine le plateau avec les quadrants configurés et des bordures pour les délimiter.
    """

    for (x, y), config in selected_quadrants.items():
        quadrant = config["quadrant"]
        for i in range(4):
            for j in range(4):
                color = quadrant[i][j]
                # Dessiner la case
                pygame.draw.rect(screen, color, (
                    x * CELL_SIZE * 4 + j * CELL_SIZE,
                    y * CELL_SIZE * 4 + i * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                ))
        
        # Dessiner une bordure autour du quadrant
        pygame.draw.rect(screen, BLACK, (
            x * CELL_SIZE * 4,
            y * CELL_SIZE * 4,
            CELL_SIZE * 4, CELL_SIZE * 4
        ), 3)  # 3 est l'épaisseur de la bordure

def configure_board():
    """
    Permet à l'utilisateur de configurer le plateau en choisissant les quadrants et leur orientation.
    """
    running = True
    quadrants = [genererQuart() for _ in range(4)]  # Génère 4 quadrants aléatoires
    selected_quadrants = {
        (0, 0): {"quadrant": quadrants[0], "initial_quadrant": [row[:] for row in quadrants[0]], "rotation": 0, "side": "recto", "selected": False},
        (1, 0): {"quadrant": quadrants[1], "initial_quadrant": [row[:] for row in quadrants[1]], "rotation": 0, "side": "recto", "selected": False},
        (0, 1): {"quadrant": quadrants[2], "initial_quadrant": [row[:] for row in quadrants[2]], "rotation": 0, "side": "recto", "selected": False},
        (1, 1): {"quadrant": quadrants[3], "initial_quadrant": [row[:] for row in quadrants[3]], "rotation": 0, "side": "recto", "selected": False}
    }

    # Créer une instance de Init_Board
    init_board = Init_Board(quadrants[0], quadrants[1], quadrants[2], quadrants[3])

    # Variables pour stocker la position du quadrant sélectionné et l'échange
    selected_quadrant_pos = None
    swap_quadrant_pos = None

    while running:
        screen.fill(WHITE)

        # Titre
        title_text = font.render("Configuration du plateau", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Dessiner le plateau
        if selected_quadrant_pos is None:
            # Afficher tous les quadrants
            draw_board(screen, selected_quadrants)
        else:
            # Afficher uniquement le quadrant sélectionné au centre
            x, y = selected_quadrant_pos
            config = selected_quadrants[(x, y)]
            draw_quadrant_center(screen, config["quadrant"])

        # Dessiner les zones cliquables pour déboguer
        for (x, y), config in selected_quadrants.items():
            button_rect = pygame.Rect(50 + x * 200, 400 + y * 60, 150, 50)
            pygame.draw.rect(screen, RED, button_rect, 2)  # Dessine la zone cliquable en rouge

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Vérifier les clics sur les boutons des quadrants
                for (x, y), config in selected_quadrants.items():
                    button_rect = pygame.Rect(50 + x * 200, 400 + y * 60, 150, 50)
                    if button_rect.collidepoint((mouse_x, mouse_y)):
                        if selected_quadrant_pos is None:
                            # Sélectionner ce quadrant pour le modifier
                            selected_quadrant_pos = (x, y)
                        else:
                            # Échanger les positions des quadrants
                            if swap_quadrant_pos is None:
                                swap_quadrant_pos = (x, y)
                            else:
                                # Échanger les quadrants
                                selected_quadrants[selected_quadrant_pos], selected_quadrants[swap_quadrant_pos] = selected_quadrants[swap_quadrant_pos], selected_quadrants[selected_quadrant_pos]
                                selected_quadrant_pos = None
                                swap_quadrant_pos = None

            if event.type == pygame.KEYDOWN:
                if selected_quadrant_pos is not None:
                    x, y = selected_quadrant_pos
                    config = selected_quadrants[(x, y)]

                    # Faire tourner le quadrant sélectionné avec les flèches
                    if event.key == pygame.K_LEFT:  # Flèche gauche
                        config["rotation"] = (config["rotation"] - 90) % 360  # Rotation à gauche
                    elif event.key == pygame.K_RIGHT:  # Flèche droite
                        config["rotation"] = (config["rotation"] + 90) % 360  # Rotation à droite
                    
                    # Si la rotation est à 0°, restaurer le quadrant initial
                    if config["rotation"] == 0:
                        config["quadrant"] = [row[:] for row in config["initial_quadrant"]]
                    else:
                        # Appliquer la rotation au quadrant
                        config["quadrant"] = init_board.rotate_quadrant(config["quadrant"], config["rotation"] // 90)
                    
                    print(f"Quadrant Q{x*2 + y + 1} tourné à {config['rotation']}°")

                # Valider la configuration
                if event.key == pygame.K_RETURN:
                    if selected_quadrant_pos is not None:
                        # Revenir à la vue d'ensemble
                        selected_quadrant_pos = None
                    else:
                        print("Configuration confirmée :", selected_quadrants)
                        loading_screen("Démarrage du jeu...")
                        return selected_quadrants

        pygame.display.flip()

def draw_quadrant_center(screen, quadrant):
    """
    Dessine un quadrant au centre de l'écran.
    """
    for i in range(4):
        for j in range(4):
            color = quadrant[i][j]
            pygame.draw.rect(screen, color, (
                SCREEN_WIDTH // 2 - 2 * CELL_SIZE + j * CELL_SIZE,
                SCREEN_HEIGHT // 2 - 2 * CELL_SIZE + i * CELL_SIZE,
                CELL_SIZE, CELL_SIZE
            ))

def animate_rotation(quadrant, current_rotation, target_rotation):
    """
    Anime la rotation d'un quadrant de current_rotation à target_rotation.
    """
    step = 9  # Rotation de 9° par étape
    if current_rotation < target_rotation:
        current_rotation += step
    elif current_rotation > target_rotation:
        current_rotation -= step
    return current_rotation % 360

# Charger et redimensionner l'image de fond
try:
    background_image = pygame.image.load("./img/Image_du_jeu.png")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error:
    print("Image de fond non trouvée.")
    background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image.fill((0, 0, 0))

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (52, 152, 219)
HOVER_BLUE = (41, 128, 185)
GREEN = (46, 204, 113)
HOVER_GREEN = (39, 174, 96)
RED = (231, 76, 60)
HOVER_RED = (192, 57, 43)
GRAY = (200, 200, 200)

# Polices
font = pygame.font.Font(None, 80)  # Grande police pour le titre
button_font = pygame.font.Font(None, 40)  # Police pour les boutons
small_font = pygame.font.Font(None, 30)  # Police plus petite pour les textes secondaires

# Charger les sons
try:
    click_sound = pygame.mixer.Sound("musique/click.wav")  # Son de clic
    hover_sound = pygame.mixer.Sound("musique/hover.wav")  # Son de survol
except pygame.error:
    print("Sons non trouvés. Les effets sonores seront désactivés.")
    click_sound = None
    hover_sound = None

# Charger la musique de fond
try:
    pygame.mixer.music.load("musique/adventure.mp3")
    pygame.mixer.music.set_volume(settings["volume"])
    pygame.mixer.music.play(-1)  # Boucle infinie
except pygame.error:
    print("Musique de fond non trouvée.")

# Animation d'intro
def intro_animation():
    screen.fill(BLACK)
    logo_font = pygame.font.Font(None, 100)
    text_surface = logo_font.render("Smart Games", True, WHITE)

    alpha = 0
    fade_in_speed = 5
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(BLACK)

        if alpha < 255:
            alpha += fade_in_speed
        else:
            time.sleep(1)
            running = False

        text_surface.set_alpha(alpha)
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - text_surface.get_height() // 2))

        pygame.display.flip()
        clock.tick(30)

    time.sleep(1)  # Pause avant le menu

# Animation de chargement
def loading_screen(message="Chargement..."):
    screen.fill(GRAY)
    text = font.render(message, True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    time.sleep(1)

# Fonction pour dessiner les boutons avec des effets de survol
def draw_button(text, x, y, width, height, color, hover_color, text_color=WHITE):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    if button_rect.collidepoint((mouse_x, mouse_y)):
        pygame.draw.rect(screen, hover_color, button_rect, border_radius=15)
        pygame.draw.rect(screen, WHITE, button_rect, width=3, border_radius=15)  # Bordure blanche
        if hover_sound:
            if not hasattr(draw_button, 'last_hovered') or draw_button.last_hovered != button_rect:
                hover_sound.play()
                draw_button.last_hovered = button_rect
    else:
        pygame.draw.rect(screen, color, button_rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, button_rect, width=3, border_radius=15)  # Bordure noire

    # Texte centré
    text_surface = button_font.render(text, True, text_color)
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
                    settings["language"] = current_language
                    save_settings()

                # Retour
                if back_button.collidepoint(event.pos):
                    loading_screen(t("back") + "...")
                    return

        pygame.display.flip()

# Démarrage du jeu
def start_game(player1_name, player2_name, game_name, selected_quadrants=None):
    """
    Démarre le jeu avec les noms des joueurs et la configuration du plateau (si applicable).
    """
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

        # Dessiner le plateau si c'est Katarenga
        if game_name == "Katarenga" and selected_quadrants:
            draw_board(screen, selected_quadrants)

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

                        # Démarrer le jeu après la validation des noms
                        if game_name == "Katarenga":
                            selected_quadrants = configure_board()  # Appelle la configuration du plateau
                            start_game(player1_name, player2_name, game_name, selected_quadrants)
                        else:
                            start_game(player1_name, player2_name, game_name)
                        return
                    elif event.unicode.isalnum():  # Empêche les espaces et caractères spéciaux
                        player2_name += event.unicode

        pygame.display.flip()

def main_menu():
    running = True
    title_alpha = 255  # Opacité du titre
    fade_out = True  # Direction de l'animation du titre

    while running:
        screen.blit(background_image, (0, 0))  # Affiche l'image de fond

        # Animation du titre
        if fade_out:
            title_alpha -= 3
            if title_alpha <= 100:
                fade_out = False
        else:
            title_alpha += 3
            if title_alpha >= 255:
                fade_out = True

        # Titre
        title_surface = font.render("Katarenga", True, WHITE)
        title_surface.set_alpha(title_alpha)  # Appliquer la transparence
        screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 50))

        # Boutons
        start_button = draw_button("Lancer le jeu", SCREEN_WIDTH // 2 - 150, 250, 300, 60, GREEN, HOVER_GREEN)
        settings_button = draw_button("Paramètres", SCREEN_WIDTH // 2 - 150, 350, 300, 60, BLUE, HOVER_BLUE)
        quit_button = draw_button("Quitter", SCREEN_WIDTH // 2 - 150, 450, 300, 60, RED, HOVER_RED)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    game_selection()  # Sélection du jeu
                if settings_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    settings_menu()  # Menu des paramètres
                if quit_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
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
                    if click_sound:
                        click_sound.play()
                    loading_screen("Retour...")
                    return
                if katarenga_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    loading_screen("Chargement...")
                    player_names("Katarenga")
                if congress_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    loading_screen("Chargement...")
                    player_names("Congress")
                if isolation_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    loading_screen("Chargement...")
                    player_names("Isolation")

        pygame.display.flip()

# Lancer le programme
if __name__ == "__main__":
    intro_animation()
    main_menu()