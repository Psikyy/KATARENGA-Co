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
    # Ajuster la position pour centrer le plateau et éviter les coupures
    cell_size = min(CELL_SIZE, 50)  # Réduire la taille des cellules si nécessaire
    board_width = 8 * cell_size
    board_height = 8 * cell_size
    
    offset_x = (SCREEN_WIDTH - board_width) // 2
    offset_y = 100  # Laisser de l'espace pour le titre, mais pas trop bas
    
    # Assurer que le plateau entier est visible
    if offset_y + board_height > SCREEN_HEIGHT - 120:  # Laisser de l'espace pour les boutons
        offset_y = max(80, SCREEN_HEIGHT - board_height - 120)
    
    for (x, y), config in selected_quadrants.items():
        quadrant = config["quadrant"]
        for i in range(4):
            for j in range(4):
                color = quadrant[i][j]
                # Dessiner la case avec le décalage approprié et la taille ajustée
                pygame.draw.rect(screen, color, (
                    offset_x + x * cell_size * 4 + j * cell_size,
                    offset_y + y * cell_size * 4 + i * cell_size,
                    cell_size, cell_size
                ))
        
        # Dessiner une bordure autour du quadrant avec la taille ajustée
        pygame.draw.rect(screen, BLACK, (
            offset_x + x * cell_size * 4,
            offset_y + y * cell_size * 4,
            cell_size * 4, cell_size * 4
        ), 2)  # Réduire l'épaisseur de la bordure pour plus de clarté
        
        # Afficher un indicateur de quadrant pour l'identification
        indicator_text = small_font.render(f"Q{x*2 + y*2 + 1}", True, BLACK)
        indicator_bg = pygame.Surface((indicator_text.get_width() + 10, indicator_text.get_height() + 10))
        indicator_bg.fill(WHITE)
        indicator_bg.set_alpha(200)  # Semi-transparent
        screen.blit(indicator_bg, (
            offset_x + x * cell_size * 4 + 5,
            offset_y + y * cell_size * 4 + 5
        ))
        screen.blit(indicator_text, (
            offset_x + x * cell_size * 4 + 10,
            offset_y + y * cell_size * 4 + 10
        ))
    
    # Retourner les informations sur la position et la taille du plateau
    return {
        "offset_x": offset_x,
        "offset_y": offset_y,
        "cell_size": cell_size
    }

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
    
    # Ajuster la taille des cellules pour l'affichage
    cell_size_display = min(50, CELL_SIZE)  # Utiliser une taille plus petite pour l'affichage général

    instructions_shown = True
    instructions_timer = 5000  # Afficher les instructions pendant 5 secondes

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    while running:
        screen.fill(WHITE)
        current_time = pygame.time.get_ticks()

        # Titre
        title_text = font.render("Configuration du plateau", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 20))

        # Dessiner le plateau
        if selected_quadrant_pos is None:
            # Afficher tous les quadrants en mode vue d'ensemble
            draw_board(screen, selected_quadrants)
            
            # Dessiner des boutons pour chaque quadrant
            button_width = 150
            button_height = 40
            button_spacing = 20
            total_width = 2 * button_width + button_spacing
            start_x = (SCREEN_WIDTH - total_width) // 2
            
            # Première rangée de boutons
            for x in range(2):
                button_rect = pygame.Rect(
                    start_x + x * (button_width + button_spacing), 
                    SCREEN_HEIGHT - 100, 
                    button_width, 
                    button_height
                )
                color = GREEN if selected_quadrants[(x, 0)]["selected"] else BLUE
                hover_color = HOVER_GREEN if selected_quadrants[(x, 0)]["selected"] else HOVER_BLUE
                pygame.draw.rect(screen, color, button_rect, border_radius=5)
                
                # Texte du bouton
                button_text = button_font.render(f"Quadrant {x*2 + 1}", True, WHITE)
                screen.blit(button_text, (
                    button_rect.x + (button_rect.width - button_text.get_width()) // 2,
                    button_rect.y + (button_rect.height - button_text.get_height()) // 2
                ))
                
            # Deuxième rangée de boutons
            for x in range(2):
                button_rect = pygame.Rect(
                    start_x + x * (button_width + button_spacing), 
                    SCREEN_HEIGHT - 50, 
                    button_width, 
                    button_height
                )
                color = GREEN if selected_quadrants[(x, 1)]["selected"] else BLUE
                hover_color = HOVER_GREEN if selected_quadrants[(x, 1)]["selected"] else HOVER_BLUE
                pygame.draw.rect(screen, color, button_rect, border_radius=5)
                
                # Texte du bouton
                button_text = button_font.render(f"Quadrant {x*2 + 2}", True, WHITE)
                screen.blit(button_text, (
                    button_rect.x + (button_rect.width - button_text.get_width()) // 2,
                    button_rect.y + (button_rect.height - button_text.get_height()) // 2
                ))
                
            # Bouton pour confirmer la configuration
            confirm_button = pygame.Rect(
                SCREEN_WIDTH - 150, 
                SCREEN_HEIGHT - 60, 
                120, 
                40
            )
            pygame.draw.rect(screen, GREEN, confirm_button, border_radius=5)
            confirm_text = button_font.render("Confirmer", True, WHITE)
            screen.blit(confirm_text, (
                confirm_button.x + (confirm_button.width - confirm_text.get_width()) // 2,
                confirm_button.y + (confirm_button.height - confirm_text.get_height()) // 2
            ))
            
        else:
            # Afficher le quadrant sélectionné au centre pour modification
            x, y = selected_quadrant_pos
            config = selected_quadrants[(x, y)]
            
            # Dessiner un fond gris clair pour la zone de travail
            work_area = pygame.Rect(
                SCREEN_WIDTH // 2 - 2 * CELL_SIZE - 20,
                SCREEN_HEIGHT // 2 - 2 * CELL_SIZE - 20,
                4 * CELL_SIZE + 40,
                4 * CELL_SIZE + 40
            )
            pygame.draw.rect(screen, GRAY, work_area, border_radius=10)
            
            # Dessiner le quadrant sélectionné
            for i in range(4):
                for j in range(4):
                    color = config["quadrant"][i][j]
                    pygame.draw.rect(screen, color, (
                        SCREEN_WIDTH // 2 - 2 * CELL_SIZE + j * CELL_SIZE,
                        SCREEN_HEIGHT // 2 - 2 * CELL_SIZE + i * CELL_SIZE,
                        CELL_SIZE, CELL_SIZE
                    ))
            
            # Dessiner une bordure autour du quadrant
            pygame.draw.rect(screen, BLACK, (
                SCREEN_WIDTH // 2 - 2 * CELL_SIZE,
                SCREEN_HEIGHT // 2 - 2 * CELL_SIZE,
                CELL_SIZE * 4, CELL_SIZE * 4
            ), 3)
            
            # Boutons de rotation
            rotate_left_button = pygame.Rect(
                SCREEN_WIDTH // 2 - 2 * CELL_SIZE - 60,
                SCREEN_HEIGHT // 2 - 30,
                50,
                60
            )
            rotate_right_button = pygame.Rect(
                SCREEN_WIDTH // 2 + 2 * CELL_SIZE + 10,
                SCREEN_HEIGHT // 2 - 30,
                50,
                60
            )
            
            pygame.draw.rect(screen, BLUE, rotate_left_button, border_radius=5)
            pygame.draw.rect(screen, BLUE, rotate_right_button, border_radius=5)
            
            left_text = font.render("←", True, WHITE)
            right_text = font.render("→", True, WHITE)
            
            screen.blit(left_text, (
                rotate_left_button.x + (rotate_left_button.width - left_text.get_width()) // 2,
                rotate_left_button.y + (rotate_left_button.height - left_text.get_height()) // 2
            ))
            screen.blit(right_text, (
                rotate_right_button.x + (rotate_right_button.width - right_text.get_width()) // 2,
                rotate_right_button.y + (rotate_right_button.height - right_text.get_height()) // 2
            ))
            
            # Bouton Retour
            back_button = pygame.Rect(
                10,
                SCREEN_HEIGHT - 60,
                100,
                40
            )
            pygame.draw.rect(screen, RED, back_button, border_radius=5)
            back_text = button_font.render("Retour", True, WHITE)
            screen.blit(back_text, (
                back_button.x + (back_button.width - back_text.get_width()) // 2,
                back_button.y + (back_button.height - back_text.get_height()) // 2
            ))
            
            # Afficher l'angle de rotation actuel
            rotation_text = button_font.render(f"Rotation: {config['rotation']}°", True, BLACK)
            screen.blit(rotation_text, (
                SCREEN_WIDTH // 2 - rotation_text.get_width() // 2,
                SCREEN_HEIGHT // 2 + 2 * CELL_SIZE + 20
            ))

        # Afficher les instructions pendant un certain temps
        if instructions_shown and current_time - start_time < instructions_timer:
            instruction_bg = pygame.Surface((SCREEN_WIDTH - 100, 100))
            instruction_bg.fill(WHITE)
            instruction_bg.set_alpha(220)
            screen.blit(instruction_bg, (50, SCREEN_HEIGHT // 2 - 70))
            
            instructions = [
                "- Cliquez sur un quadrant pour le sélectionner et le modifier",
                "- Utilisez les flèches ou les boutons pour faire pivoter un quadrant",
                "- Pour échanger deux quadrants, sélectionnez-les l'un après l'autre",
                "- Appuyez sur ENTRÉE pour confirmer la configuration"
            ]
            
            for i, line in enumerate(instructions):
                instr_text = small_font.render(line, True, BLACK)
                screen.blit(instr_text, (60, SCREEN_HEIGHT // 2 - 60 + i * 25))
        elif instructions_shown:
            instructions_shown = False

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                
                if selected_quadrant_pos is None:
                    # En mode vue d'ensemble
                    
                    # Vérifier les clics sur les boutons de quadrant
                    button_width = 150
                    button_height = 40
                    button_spacing = 20
                    total_width = 2 * button_width + button_spacing
                    start_x = (SCREEN_WIDTH - total_width) // 2
                    
                    # Première rangée de boutons
                    for x in range(2):
                        button_rect = pygame.Rect(
                            start_x + x * (button_width + button_spacing), 
                            SCREEN_HEIGHT - 100, 
                            button_width, 
                            button_height
                        )
                        if button_rect.collidepoint((mouse_x, mouse_y)):
                            if click_sound:
                                click_sound.play()
                            if swap_quadrant_pos is None:
                                # Premier quadrant sélectionné pour échange
                                selected_quadrants[(x, 0)]["selected"] = True
                                swap_quadrant_pos = (x, 0)
                            else:
                                # Deuxième quadrant sélectionné, effectuer l'échange
                                x1, y1 = swap_quadrant_pos
                                selected_quadrants[(x1, y1)]["selected"] = False
                                # Échanger les quadrants
                                selected_quadrants[(x, 0)], selected_quadrants[swap_quadrant_pos] = selected_quadrants[swap_quadrant_pos], selected_quadrants[(x, 0)]
                                swap_quadrant_pos = None
                            
                    # Deuxième rangée de boutons
                    for x in range(2):
                        button_rect = pygame.Rect(
                            start_x + x * (button_width + button_spacing), 
                            SCREEN_HEIGHT - 50, 
                            button_width,button_height
                        )
                        if button_rect.collidepoint((mouse_x, mouse_y)):
                            if click_sound:
                                click_sound.play()
                            if swap_quadrant_pos is None:
                                # Premier quadrant sélectionné pour échange
                                selected_quadrants[(x, 1)]["selected"] = True
                                swap_quadrant_pos = (x, 1)
                            else:
                                # Deuxième quadrant sélectionné, effectuer l'échange
                                x1, y1 = swap_quadrant_pos
                                selected_quadrants[(x1, y1)]["selected"] = False
                                # Échanger les quadrants
                                selected_quadrants[(x, 1)], selected_quadrants[swap_quadrant_pos] = selected_quadrants[swap_quadrant_pos], selected_quadrants[(x, 1)]
                                swap_quadrant_pos = None
                    
                    # Vérifier les clics sur le plateau pour sélectionner directement un quadrant pour édition
                    offset_x = (SCREEN_WIDTH - BOARD_SIZE * CELL_SIZE) // 2
                    offset_y = 100
                    
                    for (qx, qy), config in selected_quadrants.items():
                        quadrant_rect = pygame.Rect(
                            offset_x + qx * CELL_SIZE * 4,
                            offset_y + qy * CELL_SIZE * 4,
                            CELL_SIZE * 4, CELL_SIZE * 4
                        )
                        if quadrant_rect.collidepoint((mouse_x, mouse_y)):
                            if click_sound:
                                click_sound.play()
                            selected_quadrant_pos = (qx, qy)
                            break
                    
                    # Vérifier le clic sur le bouton de confirmation
                    confirm_button = pygame.Rect(
                        SCREEN_WIDTH - 150, 
                        SCREEN_HEIGHT - 60, 
                        120, 
                        40
                    )
                    if confirm_button.collidepoint((mouse_x, mouse_y)):
                        if click_sound:
                            click_sound.play()
                        print("Configuration confirmée :", selected_quadrants)
                        loading_screen("Démarrage du jeu...")
                        return selected_quadrants
                
                else:
                    # En mode édition d'un quadrant
                    x, y = selected_quadrant_pos
                    config = selected_quadrants[(x, y)]
                    
                    # Vérifier les clics sur les boutons de rotation
                    rotate_left_button = pygame.Rect(
                        SCREEN_WIDTH // 2 - 2 * CELL_SIZE - 60,
                        SCREEN_HEIGHT // 2 - 30,
                        50,
                        60
                    )
                    rotate_right_button = pygame.Rect(
                        SCREEN_WIDTH // 2 + 2 * CELL_SIZE + 10,
                        SCREEN_HEIGHT // 2 - 30,
                        50,
                        60
                    )
                    
                    if rotate_left_button.collidepoint((mouse_x, mouse_y)):
                        if click_sound:
                            click_sound.play()
                        config["rotation"] = (config["rotation"] - 90) % 360
                        config["quadrant"] = init_board.rotate_quadrant(config["initial_quadrant"], config["rotation"] // 90)
                        print(f"Quadrant Q{x*2 + y*2 + 1} tourné à {config['rotation']}°")
                    
                    elif rotate_right_button.collidepoint((mouse_x, mouse_y)):
                        if click_sound:
                            click_sound.play()
                        config["rotation"] = (config["rotation"] + 90) % 360
                        config["quadrant"] = init_board.rotate_quadrant(config["initial_quadrant"], config["rotation"] // 90)
                        print(f"Quadrant Q{x*2 + y*2 + 1} tourné à {config['rotation']}°")
                    
                    # Vérifier le clic sur le bouton retour
                    back_button = pygame.Rect(
                        10,
                        SCREEN_HEIGHT - 60,
                        100,
                        40
                    )
                    if back_button.collidepoint((mouse_x, mouse_y)):
                        if click_sound:
                            click_sound.play()
                        selected_quadrant_pos = None
            
            if event.type == pygame.KEYDOWN:
                if selected_quadrant_pos is not None:
                    x, y = selected_quadrant_pos
                    config = selected_quadrants[(x, y)]

                    # Faire tourner le quadrant sélectionné avec les flèches
                    if event.key == pygame.K_LEFT:  # Flèche gauche
                        config["rotation"] = (config["rotation"] - 90) % 360  # Rotation à gauche
                        config["quadrant"] = init_board.rotate_quadrant(config["initial_quadrant"], config["rotation"] // 90)
                        print(f"Quadrant Q{x*2 + y*2 + 1} tourné à {config['rotation']}°")
                    elif event.key == pygame.K_RIGHT:  # Flèche droite
                        config["rotation"] = (config["rotation"] + 90) % 360  # Rotation à droite
                        config["quadrant"] = init_board.rotate_quadrant(config["initial_quadrant"], config["rotation"] // 90)
                        print(f"Quadrant Q{x*2 + y*2 + 1} tourné à {config['rotation']}°")
                    elif event.key == pygame.K_ESCAPE:  # Echap pour retourner à la vue d'ensemble
                        selected_quadrant_pos = None
                
                # Valider la configuration avec Entrée
                if event.key == pygame.K_RETURN:
                    if selected_quadrant_pos is not None:
                        # Revenir à la vue d'ensemble
                        selected_quadrant_pos = None
                    else:
                        print("Configuration confirmée :", selected_quadrants)
                        loading_screen("Démarrage du jeu...")
                        return selected_quadrants

        pygame.display.flip()
        clock.tick(30)

def draw_quadrant_center(screen, quadrant):
    """
    Dessine un quadrant au centre de l'écran avec une taille appropriée.
    """
    for i in range(4):
        for j in range(4):
            color = quadrant[i][j]
            pygame.draw.rect(screen, color, (
                SCREEN_WIDTH // 2 - 2 * CELL_SIZE + j * CELL_SIZE,
                SCREEN_HEIGHT // 2 - 2 * CELL_SIZE + i * CELL_SIZE,
                CELL_SIZE, CELL_SIZE
            ))
    
    # Dessiner une bordure autour du quadrant
    pygame.draw.rect(screen, BLACK, (
        SCREEN_WIDTH // 2 - 2 * CELL_SIZE,
        SCREEN_HEIGHT // 2 - 2 * CELL_SIZE,
        CELL_SIZE * 4, CELL_SIZE * 4
    ), 3)  # 3 est l'épaisseur de la bordure

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
        screen.blit(player_text1, (50, 120))
        screen.blit(player_text2, (50, 150))

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