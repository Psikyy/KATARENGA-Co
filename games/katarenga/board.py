import pygame
import random
import sys
import os
from ui.colors import WHITE, BLACK, BLUE, RED, GREEN, HOVER_GREEN
from ui.buttons import draw_button, click_sound

# Tile movement types and their respective images
TILE_IMAGES = {
    'A': pygame.image.load(os.path.join("design_case", "rouge_sans_blanc.png")),  # Orthogonal movement
    'B': pygame.image.load(os.path.join("design_case", "jaune_sans_blanc.png")),  # Diagonal movement
    'C': pygame.image.load(os.path.join("design_case", "vert_sans_blanc.png")),   # L-shaped movement (like a knight)
    'D': pygame.image.load(os.path.join("design_case", "bleu_sans_blanc.png")),   # Movement in all directions
}

# Border and corner images
CONTOUR_IMAGE = pygame.image.load(os.path.join("design_case", "contour.png"))
COIN_IMAGE = pygame.image.load(os.path.join("design_case", "coin.png"))

# Board size
BOARD_SIZE = 8

# Tile size
TILE_SIZE = 55

TILE_KEYS = ['A', 'B', 'C', 'D']

# Generate a random board
def generate_random_board():
    board = []
    for _ in range(BOARD_SIZE):
        row = []
        for _ in range(BOARD_SIZE):
            tile_type = random.choice(TILE_KEYS)
            row.append(tile_type)
        board.append(row)
    return board

# Generate a board from quadrants
def generate_board_from_quadrants(quadrants):
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    # Place the quadrants
    for i in range(2):
        for j in range(2):
            quadrant_index = i * 2 + j
            quadrant = quadrants[quadrant_index]
            for y in range(4):
                for x in range(4):
                    board[i * 4 + y][j * 4 + x] = quadrant[y][x]
    
    return board

# Generate a random quadrant
def generate_random_quadrant():
    quadrant = []
    for _ in range(4):
        row = []
        for _ in range(4):
            tile_type = random.choice(TILE_KEYS)
            row.append(tile_type)
        quadrant.append(row)
    return quadrant

# Rotate a quadrant
def rotate_quadrant(quadrant, rotations=1):
    for _ in range(rotations):
        quadrant = [list(row) for row in zip(*quadrant[::-1])]
    return quadrant

# Draw borders and corners around the board
def draw_borders_and_corners(screen, board_x, board_y, board_width, board_height):
    # Resize the images
    contour_scaled_h = pygame.transform.scale(CONTOUR_IMAGE, (TILE_SIZE, TILE_SIZE))  # Horizontal
    contour_scaled_v = pygame.transform.rotate(contour_scaled_h, 90)  # Vertical
    coin_scaled = pygame.transform.scale(COIN_IMAGE, (TILE_SIZE, TILE_SIZE))  # Corner

    # Draw the borders
    # Top and bottom
    for x in range(BOARD_SIZE):
        screen.blit(contour_scaled_h, (board_x + x * TILE_SIZE, board_y - TILE_SIZE))  # Top
        screen.blit(contour_scaled_h, (board_x + x * TILE_SIZE, board_y + board_height))  # Bottom

    # Left and right
    for y in range(BOARD_SIZE):
        screen.blit(contour_scaled_v, (board_x - TILE_SIZE, board_y + y * TILE_SIZE))  # Left
        screen.blit(contour_scaled_v, (board_x + board_width, board_y + y * TILE_SIZE))  # Right

    # Draw the corners
    screen.blit(coin_scaled, (board_x - TILE_SIZE, board_y - TILE_SIZE))  # Top left
    screen.blit(pygame.transform.rotate(coin_scaled, 90), (board_x + board_width, board_y - TILE_SIZE))  # Top right
    screen.blit(pygame.transform.rotate(coin_scaled, 270), (board_x - TILE_SIZE, board_y + board_height))  # Bottom left
    screen.blit(pygame.transform.rotate(coin_scaled, 180), (board_x + board_width, board_y + board_height))  # Bottom right

# Draw the board
def draw_board(screen, fonts, selected_quadrants=None, draw_pieces=True):
    board_width = BOARD_SIZE * TILE_SIZE
    board_height = BOARD_SIZE * TILE_SIZE
    
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    # Calculate the position of the board to center it
    board_x = (screen_width - board_width) // 2
    board_y = (screen_height - board_height) // 2

    # Generate the board
    if selected_quadrants:
        board = generate_board_from_quadrants(selected_quadrants)
    else:
        board = generate_random_board()

    # Draw the borders and corners
    draw_borders_and_corners(screen, board_x, board_y, board_width, board_height)

    # Define the positions of the camps
    camps1_positions = [(0, 0), (7, 0)]  # Camps of player 1 (Black)
    camps2_positions = [(0, 7), (7, 7)]  # Camps of player 2 (White)

    # Draw the tiles
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            tile_type = board[y][x]
            
            tile_rect = pygame.Rect(
                board_x + x * TILE_SIZE,
                board_y + y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
            
            # Check if it's a camp
            is_camp1 = (x, y) in camps1_positions
            is_camp2 = (x, y) in camps2_positions
            
            # Draw the tile with its image
            tile_image = TILE_IMAGES[tile_type]
            tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
            screen.blit(tile_image, tile_rect.topleft)
            
            # Add a pattern or marker for the camps
            if is_camp1 or is_camp2:
                # More visible frame for the camps
                camp_color = BLACK if is_camp1 else WHITE
                pygame.draw.rect(screen, camp_color, tile_rect, 3)
                
                if is_camp2:  # Add a black outline for white camps
                    pygame.draw.rect(screen, BLACK, tile_rect, 1)
            
            # Border for all tiles
            pygame.draw.rect(screen, BLACK, tile_rect, 1)

    # Draw the initial pieces if requested
    if draw_pieces:
        piece_radius = TILE_SIZE // 3
        pygame.draw.circle(screen, RED, (
            board_x + TILE_SIZE // 2,
            board_y + TILE_SIZE // 2
        ), piece_radius)
        
        pygame.draw.circle(screen, BLUE, (
            board_x + 7 * TILE_SIZE + TILE_SIZE // 2,
            board_y + 7 * TILE_SIZE + TILE_SIZE // 2
        ), piece_radius)

    return board

# Interface to configure the board
def configure_board(screen, fonts):
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # Generate 4 random quadrants
    quadrants = [generate_random_quadrant() for _ in range(4)]
    rotations = [0, 0, 0, 0]  # Current rotation for each quadrant

    # Size of a displayed quadrant
    quadrant_size = 4 * TILE_SIZE
    board_width = 8 * TILE_SIZE
    board_height = 8 * TILE_SIZE

    running = True

    while running:
        screen.fill(WHITE)

        # Title
        title_text = fonts['title'].render("Configuration du plateau", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))

        # Instructions
        instruction_text = fonts['small'].render("Cliquez sur un quadrant pour le faire pivoter", True, BLACK)
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, 90))

        # Calculate board position to center it
        board_x = screen_width // 2 - quadrant_size 
        board_y = 160

        # Add borders and corners
        draw_borders_and_corners(screen, board_x, board_y, board_width, board_height)

        # Draw the quadrants
        for i in range(2):
            for j in range(2):
                quadrant_index = i * 2 + j
                quadrant = rotate_quadrant(quadrants[quadrant_index], rotations[quadrant_index])

                quadrant_x = board_x + j * quadrant_size
                quadrant_y = board_y + i * quadrant_size

                # Draw each tile of the quadrant
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

                # Frame around the quadrant
                pygame.draw.rect(screen, BLACK, (
                    quadrant_x,
                    quadrant_y,
                    quadrant_size,
                    quadrant_size
                ), 2)

        # Validate button
        valid_button_y = board_y + board_height + 50
        valid_button = draw_button(screen, fonts, "Valider", screen_width // 2 - 100, valid_button_y, 200, 50, GREEN, HOVER_GREEN)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Check if a quadrant was clicked
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

                # Check if the Validate button was clicked
                if valid_button.collidepoint(mouse_x, mouse_y):
                    if click_sound:
                        click_sound.play()
                    rotated_quadrants = [rotate_quadrant(quadrants[i], rotations[i]) for i in range(4)]
                    return rotated_quadrants

        pygame.display.flip()