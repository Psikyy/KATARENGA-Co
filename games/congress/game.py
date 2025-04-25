import pygame
import sys
from ui.colors import WHITE, BLACK, BLUE, RED, GREEN, HOVER_GREEN
from ui.buttons import draw_button, click_sound
from games.katarenga.board import BOARD_SIZE, TILE_SIZE, draw_board

class GameState:
    def __init__(self):
        self.board = None
        self.player1_pieces = []
        self.player2_pieces = []
        self.selected_piece = None
        self.current_player = 1
        self.valid_moves = []
        self.game_over = False
        self.winner = None

def get_valid_moves_for_piece(pos, board, all_pieces):
    x, y = pos
    tile_type = board[y][x]

    if tile_type == 'A':
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    elif tile_type == 'B':
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
    elif tile_type == 'C':
        directions = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
    elif tile_type == 'D':
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
    else:
        directions = []

    moves = []
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
            if (new_x, new_y) not in all_pieces:
                moves.append((new_x, new_y))
    return moves

def are_pieces_connected(pieces):
    if not pieces:
        return False
    visited = set()
    to_visit = [pieces[0]]

    while to_visit:
        x, y = to_visit.pop()
        visited.add((x, y))
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) in pieces and (nx, ny) not in visited:
                to_visit.append((nx, ny))
    return len(visited) == len(pieces)

def setup_initial_pieces():
    p1 = [(0, 1),(0,4),(1,7),(4,7),(7,6),(7,4),(3,0),(6,0)]
    p2 = [(1, 0),(4,0),(6,7),(3,7),(0,3),(0,6),(7,4),(7,1)]
    return p1, p2

def start_game(screen, fonts, player1_name, player2_name, selected_quadrants):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    game_state = GameState()
    game_state.board = draw_board(screen, fonts, selected_quadrants)

    board_width = BOARD_SIZE * TILE_SIZE
    board_height = BOARD_SIZE * TILE_SIZE
    board_x = (screen_width - board_width) // 2
    board_y = (screen_height - board_height) // 2

    game_state.player1_pieces, game_state.player2_pieces = setup_initial_pieces()
    help_text = fonts['small'].render("Formez un bloc connecté avec vos pièces !", True, BLACK)

    running = True
    while running:
        screen.fill(WHITE)

        title_text = fonts['title'].render("Katarenga - Mode Connexion", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))

        player1_text = fonts['small'].render(f"{player1_name} (Blanc)", True, BLACK)
        player2_text = fonts['small'].render(f"{player2_name} (Noir)", True, BLACK)
        screen.blit(player1_text, (50, 100))
        screen.blit(player2_text, (screen_width - 50 - player2_text.get_width(), 100))

        current_color = BLACK if game_state.current_player == 1 else (50, 50, 50)
        current_player_text = fonts['button'].render(
            f"Tour de {player1_name}" if game_state.current_player == 1 else f"Tour de {player2_name}",
            True, current_color)
        screen.blit(current_player_text, (screen_width // 2 - current_player_text.get_width() // 2, 100))

        screen.blit(help_text, (screen_width // 2 - help_text.get_width() // 2, 140))

        draw_board(screen, fonts, selected_quadrants)

        all_pieces = game_state.player1_pieces + game_state.player2_pieces
        piece_radius = TILE_SIZE // 3
        for x, y in game_state.player1_pieces:
            pygame.draw.circle(screen, WHITE, (board_x + x * TILE_SIZE + TILE_SIZE // 2, board_y + y * TILE_SIZE + TILE_SIZE // 2), piece_radius)
        for x, y in game_state.player2_pieces:
            pygame.draw.circle(screen, BLACK, (board_x + x * TILE_SIZE + TILE_SIZE // 2, board_y + y * TILE_SIZE + TILE_SIZE // 2), piece_radius)

        for move_x, move_y in game_state.valid_moves:
            pygame.draw.circle(screen, GREEN, (board_x + move_x * TILE_SIZE + TILE_SIZE // 2, board_y + move_y * TILE_SIZE + TILE_SIZE // 2), piece_radius // 2, 2)

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

                if game_state.game_over:
                    if 'new_game_button' in locals() and new_game_button.collidepoint(mouse_x, mouse_y):
                        if click_sound:
                            click_sound.play()
                        return
                else:
                    grid_x = (mouse_x - board_x) // TILE_SIZE
                    grid_y = (mouse_y - board_y) // TILE_SIZE
                    if 0 <= grid_x < BOARD_SIZE and 0 <= grid_y < BOARD_SIZE:
                        pos = (grid_x, grid_y)
                        player_pieces = game_state.player1_pieces if game_state.current_player == 1 else game_state.player2_pieces
                        opponent_pieces = game_state.player2_pieces if game_state.current_player == 1 else game_state.player1_pieces

                        if pos in player_pieces:
                            game_state.selected_piece = pos
                            game_state.valid_moves = get_valid_moves_for_piece(pos, game_state.board, player_pieces + opponent_pieces)
                        elif pos in game_state.valid_moves and game_state.selected_piece:
                            player_pieces.remove(game_state.selected_piece)
                            player_pieces.append(pos)
                            game_state.selected_piece = None
                            game_state.valid_moves = []

                            if are_pieces_connected(player_pieces):
                                game_state.game_over = True
                                game_state.winner = game_state.current_player
                            else:
                                game_state.current_player = 3 - game_state.current_player

        pygame.display.flip()
