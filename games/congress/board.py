import pygame
import random
import sys
import os
from ui.colors import WHITE, BLACK, GREEN, HOVER_GREEN
from ui.buttons import draw_button, click_sound

TILE_IMAGES = {
    'A': pygame.image.load(os.path.join("design_case", "rouge_sans_blanc.png")),
    'B': pygame.image.load(os.path.join("design_case", "jaune_sans_blanc.png")),
    'C': pygame.image.load(os.path.join("design_case", "vert_sans_blanc.png")),
    'D': pygame.image.load(os.path.join("design_case", "bleu_sans_blanc.png")),
}

CONTOUR_IMAGE = pygame.image.load(os.path.join("design_case", "contour.png"))
COIN_IMAGE = pygame.image.load(os.path.join("design_case", "coin.png"))

BOARD_SIZE = 8
TILE_SIZE = 55
TILE_KEYS = ['A', 'B', 'C', 'D']

def generate_random_board():
    return [[random.choice(TILE_KEYS) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def generate_board_from_quadrants(quadrants):
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for i in range(2):
        for j in range(2):
            quadrant = quadrants[i * 2 + j]
            for y in range(4):
                for x in range(4):
                    board[i * 4 + y][j * 4 + x] = quadrant[y][x]
    return board

def generate_random_quadrant():
    return [[random.choice(TILE_KEYS) for _ in range(4)] for _ in range(4)]

def rotate_quadrant(quadrant, rotations=1):
    for _ in range(rotations):
        quadrant = [list(row) for row in zip(*quadrant[::-1])]
    return quadrant

def draw_borders_and_corners(screen, board_x, board_y, board_width, board_height):
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

def draw_board(screen, fonts, selected_quadrants=None, draw_pieces=True):
    board_width = BOARD_SIZE * TILE_SIZE
    board_height = BOARD_SIZE * TILE_SIZE
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    board_x = (screen_width - board_width) // 2
    board_y = (screen_height - board_height) // 2

    board = generate_board_from_quadrants(selected_quadrants) if selected_quadrants else generate_random_board()
    draw_borders_and_corners(screen, board_x, board_y, board_width, board_height)

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            tile_type = board[y][x]
            tile_rect = pygame.Rect(
                board_x + x * TILE_SIZE,
                board_y + y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
            tile_image = pygame.transform.scale(TILE_IMAGES[tile_type], (TILE_SIZE, TILE_SIZE))
            screen.blit(tile_image, tile_rect.topleft)
            pygame.draw.rect(screen, BLACK, tile_rect, 1)

    return board

def configure_board(screen, fonts):
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

        title_text = fonts['title'].render("Configuration du plateau", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))

        instruction_text = fonts['small'].render("Cliquez sur un quadrant pour le faire pivoter", True, BLACK)
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, 90))

        # --- ESPACEMENT AJOUTÉ ICI ---
        board_y = 140  # Anciennement 160 → réduit l'espace entre le texte et le plateau
        board_y += 30  # Ajoute un espacement supplémentaire
        board_x = screen_width // 2 - quadrant_size

        draw_borders_and_corners(screen, board_x, board_y, board_width, board_height)

        for i in range(2):
            for j in range(2):
                quadrant_index = i * 2 + j
                quadrant = rotate_quadrant(quadrants[quadrant_index], rotations[quadrant_index])

                quadrant_x = board_x + j * quadrant_size
                quadrant_y = board_y + i * quadrant_size

                for y in range(4):
                    for x in range(4):
                        tile_type = quadrant[y][x]
                        tile_rect = pygame.Rect(
                            quadrant_x + x * TILE_SIZE,
                            quadrant_y + y * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE
                        )
                        tile_image = pygame.transform.scale(TILE_IMAGES[tile_type], (TILE_SIZE, TILE_SIZE))
                        screen.blit(tile_image, tile_rect.topleft)
                        pygame.draw.rect(screen, BLACK, tile_rect, 1)

                pygame.draw.rect(screen, BLACK, (
                    quadrant_x,
                    quadrant_y,
                    quadrant_size,
                    quadrant_size
                ), 2)

        # --- ESPACEMENT AJOUTÉ ICI ---
        valid_button_y = board_y + board_height + 70  # Anciennement +50 → plus d'espace en dessous
        valid_button = draw_button(screen, fonts, "Valider", screen_width // 2 - 100, valid_button_y, 200, 50, GREEN, HOVER_GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

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

                if valid_button.collidepoint(mouse_x, mouse_y):
                    if click_sound:
                        click_sound.play()
                    rotated_quadrants = [rotate_quadrant(quadrants[i], rotations[i]) for i in range(4)]
                    return rotated_quadrants

        pygame.display.flip()
