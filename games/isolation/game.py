import pygame
import random
import sys
from ui.colors import WHITE, BLACK, BROWN, GREEN, HOVER_GREEN, BLUE, RED
from ui.buttons import draw_button, click_sound
from games.isolation.board import BOARD_SIZE, TILE_SIZE, draw_board
from menu.settings import t

class GameState:
    def __init__(self):
        self.board = None
        self.player1_pieces = []
        self.player2_pieces = []
        self.current_player = 1
        self.preview_pos = None
        self.game_over = False
        self.winner = None

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

def is_under_threat(x, y, board, all_pieces):
    for px, py in all_pieces:
        tile_type = board[py][px]

        if tile_type == 'A':  # Tour, arrêt sur première case rouge ou capture
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dx, dy in directions:
                step = 1
                while True:
                    new_x = px + dx * step
                    new_y = py + dy * step

                    if not (0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE):
                        break

                    if (new_x, new_y) in all_pieces:
                        break  # Bloqué

                    if (new_x, new_y) == (x, y):
                        return True

                    if board[new_y][new_x] == 'A':
                        break

                    step += 1

        elif tile_type == 'B':  # Diagonale, arrêt sur première case jaune ou capture
            directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
            for dx, dy in directions:
                step = 1
                while True:
                    new_x = px + dx * step
                    new_y = py + dy * step

                    if not (0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE):
                        break

                    if (new_x, new_y) in all_pieces:
                        break

                    if (new_x, new_y) == (x, y):
                        return True

                    if board[new_y][new_x] == 'B':
                        break

                    step += 1

        elif tile_type == 'C':  # Cavalier
            directions = [(1, 2), (2, 1), (2, -1), (1, -2),
                          (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
            for dx, dy in directions:
                if (px + dx, py + dy) == (x, y):
                    return True

        elif tile_type == 'D':  # Toutes directions
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                          (1, 1), (1, -1), (-1, -1), (-1, 1)]
            for dx, dy in directions:
                step = 1
                while True:
                    new_x = px + dx * step
                    new_y = py + dy * step

                    if not (0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE):
                        break

                    if (new_x, new_y) in all_pieces:
                        break

                    if (new_x, new_y) == (x, y):
                        return True

                    step += 1

    return False

def show_rules(screen, fonts):
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    running = True
    while running:
        screen.fill(WHITE)

        title_text = fonts['title'].render("Règles du jeu", True, BLACK)
        title_x = screen_width // 2 - title_text.get_width() // 2
        screen.blit(title_text, (title_x, 60))

        rules = [
            "Le plateau est initialement vide.",
            "Le jeu se joue à deux joueurs.",
            "",
            "À tour de rôle, chaque joueur place un de ses pions sur une case vide du plateau.",
            "Un pion ne peut être placé que s’il n’est pas en prise, c’est-à-dire :",
            "  - Il ne doit pas pouvoir être capturé par un pion déjà présent sur le plateau",
            "    (quelle que soit sa couleur), selon les règles de capture définies pour le jeu.",
            "",
            "Il n'y a aucun déplacement ni capture pendant la partie :",
            "  - Les pions restent sur la case où ils ont été posés.",
            "",
            "Le jeu continue tant que les joueurs peuvent poser des pions selon la règle ci-dessus.",
            "",
            "Le vainqueur est le dernier joueur à avoir pu poser un pion."
        ]

        line_spacing = 28
        total_height = len(rules) * line_spacing
        start_y = max(130, (screen_height - total_height) // 2)

        for i, line in enumerate(rules):
            is_indent = line.strip().startswith("-") or line.strip().startswith("•")
            font_color = BLACK
            font_used = fonts['small']
            rendered_text = font_used.render(line, True, font_color)
            x = screen_width // 2 - rendered_text.get_width() // 2 if not is_indent else screen_width // 2 - rendered_text.get_width() // 2 + 20
            y = start_y + i * line_spacing
            screen.blit(rendered_text, (x, y))

        back_button = draw_button(screen, fonts, "Retour", screen_width // 2 - 50, screen_height - 70, 100, 40, BLUE, RED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    return

        pygame.display.flip()


def get_legal_moves(board, all_pieces):
    legal = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if (x, y) not in all_pieces and not is_under_threat(x, y, board, all_pieces):
                legal.append((x, y))
    return legal

def start_game(screen, fonts, player1_name, player2_name, selected_quadrants, mode="local"):
    bot_player = 2 if mode == "bot" else None
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



        current_player_text = fonts['button'].render(
            f"Tour de {player1_name}" if game_state.current_player == 1 else f"Tour de {player2_name}",
            True,
            BLACK if game_state.current_player == 1 else BLACK
        )
        screen.blit(current_player_text, (screen_width // 2 - current_player_text.get_width() // 2, 100))
        screen.blit(help_text, (screen_width // 2 - help_text.get_width() // 2, 140))

        draw_board(screen, fonts, selected_quadrants)

        # Dessiner les pions
        for pos in game_state.player1_pieces:
            pygame.draw.circle(screen, WHITE, (board_x + pos[0]*TILE_SIZE + TILE_SIZE//2, board_y + pos[1]*TILE_SIZE + TILE_SIZE//2), TILE_SIZE//3)
        for pos in game_state.player2_pieces:
            pygame.draw.circle(screen, BROWN, (board_x + pos[0]*TILE_SIZE + TILE_SIZE//2, board_y + pos[1]*TILE_SIZE + TILE_SIZE//2), TILE_SIZE//3)

        all_pieces = game_state.player1_pieces + game_state.player2_pieces
        legal_moves = get_legal_moves(game_state.board, all_pieces)

        # Prévisualisation des coups possibles
        for (lx, ly) in legal_moves:
            color = (255, 100, 100, 100) if game_state.current_player == 1 else (100, 100, 255, 100)
            preview_circle = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(preview_circle, color, (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//4)
            screen.blit(preview_circle, (board_x + lx*TILE_SIZE, board_y + ly*TILE_SIZE))

        back_button = draw_button(screen, fonts, "Retour", 10, screen_height - 60, 100, 40, BROWN, WHITE)

        rules_button = draw_button(screen, fonts, t("rules"), screen_width - 110, screen_height - 60 , 100, 40, GREEN, HOVER_GREEN)

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
                
                if rules_button.collidepoint(mouse_x, mouse_y):
                    if click_sound:
                        click_sound.play()
                    show_rules(screen, fonts)
                

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
                            game_state.winner = next_player
                        # Si c'est le tour du bot, il joue automatiquement
                        if bot_player is not None and game_state.current_player == bot_player and not game_state.game_over:
                            pygame.time.wait(500)  # Petite pause pour voir le mouvement du bot
                            all_pieces = game_state.player1_pieces + game_state.player2_pieces
                            legal = get_legal_moves(game_state.board, all_pieces)

                            if bot_play(game_state, legal):
                                next_player = 3 - game_state.current_player
                                new_all_pieces = game_state.player1_pieces + game_state.player2_pieces
                                if get_legal_moves(game_state.board, new_all_pieces):
                                    game_state.current_player = next_player
                                else:
                                    game_state.game_over = True
                                    game_state.winner = next_player


        pygame.display.flip()

def bot_play(game_state, legal_moves):
    if not legal_moves:
        return False

    move = random.choice(legal_moves)

    if game_state.current_player == 2:
        game_state.player2_pieces.append(move)
    elif game_state.current_player == 1:
        game_state.player1_pieces.append(move)

    return True

