import pygame
import sys
from ui.colors import WHITE, BLACK, BLUE, RED, GREEN, HOVER_GREEN
from ui.buttons import draw_button, click_sound
from games.katarenga.board import BOARD_SIZE, TILE_SIZE, TILE_TYPES, draw_board
from collections import deque

# Nouvelle classe d’état du jeu avec plusieurs pions par joueur
class GameState:
    def __init__(self):
        self.board = None
        self.player1_pieces = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.player2_pieces = [(6, 6), (6, 7), (7, 6), (7, 7)]
        self.current_player = 1
        self.selected_piece = None
        self.valid_moves = []
        self.game_over = False
        self.winner = None

# Obtenir les mouvements valides pour un pion
def get_valid_moves(pos, board, all_positions):
    x, y = pos
    tile_type = board[y][x]
    directions = []

    if tile_type == 'A':
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    elif tile_type == 'B':
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
    elif tile_type == 'C':
        directions = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
    elif tile_type == 'D':
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]

    valid = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and (nx, ny) not in all_positions:
            valid.append((nx, ny))
    return valid

# Vérifie si tous les pions sont connectés orthogonalement
def is_connected(pieces):
    if not pieces:
        return False
    visited = set()
    queue = deque([pieces[0]])
    while queue:
        x, y = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) in pieces and (nx, ny) not in visited:
                queue.append((nx, ny))
    return len(visited) == len(pieces)

# Jeu principal
def start_game(screen, fonts, player1_name, player2_name, selected_quadrants):
    screen_width, screen_height = screen.get_width(), screen.get_height()
    game_state = GameState()
    game_state.board = draw_board(screen, fonts, selected_quadrants)

    board_width = BOARD_SIZE * TILE_SIZE
    board_height = BOARD_SIZE * TILE_SIZE
    board_x = (screen_width - board_width) // 2
    board_y = (screen_height - board_height) // 2

    help_text = fonts['small'].render("Sélectionnez un pion puis une case valide", True, BLACK)
    running = True

    while running:
        screen.fill(WHITE)

        # UI
        title_text = fonts['title'].render("Katarenga", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))

        player1_text = fonts['small'].render(f"{player1_name} (Rouge)", True, RED)
        player2_text = fonts['small'].render(f"{player2_name} (Bleu)", True, BLUE)
        screen.blit(player1_text, (50, 100))
        screen.blit(player2_text, (screen_width - 50 - player2_text.get_width(), 100))

        current_player_text = fonts['button'].render(
            f"Tour de {player1_name}" if game_state.current_player == 1 else f"Tour de {player2_name}",
            True,
            RED if game_state.current_player == 1 else BLUE
        )
        screen.blit(current_player_text, (screen_width // 2 - current_player_text.get_width() // 2, 100))
        screen.blit(help_text, (screen_width // 2 - help_text.get_width() // 2, 140))

        draw_board(screen, fonts, selected_quadrants)

        # Dessiner les pions
        for pos in game_state.player1_pieces:
            pygame.draw.circle(screen, RED, (board_x + pos[0]*TILE_SIZE + TILE_SIZE//2, board_y + pos[1]*TILE_SIZE + TILE_SIZE//2), TILE_SIZE//3)
        for pos in game_state.player2_pieces:
            pygame.draw.circle(screen, BLUE, (board_x + pos[0]*TILE_SIZE + TILE_SIZE//2, board_y + pos[1]*TILE_SIZE + TILE_SIZE//2), TILE_SIZE//3)

        # Mouvements valides
        for x, y in game_state.valid_moves:
            pygame.draw.circle(screen, GREEN, (board_x + x*TILE_SIZE + TILE_SIZE//2, board_y + y*TILE_SIZE + TILE_SIZE//2), TILE_SIZE//6, 2)

        # Surlignage du pion sélectionné
        if game_state.selected_piece:
            sel_x, sel_y = game_state.selected_piece
            pygame.draw.rect(screen, HOVER_GREEN, (board_x + sel_x*TILE_SIZE, board_y + sel_y*TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)

        back_button = draw_button(screen, fonts, "Retour", 10, screen_height - 60, 100, 40, BLUE, RED)

        if game_state.game_over:
            winner_name = player1_name if game_state.winner == 1 else player2_name
            winner_text = fonts['title'].render(f"{winner_name} a gagné !", True, BLACK)
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 200))
            screen.blit(overlay, (0, 0))
            screen.blit(winner_text, (screen_width // 2 - winner_text.get_width() // 2, screen_height // 2 - 50))
            new_game_button = draw_button(screen, fonts, "Nouvelle Partie", screen_width // 2 - 100, screen_height // 2 + 50, 200, 50, GREEN, HOVER_GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if back_button.collidepoint(mouse_x, mouse_y):
                    if click_sound:
                        click_sound.play()
                    return

                if game_state.game_over and 'new_game_button' in locals() and new_game_button.collidepoint(mouse_x, mouse_y):
                    if click_sound:
                        click_sound.play()
                    return

                if not game_state.game_over:
                    tile_x = (mouse_x - board_x) // TILE_SIZE
                    tile_y = (mouse_y - board_y) // TILE_SIZE

                    if 0 <= tile_x < BOARD_SIZE and 0 <= tile_y < BOARD_SIZE:
                        pos = (tile_x, tile_y)
                        current_pieces = game_state.player1_pieces if game_state.current_player == 1 else game_state.player2_pieces
                        opponent_pieces = game_state.player2_pieces if game_state.current_player == 1 else game_state.player1_pieces
                        all_pieces = current_pieces + opponent_pieces

                        if pos in current_pieces:
                            game_state.selected_piece = pos
                            game_state.valid_moves = get_valid_moves(pos, game_state.board, all_pieces)
                        elif game_state.selected_piece and pos in game_state.valid_moves:
                            if click_sound:
                                click_sound.play()

                            current_pieces.remove(game_state.selected_piece)
                            current_pieces.append(pos)
                            game_state.selected_piece = None
                            game_state.valid_moves = []

                            if is_connected(current_pieces):
                                game_state.game_over = True
                                game_state.winner = game_state.current_player
                            else:
                                game_state.current_player = 3 - game_state.current_player

        pygame.display.flip()
