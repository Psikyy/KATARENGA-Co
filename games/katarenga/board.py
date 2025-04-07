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
    'A': pygame.image.load(os.path.join("design_case", "rendu_case_rouge.png")),
    'B': pygame.image.load(os.path.join("design_case", "rendu_case_jaune.png")),
    'C': pygame.image.load(os.path.join("design_case", "rendu_case_vert.png")),
    'D': pygame.image.load(os.path.join("design_case", "rendu_case_bleu.png")),
}

# Taille du plateau
BOARD_SIZE = 8

# Taille des cases
TILE_SIZE = 60

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

# Dessiner le plateau
def draw_board(screen, fonts, selected_quadrants=None):
    board_width = BOARD_SIZE * TILE_SIZE
    board_height = BOARD_SIZE * TILE_SIZE
    
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    # Calculer la position du plateau pour le centrer
    board_x = (screen_width - board_width) // 2
    board_y = (screen_height - board_height) // 2
    
    # Générer le plateau si nécessaire
    if selected_quadrants:
        board = generate_board_from_quadrants(selected_quadrants)
    else:
        board = generate_random_board()
    
    # Dessiner chaque case
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
            tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))  # si pas déjà à la bonne taille
            screen.blit(tile_image, tile_rect.topleft)

            pygame.draw.rect(screen, BLACK, tile_rect, 1)
            
    # Dessiner les pièces initiales
    # Joueur 1 (Rouge)
    piece_radius = TILE_SIZE // 3
    pygame.draw.circle(screen, RED, (
        board_x + 0 * TILE_SIZE + TILE_SIZE // 2,
        board_y + 0 * TILE_SIZE + TILE_SIZE // 2
    ), piece_radius)
    
    # Joueur 2 (Bleu)
    pygame.draw.circle(screen, BLUE, (
        board_x + 7 * TILE_SIZE + TILE_SIZE // 2,
        board_y + 7 * TILE_SIZE + TILE_SIZE // 2
    ), piece_radius)
    
    return board

# Interface pour configurer le plateau
def configure_board(screen, fonts):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    # Générer 4 quadrants aléatoires
    quadrants = [generate_random_quadrant() for _ in range(4)]
    rotations = [0, 0, 0, 0]  # Rotation actuelle pour chaque quadrant
    
    # Taille d'un quadrant affiché
    quadrant_size = 4 * TILE_SIZE
    
    running = True
    
    while running:
        screen.fill(WHITE)
        
        # Titre
        title_text = fonts['title'].render("Configuration du plateau", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))
        
        # Instructions
        instruction_text = fonts['small'].render("Cliquez sur un quadrant pour le faire pivoter", True, BLACK)
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, 100))
        
        # Dessiner les quadrants
        for i in range(2):
            for j in range(2):
                quadrant_index = i * 2 + j
                quadrant = rotate_quadrant(quadrants[quadrant_index], rotations[quadrant_index])
                
                quadrant_x = screen_width // 2 - quadrant_size + j * quadrant_size
                quadrant_y = 150 + i * quadrant_size
                
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
                        tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))  # si ce n'est pas déjà fait
                        screen.blit(tile_image, tile_rect.topleft)

                        pygame.draw.rect(screen, BLACK, tile_rect, 1)
                        
                        # Afficher le type de la case
                        tile_text = fonts['small'].render(tile_type, True, BLACK)
                        screen.blit(tile_text, (
                            quadrant_x + x * TILE_SIZE + (TILE_SIZE - tile_text.get_width()) // 2,
                            quadrant_y + y * TILE_SIZE + (TILE_SIZE - tile_text.get_height()) // 2
                        ))
                
                # Cadre autour du quadrant
                pygame.draw.rect(screen, BLACK, (
                    quadrant_x,
                    quadrant_y,
                    quadrant_size,
                    quadrant_size
                ), 2)
        
        # Bouton Valider
        valid_button = draw_button(screen, fonts, "Valider", screen_width // 2 - 100, screen_height - 100, 200, 50, GREEN, HOVER_GREEN)
        
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
                        quadrant_x = screen_width // 2 - quadrant_size + j * quadrant_size
                        quadrant_y = 150 + i * quadrant_size
                        
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
                    # Préparer les quadrants avec les rotations appliquées
                    rotated_quadrants = [rotate_quadrant(quadrants[i], rotations[i]) for i in range(4)]
                    return rotated_quadrants
        
        pygame.display.flip()