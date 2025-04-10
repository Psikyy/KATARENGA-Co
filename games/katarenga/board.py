import pygame
import random
import sys
import os
from ui.colors import WHITE, BLACK, BLUE, RED, GREEN, HOVER_GREEN
from ui.buttons import draw_button, click_sound

# Définition des types de cases et leurs couleurs
# TILE_TYPES = {
#     'A': (220, 220, 220),  # Gris clair - Déplacement orthogonal
#     'B': (160, 82, 45),    # Marron - Déplacement diagonal
#     'C': (0, 128, 0),      # Vert - Déplacement en L (comme un cavalier)
#     'D': (70, 130, 180),   # Bleu acier - Déplacement dans toutes les directions
# }

TILE_IMAGES = {
    'A': pygame.image.load(os.path.join("design_case", "rouge_sans_blanc.png")),
    'B': pygame.image.load(os.path.join("design_case", "jaune_sans_blanc.png")),
    'C': pygame.image.load(os.path.join("design_case", "vert_sans_blanc.png")),
    'D': pygame.image.load(os.path.join("design_case", "bleu_sans_blanc.png")),
}

CONTOUR_IMAGE = pygame.image.load(os.path.join("design_case", "contour.png"))
COIN_IMAGE = pygame.image.load(os.path.join("design_case", "coin.png"))

# Taille du plateau
BOARD_SIZE = 8

# Taille des cases
TILE_SIZE = 45

TILE_KEYS = ['A', 'B', 'C', 'D']


# Générer un plateau aléatoire
def generate_random_board():
    board = []
    for _ in range(BOARD_SIZE):
        row = []
        for _ in range(BOARD_SIZE):
            tile_type = random.choice(TILE_KEYS)
            row.append(tile_type)
        board.append(row)
    return board

# Générer un plateau à partir de quadrants
def generate_board_from_quadrants(quadrants):
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    # Placer les quadrants
    for i in range(2):
        for j in range(2):
            quadrant_index = i * 2 + j
            quadrant = quadrants[quadrant_index]
            for y in range(4):
                for x in range(4):
                    board[i * 4 + y][j * 4 + x] = quadrant[y][x]
    
    return board

# Générer un quadrant aléatoire
def generate_random_quadrant():
    quadrant = []
    for _ in range(4):
        row = []
        for _ in range(4):
            tile_type = random.choice(TILE_KEYS)
            row.append(tile_type)
        quadrant.append(row)
    return quadrant

# Rotation d'un quadrant
def rotate_quadrant(quadrant, rotations=1):
    for _ in range(rotations):
        quadrant = [list(row) for row in zip(*quadrant[::-1])]
    return quadrant

def draw_borders_and_corners(screen, board_x, board_y, board_width, board_height):
    # Redimensionner les images
    contour_scaled_h = pygame.transform.scale(CONTOUR_IMAGE, (TILE_SIZE, TILE_SIZE))  # Horizontal
    contour_scaled_v = pygame.transform.rotate(contour_scaled_h, 90)  # Vertical
    coin_scaled = pygame.transform.scale(COIN_IMAGE, (TILE_SIZE, TILE_SIZE))  # Coin

    # === Dessiner les contours ===

    # Haut et bas
    for x in range(BOARD_SIZE):
        screen.blit(contour_scaled_h, (board_x + x * TILE_SIZE, board_y - TILE_SIZE))            # Haut
        screen.blit(contour_scaled_h, (board_x + x * TILE_SIZE, board_y + board_height))         # Bas

    # Gauche et droite
    for y in range(BOARD_SIZE):
        screen.blit(contour_scaled_v, (board_x - TILE_SIZE, board_y + y * TILE_SIZE))            # Gauche
        screen.blit(contour_scaled_v, (board_x + board_width, board_y + y * TILE_SIZE))          # Droite

    # === Dessiner les coins ===

    screen.blit(coin_scaled, (board_x - TILE_SIZE, board_y - TILE_SIZE))                                # Haut gauche
    screen.blit(pygame.transform.rotate(coin_scaled, 90), (board_x + board_width, board_y - TILE_SIZE)) # Haut droit
    screen.blit(pygame.transform.rotate(coin_scaled, 270), (board_x - TILE_SIZE, board_y + board_height)) # Bas gauche
    screen.blit(pygame.transform.rotate(coin_scaled, 180), (board_x + board_width, board_y + board_height)) # Bas droit



# Dessiner le plateau
def draw_board(screen, fonts, selected_quadrants=None):
    board_width = BOARD_SIZE * TILE_SIZE
    board_height = BOARD_SIZE * TILE_SIZE
    
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    # Calculer la position du plateau pour le centrer
    board_x = (screen_width - board_width) // 2
    board_y = (screen_height - board_height) // 2

    draw_borders_and_corners(screen, board_x, board_y, board_width, board_height)


    # Générer le plateau
    if selected_quadrants:
        board = generate_board_from_quadrants(selected_quadrants)
    else:
        board = generate_random_board()

    # Dessiner les cases
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            tile_type = board[y][x]
            
            tile_rect = pygame.Rect(
                board_x + x * TILE_SIZE,
                board_y + y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
            tile_image = TILE_IMAGES[tile_type]
            tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
            screen.blit(tile_image, tile_rect.topleft)

            pygame.draw.rect(screen, BLACK, tile_rect, 1)

    # Dessiner les pièces initiales
    piece_radius = TILE_SIZE // 3
    pygame.draw.circle(screen, RED, (
        board_x + TILE_SIZE // 2,
        board_y + TILE_SIZE // 2
    ), piece_radius)
    
    pygame.draw.circle(screen, BLUE, (
        board_x + 7 * TILE_SIZE + TILE_SIZE // 2,
        board_y + 7 * TILE_SIZE + TILE_SIZE // 2
    ), piece_radius)

    # === Dessiner les contours ===
    contour_scaled_h = pygame.transform.scale(CONTOUR_IMAGE, (TILE_SIZE, TILE_SIZE))
    contour_scaled_v = pygame.transform.rotate(contour_scaled_h, 90)

    # Haut et bas
    for x in range(BOARD_SIZE):
        screen.blit(contour_scaled_h, (board_x + x * TILE_SIZE, board_y - TILE_SIZE))  # haut
        screen.blit(contour_scaled_h, (board_x + x * TILE_SIZE, board_y + board_height))  # bas

    # Gauche et droite
    for y in range(BOARD_SIZE):
        screen.blit(contour_scaled_v, (board_x - TILE_SIZE, board_y + y * TILE_SIZE))  # gauche
        screen.blit(contour_scaled_v, (board_x + board_width, board_y + y * TILE_SIZE))  # droite

    # === Dessiner les coins ===
    coin_scaled = pygame.transform.scale(COIN_IMAGE, (TILE_SIZE, TILE_SIZE))

    screen.blit(coin_scaled, (board_x - TILE_SIZE, board_y - TILE_SIZE))  # coin haut gauche
    screen.blit(pygame.transform.rotate(coin_scaled, 90), (board_x + board_width, board_y - TILE_SIZE))  # haut droit
    screen.blit(pygame.transform.rotate(coin_scaled, 270), (board_x - TILE_SIZE, board_y + board_height))  # bas gauche
    screen.blit(pygame.transform.rotate(coin_scaled, 180), (board_x + board_width, board_y + board_height))  # bas droit

    return board

# Interface pour configurer le plateau
# Interface pour configurer le plateau
def configure_board(screen, fonts):
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # Charger les images de contour et de coin
    CONTOUR_IMAGE = pygame.image.load(os.path.join("design_case", "contour.png"))
    COIN_IMAGE = pygame.image.load(os.path.join("design_case", "coin.png"))

    # Générer 4 quadrants aléatoires
    quadrants = [generate_random_quadrant() for _ in range(4)]
    rotations = [0, 0, 0, 0]  # Rotation actuelle pour chaque quadrant

    # Taille d'un quadrant affiché
    quadrant_size = 4 * TILE_SIZE
    board_width = 8 * TILE_SIZE
    board_height = 8 * TILE_SIZE

    running = True

    while running:
        screen.fill(WHITE)

        # Titre
        title_text = fonts['title'].render("Configuration du plateau", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))

        # Instructions
        instruction_text = fonts['small'].render("Cliquez sur un quadrant pour le faire pivoter", True, BLACK)
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, 90))  # Espacement augmenté

        board_x = screen_width // 2 - quadrant_size 
        board_y = 160

        draw_borders_and_corners(screen, board_x, board_y, board_width, board_height)

        # Dessiner les quadrants
        for i in range(2):
            for j in range(2):
                quadrant_index = i * 2 + j
                quadrant = rotate_quadrant(quadrants[quadrant_index], rotations[quadrant_index])

                quadrant_x = board_x + j * quadrant_size
                quadrant_y = board_y + i * quadrant_size

                # Dessiner chaque case du quadrant
                for y in range(4):
                    for x in range(4):
                        tile_type = quadrant[y][x]
                        tile_rect = pygame.Rect(
                            quadrant_x + x * TILE_SIZE,
                            quadrant_y + y * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE
                        )

                        tile_image = TILE_IMAGES[tile_type]
                        tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
                        screen.blit(tile_image, tile_rect.topleft)
                        pygame.draw.rect(screen, BLACK, tile_rect, 1)

                # Cadre autour du quadrant
                pygame.draw.rect(screen, BLACK, (
                    quadrant_x,
                    quadrant_y,
                    quadrant_size,
                    quadrant_size
                ), 2)

        # === Ajouter contours et coins ===
        contour_scaled_h = pygame.transform.scale(CONTOUR_IMAGE, (TILE_SIZE, TILE_SIZE))
        contour_scaled_v = pygame.transform.rotate(contour_scaled_h, 90)
        coin_scaled = pygame.transform.scale(COIN_IMAGE, (TILE_SIZE, TILE_SIZE))

        # Haut et bas
        for x in range(8):
            screen.blit(contour_scaled_h, (board_x + x * TILE_SIZE, board_y - TILE_SIZE))  # haut
            screen.blit(contour_scaled_h, (board_x + x * TILE_SIZE, board_y + board_height))  # bas

        # Gauche et droite
        for y in range(8):
            screen.blit(contour_scaled_v, (board_x - TILE_SIZE, board_y + y * TILE_SIZE))  # gauche
            screen.blit(contour_scaled_v, (board_x + board_width, board_y + y * TILE_SIZE))  # droite

        # Coins
        screen.blit(coin_scaled, (board_x - TILE_SIZE, board_y - TILE_SIZE))  # haut gauche
        screen.blit(pygame.transform.rotate(coin_scaled, 90), (board_x + board_width, board_y - TILE_SIZE))  # haut droit
        screen.blit(pygame.transform.rotate(coin_scaled, 270), (board_x - TILE_SIZE, board_y + board_height))  # bas gauche
        screen.blit(pygame.transform.rotate(coin_scaled, 180), (board_x + board_width, board_y + board_height))  # bas droit

        # Bouton Valider
        valid_button_y = board_y + board_height + 50  # Ajusté pour positionner le bouton à l'intérieur du cadre
        valid_button = draw_button(screen, fonts, "Valider", screen_width // 2 - 100, valid_button_y, 200, 50, GREEN, HOVER_GREEN)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Vérifier si un quadrant a été cliqué
                for i in range(2):
                    for j in range(2):
                        quadrant_index = i * 2 + j
                        quadrant_x = board_x + j * quadrant_size
                        quadrant_y = board_y + i * quadrant_size

                        quadrant_rect = pygame.Rect(
                            quadrant_x,
                            quadrant_y,
                            quadrant_size,
                            quadrant_size
                        )

                        if quadrant_rect.collidepoint(mouse_x, mouse_y):
                            if click_sound:
                                click_sound.play()
                            rotations[quadrant_index] = (rotations[quadrant_index] + 1) % 4

                # Vérifier si le bouton Valider a été cliqué
                if valid_button.collidepoint(mouse_x, mouse_y):
                    if click_sound:
                        click_sound.play()
                    rotated_quadrants = [rotate_quadrant(quadrants[i], rotations[i]) for i in range(4)]
                    return rotated_quadrants

        pygame.display.flip()
