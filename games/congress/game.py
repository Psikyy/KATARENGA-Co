import pygame
import random
import sys
from ui.colors import WHITE, BROWN, BLUE, RED, GREEN, HOVER_GREEN, BLACK
from ui.buttons import draw_button, click_sound
from games.congress.board import BOARD_SIZE, TILE_SIZE, draw_board
from menu.settings import t

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
    start_tile = tile_type

    if tile_type == 'A':
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        max_steps = BOARD_SIZE
    elif tile_type == 'B':
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        max_steps = BOARD_SIZE
    elif tile_type == 'C':
        knight_moves = [
            (1, 2), (2, 1), (2, -1), (1, -2),
            (-1, -2), (-2, -1), (-2, 1), (-1, 2)
        ]
        return [
            (x + dx, y + dy)
            for dx, dy in knight_moves
            if 0 <= x + dx < BOARD_SIZE and 0 <= y + dy < BOARD_SIZE
            and (x + dx, y + dy) not in all_pieces
        ]
    elif tile_type == 'D':
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (1, -1), (-1, -1), (-1, 1)]
        moves = []
        for dx, dy in directions:
            new_x = x + dx
            new_y = y + dy
            if (0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE and
                    (new_x, new_y) not in all_pieces):
                moves.append((new_x, new_y))
        return moves
    else:
        return []

    moves = []
    for dx, dy in directions:
        for step in range(1, max_steps):
            new_x = x + dx * step
            new_y = y + dy * step
            if not (0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE):
                break

            if (new_x, new_y) in all_pieces:
                break

            current_tile = board[new_y][new_x]
            moves.append((new_x, new_y))

            if current_tile == start_tile:
                break
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
    p1 = [(0, 1),(0,4),(1,7),(4,7),(7,6),(7,3),(3,0),(6,0)]
    p2 = [(1, 0),(4,0),(6,7),(3,7),(0,3),(0,6),(7,4),(7,1)]
    return p1, p2

def show_rules(screen, fonts):
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    running = True
    while running:
        screen.fill(WHITE)

        title_text = fonts['title'].render("Règles du Katarenga", True, BLACK)
        title_x = screen_width // 2 - title_text.get_width() // 2
        screen.blit(title_text, (title_x, 50))

        rules = [
            "Congress est un jeu de stratégie pour deux joueurs.",
            "Chaque joueur contrôle 8 pions qui se déplacent selon la case où ils se trouvent :",
            "",
            "Case Rouge : Mouvements orthogonaux (comme une tour aux échecs)",
            "Case Jaune : Mouvements diagonaux (comme un fou aux échecs)",
            "Case Vert : Mouvements en L (comme un cavalier aux échecs)",
            "Case Bleu : Mouvements dans toutes directions (comme une dame aux échecs)",
            "",
            "À tour de rôle, chaque joueur déplace l'un de ses pions selon les règles de déplacement ci-dessus.",
            "Les captures sont interdites.",
            "",
            "Le but du jeu est de réunir ses 8 pions sous la forme d'un bloc connecté.",
            "Un bloc connecté est un ensemble de pions du même joueur,",
            "où chaque pion est adjacent orthogonalement (haut, bas, gauche ou droite)",
            "à au moins un autre pion du même joueur.",
            "",
            "Le premier joueur à réussir cette formation gagne la partie.",
            "Si aucun joueur ne peut plus bouger et qu'aucun bloc connecté ne peut être formé,",
            "la partie est nulle.",
        ]

        line_spacing = 30
        total_height = len(rules) * line_spacing
        start_y = (screen_height - total_height) // 2

        for i, line in enumerate(rules):
            text_surface = fonts['small'].render(line, True, BLACK)
            x = screen_width // 2 - text_surface.get_width() // 2
            y = start_y + i * line_spacing
            screen.blit(text_surface, (x, y))

        back_button = draw_button(screen, fonts, "Retour", screen_width // 2 - 50, screen_height - 80, 100, 40, BLUE, RED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    return

        pygame.display.flip()


def start_game(screen, fonts, player1_name, player2_name, selected_quadrants, mode="local"):
    bot_player = 2 if mode == "bot" else None
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

        title_text = fonts['title'].render("Congress", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))

        player1_text = fonts['small'].render(f"{player1_name} (Blanc)", True, BLACK)
        player2_text = fonts['small'].render(f"{player2_name} (marron)", True, BLACK)
        screen.blit(player1_text, (50, 100))
        screen.blit(player2_text, (screen_width - 50 - player2_text.get_width(), 100))

        current_color = BROWN if game_state.current_player == 2 else BLACK
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
            pygame.draw.circle(screen, BROWN, (board_x + x * TILE_SIZE + TILE_SIZE // 2, board_y + y * TILE_SIZE + TILE_SIZE // 2), piece_radius)

        for move_x, move_y in game_state.valid_moves:
            pygame.draw.circle(screen, GREEN, (board_x + move_x * TILE_SIZE + TILE_SIZE // 2, board_y + move_y * TILE_SIZE + TILE_SIZE // 2), piece_radius // 2, 2)

        back_button = draw_button(screen, fonts, "Retour", 10, screen_height - 60, 100, 40, BLUE, RED)

        rules_button = draw_button(screen, fonts, t("rules"), screen_width - 110, screen_height - 60 , 100, 40, GREEN, HOVER_GREEN)

        if game_state.game_over:
            winner_name = player1_name if game_state.winner == 1 else player2_name
            winner_text = fonts['title'].render(f"{winner_name} a gagné !", True, BROWN)
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
                
                if rules_button.collidepoint(mouse_x, mouse_y):
                    if click_sound:
                        click_sound.play()
                    show_rules(screen, fonts)

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
                            if bot_player is not None and game_state.current_player == bot_player and not game_state.game_over:
                                pygame.time.wait(500)
                                bot_play(game_state)


        pygame.display.flip()


def bot_play(game_state):
    pieces = game_state.player2_pieces if game_state.current_player == 2 else game_state.player1_pieces
    opponent_pieces = game_state.player1_pieces if game_state.current_player == 2 else game_state.player2_pieces

    movable_pieces = []

    for piece in pieces:
        moves = get_valid_moves_for_piece(piece, game_state.board, pieces + opponent_pieces)
        if moves:
            movable_pieces.append((piece, moves))

    if not movable_pieces:
        return False

    selected_piece, moves = random.choice(movable_pieces)
    destination = random.choice(moves)

    pieces.remove(selected_piece)
    pieces.append(destination)

    if are_pieces_connected(pieces):
        game_state.game_over = True
        game_state.winner = game_state.current_player
    else:
        game_state.current_player = 3 - game_state.current_player

    return True