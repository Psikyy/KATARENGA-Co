import pygame
import random
import sys
import os
from random import choice
from menu.settings import t

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
HOVER_GREEN = (0, 200, 0)
RED = (255, 0, 0)
BOARD_SIZE = 8
TILE_SIZE = 55
TILE_KEYS = ['A', 'B', 'C', 'D']  

TILE_IMAGES = {
    'A': pygame.image.load(os.path.join("design_case", "rouge_sans_blanc.png")),
    'B': pygame.image.load(os.path.join("design_case", "jaune_sans_blanc.png")),
    'C': pygame.image.load(os.path.join("design_case", "vert_sans_blanc.png")),
    'D': pygame.image.load(os.path.join("design_case", "bleu_sans_blanc.png")),
}

CONTOUR_IMAGE = pygame.image.load(os.path.join("design_case", "contour.png"))
COIN_IMAGE = pygame.image.load(os.path.join("design_case", "coin.png"))

def validate_board(board):
    """
    Validate that the board meets Katarenga's color distribution rules
    
    Args:
        board (List[List[str]]): 8x8 board of tile types
    
    Returns:
        bool: True if board is valid, False otherwise
    """
    quadrants = split_board_into_quadrants(board)
    for quadrant in quadrants:
        if not is_valid_quadrant(quadrant):
            return False
    
    return True

def split_board_into_quadrants(board_8x8):
    """
    Split an 8x8 board into 4 quadrants
    
    Args:
        board_8x8 (List[List[str]]): 8x8 board
    
    Returns:
        List[List[List[str]]]: 4 quadrants of 4x4 tiles
    """
    quadrants = []
    for i in range(2):
        for j in range(2):
            quadrant = [row[j*4:(j+1)*4] for row in board_8x8[i*4:(i+1)*4]]
            quadrants.append(quadrant)
    return quadrants

def is_valid_quadrant(quadrant):
    """
    Check if a quadrant has exactly 4 tiles of each color
    
    Args:
        quadrant (List[List[str]]): 4x4 quadrant of tiles
    
    Returns:
        bool: True if quadrant is valid, False otherwise
    """
    flat = [cell for row in quadrant for cell in row]
    return all(flat.count(color) == 4 for color in TILE_KEYS)

def generate_random_quadrant():
    """
    Generate a random valid 4x4 quadrant
    
    Returns:
        List[List[str]]: A 4x4 quadrant with balanced color distribution
    """
    tiles = ['A'] * 4 + ['B'] * 4 + ['C'] * 4 + ['D'] * 4
    random.shuffle(tiles)
    return [tiles[i*4:(i+1)*4] for i in range(4)]

def generate_board_from_quadrants(quadrants):
    """
    Generate an 8x8 board from 4 quadrants
    
    Args:
        quadrants (List[List[List[str]]]): 4 quadrants to combine
    
    Returns:
        List[List[str]]: 8x8 board
    """
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for i in range(2):
        for j in range(2):
            quadrant = quadrants[i * 2 + j]
            for y in range(4):
                for x in range(4):
                    board[i * 4 + y][j * 4 + x] = quadrant[y][x]
    return board

def rotate_quadrant(quadrant, rotations=1):
    """
    Rotate a quadrant 90 degrees clockwise
    
    Args:
        quadrant (List[List[str]]): 4x4 quadrant to rotate
        rotations (int): Number of 90-degree rotations
    
    Returns:
        List[List[str]]: Rotated quadrant
    """
    for _ in range(rotations):
        quadrant = [list(row) for row in zip(*quadrant[::-1])]
    return quadrant

def create_random_board(rows=8, cols=8):
    """
    Create a completely random board
    
    Args:
        rows (int): Number of rows
        cols (int): Number of columns
    
    Returns:
        List[List[str]]: Randomly generated board
    """
    possible_tiles = ['A', 'B', 'C', 'D']
    while True:
        board = [[choice(possible_tiles) for _ in range(cols)] for _ in range(rows)]
        if validate_board(board):
            return board

def draw_borders_and_corners(screen, board_x, board_y, board_width, board_height):
    """
    Draw decorative borders and corners around the board
    
    Args:
        screen (pygame.Surface): Surface to draw on
        board_x (int): X coordinate of board's top-left corner
        board_y (int): Y coordinate of board's top-left corner
        board_width (int): Width of the board
        board_height (int): Height of the board
    """
    contour_scaled_h = pygame.transform.scale(CONTOUR_IMAGE, (TILE_SIZE, TILE_SIZE))
    contour_scaled_v = pygame.transform.rotate(contour_scaled_h, 90)
    coin_scaled = pygame.transform.scale(COIN_IMAGE, (TILE_SIZE, TILE_SIZE))

    for x in range(BOARD_SIZE):
        screen.blit(contour_scaled_h, (board_x + x * TILE_SIZE, board_y - TILE_SIZE))
        screen.blit(contour_scaled_h, (board_x + x * TILE_SIZE, board_y + board_height))

    for y in range(BOARD_SIZE):
        screen.blit(contour_scaled_v, (board_x - TILE_SIZE, board_y + y * TILE_SIZE))
        screen.blit(contour_scaled_v, (board_x + board_width, board_y + y * TILE_SIZE))

    screen.blit(coin_scaled, (board_x - TILE_SIZE, board_y - TILE_SIZE))
    screen.blit(pygame.transform.rotate(coin_scaled, 90), (board_x + board_width, board_y - TILE_SIZE))
    screen.blit(pygame.transform.rotate(coin_scaled, 270), (board_x - TILE_SIZE, board_y + board_height))
    screen.blit(pygame.transform.rotate(coin_scaled, 180), (board_x + board_width, board_y + board_height))

def draw_board(screen, fonts, board, draw_pieces=True):
    """
    Draw the game board on the screen
    
    Args:
        screen (pygame.Surface): Surface to draw on
        fonts (dict): Dictionary of fonts
        board (List[List[str]]): 8x8 board to draw
        draw_pieces (bool): Whether to draw game pieces (default True)
    
    Returns:
        List[List[str]]: The drawn board (for consistency)
    """
    if not board or not isinstance(board, list) or len(board) != BOARD_SIZE:
        raise ValueError(f"Invalid board: must be an {BOARD_SIZE}x{BOARD_SIZE} list of tile types")
    
    board_width = BOARD_SIZE * TILE_SIZE
    board_height = BOARD_SIZE * TILE_SIZE
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    board_x = (screen_width - board_width) // 2
    board_y = (screen_height - board_height) // 2

    draw_borders_and_corners(screen, board_x, board_y, board_width, board_height)

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            tile_type = str(board[y][x])
            
            tile_rect = pygame.Rect(
                board_x + x * TILE_SIZE,
                board_y + y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )

            if tile_type not in TILE_IMAGES:
                print(f"Warning: Unknown tile type {tile_type}. Using default.")
                tile_type = 'A' 
            
            tile_image = pygame.transform.scale(TILE_IMAGES[tile_type], (TILE_SIZE, TILE_SIZE))
            screen.blit(tile_image, tile_rect.topleft)
            pygame.draw.rect(screen, BLACK, tile_rect, 1)

    return board

def configure_board(screen, fonts):
    """
    Interactive board configuration interface
    
    Args:
        screen (pygame.Surface): Screen to draw on
        fonts (dict): Dictionary of fonts
    
    Returns:
        List[List[str]]: Configured board
    """
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    quadrants = [generate_random_quadrant() for _ in range(4)]
    rotations = [0, 0, 0, 0]

    quadrant_size = 4 * TILE_SIZE
    board_width = 8 * TILE_SIZE
    board_height = 8 * TILE_SIZE

    running = True

    while running:
        screen.fill(WHITE)

        # Render title
        title_text = fonts['title'].render(t("board_edit"), True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))

        # Render instructions
        instruction_text = fonts['small'].render(t("help_text"), True, BLACK)

        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, 90))
        board_y = 170
        board_x = screen_width // 2 - quadrant_size
        draw_borders_and_corners(screen, board_x, board_y, board_width, board_height)
        for i in range(2):
            for j in range(2):
                idx = i * 2 + j
                quadrant = rotate_quadrant(quadrants[idx], rotations[idx])

                quad_x = board_x + j * quadrant_size
                quad_y = board_y + i * quadrant_size

                for y in range(4):
                    for x in range(4):
                        tile_type = quadrant[y][x]
                        tile_rect = pygame.Rect(
                            quad_x + x * TILE_SIZE,
                            quad_y + y * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE
                        )
                        tile_image = pygame.transform.scale(TILE_IMAGES[tile_type], (TILE_SIZE, TILE_SIZE))
                        screen.blit(tile_image, tile_rect.topleft)
                        pygame.draw.rect(screen, BLACK, tile_rect, 1)
                pygame.draw.rect(screen, BLACK, (quad_x, quad_y, quadrant_size, quadrant_size), 2)
        valid_button_y = board_y + board_height + 70
        valid_button = pygame.Rect(screen_width // 2 - 100, valid_button_y, 200, 50)
        edit_button = pygame.Rect(screen_width // 2 - 100, valid_button_y + 70, 200, 50)
        pygame.draw.rect(screen, GREEN, valid_button)
        pygame.draw.rect(screen, GREEN, edit_button)

        # Button text
        valid_text = fonts['small'].render(t("validate"), True, BLACK)
        edit_text = fonts['small'].render(t("edit"), True, BLACK)
        
        screen.blit(valid_text, (valid_button.x + (valid_button.width - valid_text.get_width()) // 2, 
                                  valid_button.y + (valid_button.height - valid_text.get_height()) // 2))
        screen.blit(edit_text, (edit_button.x + (edit_button.width - edit_text.get_width()) // 2, 
                                edit_button.y + (edit_button.height - edit_text.get_height()) // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for i in range(2):
                    for j in range(2):
                        idx = i * 2 + j
                        quad_x = board_x + j * quadrant_size
                        quad_y = board_y + i * quadrant_size
                        rect = pygame.Rect(quad_x, quad_y, quadrant_size, quadrant_size)
                        if rect.collidepoint(mouse_x, mouse_y):
                            rotations[idx] = (rotations[idx] + 1) % 4
                if valid_button.collidepoint(mouse_x, mouse_y):
                    rotated_quadrants = [rotate_quadrant(quadrants[i], rotations[i]) for i in range(4)]
                    current_board = generate_board_from_quadrants(rotated_quadrants)
                    if validate_board(current_board):
                        return current_board

                if edit_button.collidepoint(mouse_x, mouse_y):
                    current_board = generate_board_from_quadrants(
                        [rotate_quadrant(quadrants[i], rotations[i]) for i in range(4)])
                    current_board = edit_board(screen, fonts, current_board)
                    return current_board

        pygame.display.flip()

def edit_board(screen, fonts, board):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    working_board = [row.copy() for row in board]
    y_cursor, x_cursor = 0, 0

    running = True
    while running:
        screen.fill(WHITE)

        # Title
        title_text = fonts['title'].render(t("board_edit"), True, BLACK)

        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))
        board_x = screen_width // 2 - (8 * TILE_SIZE) // 2
        board_y = 100
        for y in range(8):
            for x in range(8):
                tile_type = working_board[y][x]
                tile_rect = pygame.Rect(board_x + x * TILE_SIZE, board_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile_type not in TILE_IMAGES:
                    tile_type = 'A' 
                
                tile_image = pygame.transform.scale(TILE_IMAGES[tile_type], (TILE_SIZE, TILE_SIZE))
                screen.blit(tile_image, tile_rect.topleft)
                pygame.draw.rect(screen, BLACK, tile_rect, 1)
        pygame.draw.rect(screen, RED, (
            board_x + x_cursor * TILE_SIZE,
            board_y + y_cursor * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        ), 3)
        confirm_button = pygame.Rect(screen_width // 2 - 100, screen_height - 80, 200, 50)
        pygame.draw.rect(screen, GREEN, confirm_button)
        confirm_text = fonts['small'].render(t("confirm"), True, BLACK)
        screen.blit(confirm_text, (
            confirm_button.x + (confirm_button.width - confirm_text.get_width()) // 2,
            confirm_button.y + (confirm_button.height - confirm_text.get_height()) // 2
        ))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    x_cursor = (x_cursor + 1) % 8
                elif event.key == pygame.K_LEFT:
                    x_cursor = (x_cursor - 1) % 8
                elif event.key == pygame.K_DOWN:
                    y_cursor = (y_cursor + 1) % 8
                elif event.key == pygame.K_UP:
                    y_cursor = (y_cursor - 1) % 8
                elif event.key == pygame.K_SPACE:
                    current_index = TILE_KEYS.index(working_board[y_cursor][x_cursor])
                    next_index = (current_index + 1) % len(TILE_KEYS)
                    working_board[y_cursor][x_cursor] = TILE_KEYS[next_index]
                elif event.key == pygame.K_RETURN:
                    if validate_board(working_board):
                        return working_board

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for y in range(8):
                    for x in range(8):
                        tile_rect = pygame.Rect(board_x + x * TILE_SIZE, board_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if tile_rect.collidepoint(mouse_x, mouse_y):
                            current_index = TILE_KEYS.index(working_board[y][x])
                            next_index = (current_index + 1) % len(TILE_KEYS)
                            working_board[y][x] = TILE_KEYS[next_index]
                if confirm_button.collidepoint(mouse_x, mouse_y):
                    if validate_board(working_board):
                        return working_board

        pygame.display.flip()
    return board
def print_board(board):
    """
    Print a text representation of the board for debugging
    
    Args:
        board (List[List[str]]): Board to print
    """
    for row in board:
        print(' '.join(row))

def board_to_quadrants(board):
    """
    Convert a full board back to quadrants
    
    Args:
        board (List[List[str]]): 8x8 board
    
    Returns:
        List[List[List[str]]]: 4 quadrants
    """
    return split_board_into_quadrants(board)
__all__ = [
    'create_random_board',
    'configure_board',
    'draw_board',
    'edit_board',
    'validate_board',
    'generate_board_from_quadrants',
    'split_board_into_quadrants',
    'rotate_quadrant',
    'print_board',
    'board_to_quadrants'
]