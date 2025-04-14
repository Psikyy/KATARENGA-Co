import pygame
import random
import sys
from ui.colors import WHITE, BLACK, BLUE, RED, GREEN, HOVER_GREEN
from ui.buttons import draw_button, click_sound

# Définition des types de cases et leurs couleurs
TILE_TYPES = {
    'A': (220, 220, 220),  # Gris clair - Déplacement orthogonal
    'B': (160, 82, 45),    # Marron - Déplacement diagonal
    'C': (0, 128, 0),      # Vert - Déplacement en L (comme un cavalier)
    'D': (70, 130, 180),   # Bleu acier - Déplacement dans toutes les directions
}

# Taille du plateau
BOARD_SIZE = 8

# Taille des cases
TILE_SIZE = 60

# Générer un plateau aléatoire
def generate_random_board():
    board = []
    for _ in range(BOARD_SIZE):
        row = []
        for _ in range(BOARD_SIZE):
            tile_type = random.choice(list(TILE_TYPES.keys()))
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
            tile_type = random.choice(list(TILE_TYPES.keys()))
            row.append(tile_type)
        quadrant.append(row)
    return quadrant

# Rotation d'un quadrant
def rotate_quadrant(quadrant, rotations=1):
    for _ in range(rotations):
        quadrant = [list(row) for row in zip(*quadrant[::-1])]
    return quadrant

# Dessiner le plateau
def draw_board(screen, fonts, selected_quadrants=None, draw_pieces=True):
    # Taille du plateau original (8x8)
    board_width = BOARD_SIZE * TILE_SIZE
    board_height = BOARD_SIZE * TILE_SIZE
    
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    # Taille de la bordure décorative
    border_size = TILE_SIZE // 2
    
    # Calculer la position du plateau pour le centrer (en incluant la bordure)
    board_x = (screen_width - (board_width + 2 * border_size)) // 2 + border_size
    board_y = (screen_height - (board_height + 2 * border_size)) // 2 + border_size
    
    # Générer le plateau si nécessaire
    if selected_quadrants:
        board = generate_board_from_quadrants(selected_quadrants)
    else:
        board = generate_random_board()
    
    # Dessiner la bordure décorative (avec arrière-plan gris foncé)
    border_color = (50, 50, 60)  # Gris foncé pour la bordure
    # Bordure extérieure complète
    pygame.draw.rect(screen, border_color, (
        board_x - border_size,
        board_y - border_size,
        board_width + 2 * border_size,
        board_height + 2 * border_size
    ))
    
    # Ajouter des motifs ou décorations dans la bordure
    # Motifs aux coins non-camp (coin supérieur droit et inférieur gauche)
    corner_decoration_size = border_size - 4
    
    # Couleur du motif coin
    corner_color = (30, 30, 30)  # Noir/gris foncé

    # Coin supérieur gauche
    pygame.draw.rect(screen, corner_color, (
        board_x - border_size + 2,
        board_y - border_size + 2,
        corner_decoration_size,
        corner_decoration_size
    ))

    # Coin supérieur droit
    pygame.draw.rect(screen, corner_color, (
        board_x + board_width + 2,
        board_y - border_size + 2,
        corner_decoration_size,
        corner_decoration_size
    ))

    # Coin inférieur gauche
    pygame.draw.rect(screen, corner_color, (
        board_x - border_size + 2,
        board_y + board_height + 2,
        corner_decoration_size,
        corner_decoration_size
    ))

    # Coin inférieur droit
    pygame.draw.rect(screen, corner_color, (
        board_x + board_width + 2,
        board_y + board_height + 2,
        corner_decoration_size,
        corner_decoration_size
    ))

    
    # Définir les positions des camps
    camps1_positions = [(0, 0), (7, 0)]  # Camps du joueur 1 (Noir)
    camps2_positions = [(0, 7), (7, 7)]  # Camps du joueur 2 (Blanc)
    
    # Dessiner chaque case du plateau
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            tile_type = board[y][x]
            tile_color = TILE_TYPES[tile_type]
            
            tile_rect = pygame.Rect(
                board_x + x * TILE_SIZE,
                board_y + y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
            
            # Vérifier si c'est un camp
            is_camp1 = (x, y) in camps1_positions
            is_camp2 = (x, y) in camps2_positions
            
            # Dessiner la case avec sa couleur normale
            pygame.draw.rect(screen, tile_color, tile_rect)
            
            # Ajouter un motif ou une marque pour les camps
            if is_camp1 or is_camp2:
                # Encadrement plus visible pour les camps
                camp_color = BLACK if is_camp1 else WHITE
                pygame.draw.rect(screen, camp_color, tile_rect, 3)
                
                if is_camp2:  # Ajouter un contour noir pour les camps blancs
                    pygame.draw.rect(screen, BLACK, tile_rect, 1)
            
            # Bordure fine pour toutes les cases
            pygame.draw.rect(screen, BLACK, tile_rect, 1)
            
            # Afficher le type de la case (pour le débogage)
            tile_text = fonts['small'].render(tile_type, True, BLACK)
            screen.blit(tile_text, (
                board_x + x * TILE_SIZE + (TILE_SIZE - tile_text.get_width()) // 2,
                board_y + y * TILE_SIZE + (TILE_SIZE - tile_text.get_height()) // 2
            ))
    
    # Dessiner des décorations supplémentaires dans la bordure (similaires à l'image)
    # Motifs horizontaux et verticaux
    for i in range(1, 7):
        # Motif horizontal haut
        pygame.draw.rect(screen, (70, 70, 80), (
            board_x + i * TILE_SIZE,
            board_y - border_size + border_size//3,
            TILE_SIZE//2,
            border_size//3
        ))
        
        # Motif horizontal bas
        pygame.draw.rect(screen, (70, 70, 80), (
            board_x + i * TILE_SIZE,
            board_y + board_height + border_size//3,
            TILE_SIZE//2,
            border_size//3
        ))
        
        # Motif vertical gauche
        pygame.draw.rect(screen, (70, 70, 80), (
            board_x - border_size + border_size//3,
            board_y + i * TILE_SIZE,
            border_size//3,
            TILE_SIZE//2
        ))
        
        # Motif vertical droit
        pygame.draw.rect(screen, (70, 70, 80), (
            board_x + board_width + border_size//3,
            board_y + i * TILE_SIZE,
            border_size//3,
            TILE_SIZE//2
        ))
    
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
                        tile_color = TILE_TYPES[tile_type]
                        
                        tile_rect = pygame.Rect(
                            quadrant_x + x * TILE_SIZE,
                            quadrant_y + y * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE
                        )
                        
                        pygame.draw.rect(screen, tile_color, tile_rect)
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