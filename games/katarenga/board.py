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
BOARD_SIZE = 10
INNER_BOARD_SIZE = 8
TILE_SIZE = 55
TILE_KEYS = ['A', 'B', 'C', 'D']  

TILE_IMAGES = {
    'A': pygame.image.load(os.path.join("design_case", "rouge_sans_blanc.png")),
    'B': pygame.image.load(os.path.join("design_case", "jaune_sans_blanc.png")),
    'C': pygame.image.load(os.path.join("design_case", "vert_sans_blanc.png")),
    'D': pygame.image.load(os.path.join("design_case", "bleu_sans_blanc.png")),
    'CORNER': pygame.image.load(os.path.join("design_case", "coin.png")),
    'BORDER': pygame.image.load(os.path.join("design_case", "contour.png")),
}

CONTOUR_IMAGE = pygame.image.load(os.path.join("design_case", "contour.png"))
COIN_IMAGE = pygame.image.load(os.path.join("design_case", "coin.png"))

def validate_board(board):
    """
    Validate that the board meets Katarenga's color distribution rules
    
    Args:
        board (List[List[str]]): 10x10 board with corners and 8x8 game area
    
    Returns:
        bool: True if board is valid, False otherwise
    """
    corner_positions = [(0, 0), (0, 9), (9, 0), (9, 9)]
    for y, x in corner_positions:
        if board[y][x] != 'CORNER':
            return False
    
    inner_board = []
    for y in range(1, 9):
        row = []
        for x in range(1, 9):
            row.append(board[y][x])
        inner_board.append(row)
    
    quadrants = split_board_into_quadrants(inner_board)
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
    Generate a 10x10 board from 4 quadrants, including corners and borders
    
    Args:
        quadrants (List[List[List[str]]]): 4 quadrants to combine
    
    Returns:
        List[List[str]]: 10x10 board with corners and borders
    """
    board = [['BORDER' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    board[0][0] = 'CORNER'
    board[0][9] = 'CORNER'
    board[9][0] = 'CORNER'
    board[9][9] = 'CORNER'
    
    for i in range(2):
        for j in range(2):
            quadrant = quadrants[i * 2 + j]
            for y in range(4):
                for x in range(4):
                    board[i * 4 + 1 + y][j * 4 + 1 + x] = quadrant[y][x]
    
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

def create_random_board(rows=10, cols=10):
    """
    Create a completely random board with corners
    
    Args:
        rows (int): Number of rows (default 10)
        cols (int): Number of columns (default 10)
    
    Returns:
        List[List[str]]: Randomly generated 10x10 board
    """
    while True:
        quadrants = [generate_random_quadrant() for _ in range(4)]
        board = generate_board_from_quadrants(quadrants)
        if validate_board(board):
            return board

def draw_board(screen, fonts, board, draw_pieces=True):
    """
    Draw the game board on the screen
    
    Args:
        screen (pygame.Surface): Surface to draw on
        fonts (dict): Dictionary of fonts
        board (List[List[str]]): 10x10 board to draw
        draw_pieces (bool): Whether to draw game pieces (default True)
    
    Returns:
        List[List[str]]: The drawn board (for consistency)
    """
    if not board or not isinstance(board, list) or len(board) != BOARD_SIZE:
        raise ValueError(f"Invalid board: must be a {BOARD_SIZE}x{BOARD_SIZE} list of tile types")
    
    board_width = BOARD_SIZE * TILE_SIZE
    board_height = BOARD_SIZE * TILE_SIZE
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    board_x = (screen_width - board_width) // 2
    board_y = (screen_height - board_height) // 2

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            tile_type = str(board[y][x])
            
            tile_rect = pygame.Rect(
                board_x + x * TILE_SIZE,
                board_y + y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )

            if tile_type == 'CORNER':
                tile_image = pygame.transform.scale(COIN_IMAGE, (TILE_SIZE, TILE_SIZE))
            elif tile_type == 'BORDER':
                if y == 0 or y == 9:
                    tile_image = pygame.transform.scale(CONTOUR_IMAGE, (TILE_SIZE, TILE_SIZE))
                else:
                    tile_image = pygame.transform.rotate(
                        pygame.transform.scale(CONTOUR_IMAGE, (TILE_SIZE, TILE_SIZE)), 90)
            elif tile_type in TILE_IMAGES and tile_type in TILE_KEYS:
                tile_image = pygame.transform.scale(TILE_IMAGES[tile_type], (TILE_SIZE, TILE_SIZE))
            else:
                print(f"Warning: Unknown tile type {tile_type}. Using default.")
                tile_image = pygame.transform.scale(TILE_IMAGES['A'], (TILE_SIZE, TILE_SIZE))
            
            screen.blit(tile_image, tile_rect.topleft)
            pygame.draw.rect(screen, BLACK, tile_rect, 1)

    return board

def configure_board(screen, fonts):
    """
    Interactive board configuration interface with clickable corners
    
    Args:
        screen (pygame.Surface): Screen to draw on
        fonts (dict): Dictionary of fonts
    
    Returns:
        List[List[str]]: Configured 10x10 board with corners
    """
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    quadrants = [generate_random_quadrant() for _ in range(4)]
    rotations = [0, 0, 0, 0]

    quadrant_size = 4 * TILE_SIZE
    board_width = BOARD_SIZE * TILE_SIZE
    board_height = BOARD_SIZE * TILE_SIZE

    running = True

    while running:
        screen.fill(WHITE)

        title_text = fonts['title'].render(t("board_edit"), True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))

        instruction_text = fonts['small'].render(t("help_text"), True, BLACK)
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, 90))
        
        board_y = 170
        board_x = screen_width // 2 - board_width // 2

        current_board = generate_board_from_quadrants(
            [rotate_quadrant(quadrants[i], rotations[i]) for i in range(4)])
        
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                tile_type = current_board[y][x]
                tile_rect = pygame.Rect(
                    board_x + x * TILE_SIZE,
                    board_y + y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )
                
                if tile_type == 'CORNER':
                    tile_image = pygame.transform.scale(COIN_IMAGE, (TILE_SIZE, TILE_SIZE))
                elif tile_type == 'BORDER':
                    if y == 0 or y == 9:
                        tile_image = pygame.transform.scale(CONTOUR_IMAGE, (TILE_SIZE, TILE_SIZE))
                    else:
                        tile_image = pygame.transform.rotate(
                            pygame.transform.scale(CONTOUR_IMAGE, (TILE_SIZE, TILE_SIZE)), 90)
                else:
                    tile_image = pygame.transform.scale(TILE_IMAGES[tile_type], (TILE_SIZE, TILE_SIZE))
                
                screen.blit(tile_image, tile_rect.topleft)
                pygame.draw.rect(screen, BLACK, tile_rect, 1)

        for i in range(2):
            for j in range(2):
                quad_x = board_x + TILE_SIZE + j * quadrant_size
                quad_y = board_y + TILE_SIZE + i * quadrant_size
                pygame.draw.rect(screen, RED, (quad_x, quad_y, quadrant_size, quadrant_size), 2)

        # Boutons
        valid_button_y = board_y + board_height + 20
        valid_button = pygame.Rect(screen_width // 2 - 100, valid_button_y, 200, 50)
        edit_button = pygame.Rect(screen_width // 2 - 100, valid_button_y + 60, 200, 50)
        
        pygame.draw.rect(screen, GREEN, valid_button)
        pygame.draw.rect(screen, GREEN, edit_button)

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
                        quad_x = board_x + TILE_SIZE + j * quadrant_size
                        quad_y = board_y + TILE_SIZE + i * quadrant_size
                        rect = pygame.Rect(quad_x, quad_y, quadrant_size, quadrant_size)
                        if rect.collidepoint(mouse_x, mouse_y):
                            rotations[idx] = (rotations[idx] + 1) % 4

                corner_positions = [(0, 0), (0, 9), (9, 0), (9, 9)]
                for corner_y, corner_x in corner_positions:
                    corner_rect = pygame.Rect(
                        board_x + corner_x * TILE_SIZE,
                        board_y + corner_y * TILE_SIZE,
                        TILE_SIZE, TILE_SIZE
                    )
                    if corner_rect.collidepoint(mouse_x, mouse_y):
                        print(f"Coin cliqué : ({corner_y}, {corner_x})")

                if valid_button.collidepoint(mouse_x, mouse_y):
                    if validate_board(current_board):
                        return current_board

                if edit_button.collidepoint(mouse_x, mouse_y):
                    current_board = edit_board(screen, fonts, current_board)
                    return current_board

        pygame.display.flip()

def edit_board(screen, fonts, board):
    """
    Edit board interface for 10x10 board with corners
    """
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    working_board = [row.copy() for row in board]
    y_cursor, x_cursor = 1, 1

    running = True
    while running:
        screen.fill(WHITE)

        title_text = fonts['title'].render(t("board_edit"), True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))
        
        board_x = screen_width // 2 - (BOARD_SIZE * TILE_SIZE) // 2
        board_y = 100
        
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                tile_type = working_board[y][x]
                tile_rect = pygame.Rect(board_x + x * TILE_SIZE, board_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                if tile_type == 'CORNER':
                    tile_image = pygame.transform.scale(COIN_IMAGE, (TILE_SIZE, TILE_SIZE))
                elif tile_type == 'BORDER':
                    if y == 0 or y == 9:
                        tile_image = pygame.transform.scale(CONTOUR_IMAGE, (TILE_SIZE, TILE_SIZE))
                    else:
                        tile_image = pygame.transform.rotate(
                            pygame.transform.scale(CONTOUR_IMAGE, (TILE_SIZE, TILE_SIZE)), 90)
                elif tile_type in TILE_IMAGES and tile_type in TILE_KEYS:
                    tile_image = pygame.transform.scale(TILE_IMAGES[tile_type], (TILE_SIZE, TILE_SIZE))
                else:
                    tile_image = pygame.transform.scale(TILE_IMAGES['A'], (TILE_SIZE, TILE_SIZE))
                
                screen.blit(tile_image, tile_rect.topleft)
                pygame.draw.rect(screen, BLACK, tile_rect, 1)

        if 1 <= y_cursor <= 8 and 1 <= x_cursor <= 8:
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
                    x_cursor = min(8, x_cursor + 1)
                elif event.key == pygame.K_LEFT:
                    x_cursor = max(1, x_cursor - 1)
                elif event.key == pygame.K_DOWN:
                    y_cursor = min(8, y_cursor + 1)
                elif event.key == pygame.K_UP:
                    y_cursor = max(1, y_cursor - 1)
                elif event.key == pygame.K_SPACE:
                    if working_board[y_cursor][x_cursor] in TILE_KEYS:
                        current_index = TILE_KEYS.index(working_board[y_cursor][x_cursor])
                        next_index = (current_index + 1) % len(TILE_KEYS)
                        working_board[y_cursor][x_cursor] = TILE_KEYS[next_index]
                elif event.key == pygame.K_RETURN:
                    if validate_board(working_board):
                        return working_board

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                
                for y in range(1, 9):
                    for x in range(1, 9):
                        tile_rect = pygame.Rect(board_x + x * TILE_SIZE, board_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if tile_rect.collidepoint(mouse_x, mouse_y):
                            if working_board[y][x] in TILE_KEYS:
                                current_index = TILE_KEYS.index(working_board[y][x])
                                next_index = (current_index + 1) % len(TILE_KEYS)
                                working_board[y][x] = TILE_KEYS[next_index]

                corner_positions = [(0, 0), (0, 9), (9, 0), (9, 9)]
                for corner_y, corner_x in corner_positions:
                    corner_rect = pygame.Rect(
                        board_x + corner_x * TILE_SIZE,
                        board_y + corner_y * TILE_SIZE,
                        TILE_SIZE, TILE_SIZE
                    )
                    if corner_rect.collidepoint(mouse_x, mouse_y):
                        print(f"Coin cliqué en mode édition : ({corner_y}, {corner_x})")

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
        print(' '.join([str(cell)[:6].ljust(6) for cell in row]))

def board_to_quadrants(board):
    """
    Convert a full 10x10 board back to 8x8 inner board and then to quadrants
    
    Args:
        board (List[List[str]]): 10x10 board
    
    Returns:
        List[List[List[str]]]: 4 quadrants from the inner 8x8 area
    """
    inner_board = []
    for y in range(1, 9):
        row = []
        for x in range(1, 9):
            row.append(board[y][x])
        inner_board.append(row)
    
    return split_board_into_quadrants(inner_board)

def get_corner_owner(board, corner_pos):
    """
    Determine which player owns a corner based on its position
    
    Args:
        board (List[List[str]]): 10x10 board
        corner_pos (tuple): (y, x) position of the corner
    
    Returns:
        str: 'player1', 'player2', or 'neutral'
    """
    y, x = corner_pos
    if (y, x) == (0, 0) or (y, x) == (0, 9):
        return 'player1'
    elif (y, x) == (9, 0) or (y, x) == (9, 9):
        return 'player2'
    return 'neutral'

def is_corner_position(y, x):
    """
    Check if a position is a corner
    
    Args:
        y (int): Row position
        x (int): Column position
    
    Returns:
        bool: True if position is a corner
    """
    return (y, x) in [(0, 0), (0, 9), (9, 0), (9, 9)]

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
    'board_to_quadrants',
    'get_corner_owner',
    'is_corner_position'
]