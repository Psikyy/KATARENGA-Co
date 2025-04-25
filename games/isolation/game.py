import pygame
import sys
from ui.colors import WHITE, BLACK, BLUE, RED, GREEN, HOVER_GREEN
from ui.buttons import draw_button, click_sound
from games.katarenga.board import BOARD_SIZE, TILE_SIZE, TILE_TYPES, draw_board

# Nouvelle classe d’état du jeu pour la variante "pose uniquement"
class GameState:
    def __init__(self):
        self.board = None
        self.player1_pieces = []
        self.player2_pieces = []
        self.current_player = 1
        self.preview_pos = None
        self.game_over = False
        self.winner = None

# Obtenir les directions d’attaque en fonction du type de case
def get_attack_directions(tile_type):
    if tile_type == 'A':
        return [(0, 1), (1, 0), (0, -1), (-1, 0)]
    elif tile_type == 'B':
        return [(1, 1), (1, -1), (-1, -1), (-1, 1)]
    elif tile_type == 'C':
        return [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
    elif tile_type == 'D':
        return [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
    return []

# Vérifie si un pion posé en (x, y) serait en prise
def is_under_threat(x, y, board, all_pieces):
    for px, py in all_pieces:
        tile_type = board[py][px]
        directions = get_attack_directions(tile_type)
        for dx, dy in directions:
            if px + dx == x and py + dy == y:
                return True
    return False

# Récupère toutes les positions jouables pour le joueur courant
def get_legal_moves(board, all_pieces):
    legal = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if (x, y) not in all_pieces and not is_under_threat(x, y, board, all_pieces):
                legal.append((x, y))
    return legal

# Jeu principal pour la variante "pose uniquement"
def start_game(screen, fonts, player1_name, player2_name, selected_quadrants):
    screen_width, screen_height = screen.get_width(), screen.get_height()
    game_state = GameState()
    game_state.board = draw_board(screen, fonts, selected_quadrants)

    board_width = BOARD_SIZE * TILE_SIZE
    board_height = BOARD_SIZE * TILE_SIZE
    board_x = (screen_width - board_width) // 2
    board_y = (screen_height - board_height) // 2

    help_text = fonts['small'].render("Posez un pion sur une case non menacée", True, BLACK)
    running = True

    while running:
        screen.fill(WHITE)

        title_text = fonts['title'].render("Katarenga - Variante Pose", True, BLACK)
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

        all_pieces = game_state.player1_pieces + game_state.player2_pieces
        legal_moves = get_legal_moves(game_state.board, all_pieces)

        # Prévisualisation des coups possibles
        for (lx, ly) in legal_moves:
            color = (255, 100, 100, 100) if game_state.current_player == 1 else (100, 100, 255, 100)
            preview_circle = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(preview_circle, color, (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//4)
            screen.blit(preview_circle, (board_x + lx*TILE_SIZE, board_y + ly*TILE_SIZE))

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

            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                tile_x = (mouse_x - board_x) // TILE_SIZE
                tile_y = (mouse_y - board_y) // TILE_SIZE
                if 0 <= tile_x < BOARD_SIZE and 0 <= tile_y < BOARD_SIZE:
                    game_state.preview_pos = (tile_x, tile_y)
                else:
                    game_state.preview_pos = None

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
                    pos = (tile_x, tile_y)

                    if pos in legal_moves:
                        if click_sound:
                            click_sound.play()

                        if game_state.current_player == 1:
                            game_state.player1_pieces.append(pos)
                        else:
                            game_state.player2_pieces.append(pos)

                        # Vérifie si l’adversaire peut encore jouer
                        next_player = 3 - game_state.current_player
                        new_all_pieces = game_state.player1_pieces + game_state.player2_pieces
                        if get_legal_moves(game_state.board, new_all_pieces):
                            game_state.current_player = next_player
                        else:
                            game_state.game_over = True
                            game_state.winner = game_state.current_player

        pygame.display.flip()
