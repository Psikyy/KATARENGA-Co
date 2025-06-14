import pygame
import random
import sys
from ui.colors import WHITE, BLACK, BLUE, RED, GREEN, HOVER_GREEN, GRAY
from ui.buttons import draw_button, click_sound
from games.katarenga.board import BOARD_SIZE, TILE_SIZE, draw_board
from menu.settings import t


class GameState:
    def __init__(self):
        self.board = None
        self.player1_pieces = [(i, 1, None) for i in range(1, 9)]  
        self.player2_pieces = [(i, 8, None) for i in range(1, 9)]  
        self.current_player = 1
        self.valid_moves = {}
        self.game_over = False
        self.winner = None
        self.turn_count = 0
        self.selected_piece_idx = None
        self.player1_target_camps = [(0, 0), (9, 0)]
        self.player2_target_camps = [(0, 9), (9, 9)]
        self.base_line1 = [(i, 1) for i in range(1, 9)]
        self.base_line2 = [(i, 8) for i in range(1, 9)]


def get_adjacent_corners(x, y, target_camps):
    """
        Retourne les coins cibles adjacents à une position donnée.
        Pour Katarenga, depuis la ligne de base adverse, on peut aller aux coins adjacents.
    """
    adjacent_corners = []
    
    for corner_x, corner_y in target_camps:
        if (abs(x - corner_x) <= 2 and abs(y - corner_y) <= 2):
            adjacent_corners.append((corner_x, corner_y))
    
    return adjacent_corners


def get_valid_moves(game_state, board):
    valid_moves = {}

    if game_state.current_player == 1:
        player_pieces = game_state.player1_pieces
        opponent_pieces = game_state.player2_pieces
        enemy_camps = game_state.player2_target_camps
    else:
        player_pieces = game_state.player2_pieces
        opponent_pieces = game_state.player1_pieces
        enemy_camps = game_state.player1_target_camps

    opponent_positions = [(x, y) for x, y, in_camp in opponent_pieces if in_camp is None]

    for idx, (x, y, in_camp) in enumerate(player_pieces):
        if in_camp is not None:
            continue

        piece_moves = []

        for camp_x, camp_y in enemy_camps:
            diagonal_positions = [
                (camp_x - 1, camp_y - 1),  # diagonale haut-gauche
                (camp_x + 1, camp_y - 1),  # diagonale haut-droite
                (camp_x - 1, camp_y + 1),  # diagonale bas-gauche
                (camp_x + 1, camp_y + 1)   # diagonale bas-droite
            ]
            
            if (x, y) in diagonal_positions:
                camp_occupied = any(p_camp is not None and p_x == camp_x and p_y == camp_y 
                                  for p_x, p_y, p_camp in player_pieces)
                if not camp_occupied:
                    piece_moves.append((camp_x, camp_y, True))

        tile_type = board[y][x]
        directions = []

        if tile_type == 'A':
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dx, dy in directions:
                step = 1
                while True:
                    new_x = x + dx * step
                    new_y = y + dy * step
                    if not (0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE):
                        break

                    if (new_x, new_y) in [(0, 0), (0, 9), (9, 0), (9, 9)]:
                        break
                    else:
                        if not (1 <= new_x <= 8 and 1 <= new_y <= 8):
                            break

                    if any(px == new_x and py == new_y and pcamp is None 
                          for px, py, pcamp in player_pieces):
                        break

                    is_capture = (new_x, new_y) in opponent_positions
                    if game_state.turn_count == 0 and is_capture:
                        break

                    piece_moves.append((new_x, new_y, False))

                    if board[new_y][new_x] == 'A' or is_capture:
                        break

                    step += 1

        elif tile_type == 'B':
            directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
            for dx, dy in directions:
                step = 1
                while True:
                    new_x = x + dx * step
                    new_y = y + dy * step
                    if not (0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE):
                        break

                    if (new_x, new_y) in [(0, 0), (0, 9), (9, 0), (9, 9)]:
                        break
                    else:
                        if not (1 <= new_x <= 8 and 1 <= new_y <= 8):
                            break

                    if any(px == new_x and py == new_y and pcamp is None 
                          for px, py, pcamp in player_pieces):
                        break

                    is_capture = (new_x, new_y) in opponent_positions
                    if game_state.turn_count == 0 and is_capture:
                        break

                    piece_moves.append((new_x, new_y, False))

                    if board[new_y][new_x] == 'B' or is_capture:
                        break

                    step += 1

        elif tile_type == 'C':
            directions = [(1, 2), (2, 1), (2, -1), (1, -2),
                          (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

        elif tile_type == 'D':
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                          (1, 1), (1, -1), (-1, -1), (-1, 1)]

        else:
            continue

        if tile_type in ['C', 'D']:
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if not (0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE):
                    continue

                if (new_x, new_y) in [(0, 0), (0, 9), (9, 0), (9, 9)]:
                    continue
                elif not (1 <= new_x <= 8 and 1 <= new_y <= 8):
                    continue

                if any(p_x == new_x and p_y == new_y and p_camp is None 
                      for p_x, p_y, p_camp in player_pieces):
                    continue

                is_capture = (new_x, new_y) in opponent_positions
                if game_state.turn_count == 0 and is_capture:
                    continue

                piece_moves.append((new_x, new_y, False))

        if piece_moves:
            valid_moves[idx] = piece_moves

    return valid_moves


def check_win(game_state):
    player1_captured_camps = set()
    player2_captured_camps = set()
    
    for x, y, in_camp in game_state.player1_pieces:
        if in_camp is not None:
            if (x, y) in game_state.player2_target_camps:
                if (x, y) == game_state.player2_target_camps[0]:
                    player1_captured_camps.add(0)
                elif (x, y) == game_state.player2_target_camps[1]:
                    player1_captured_camps.add(1)
    
    for x, y, in_camp in game_state.player2_pieces:
        if in_camp is not None:
            if (x, y) in game_state.player1_target_camps:
                if (x, y) == game_state.player1_target_camps[0]:
                    player2_captured_camps.add(0)
                elif (x, y) == game_state.player1_target_camps[1]:
                    player2_captured_camps.add(1)
    
    if len(player1_captured_camps) == 2:
        game_state.winner = 1
        return True
    
    if len(player2_captured_camps) == 2:
        game_state.winner = 2
        return True
    
    remaining_pieces1 = sum(1 for x, y, in_camp in game_state.player1_pieces if in_camp is None)
    remaining_pieces2 = sum(1 for x, y, in_camp in game_state.player2_pieces if in_camp is None)
    
    total_pieces1 = len(game_state.player1_pieces)
    total_pieces2 = len(game_state.player2_pieces)
    
    if total_pieces1 < 2:
        game_state.winner = 2
        return True
    
    if total_pieces2 < 2:
        game_state.winner = 1
        return True
    
    if len(game_state.valid_moves) == 0:
        game_state.winner = 3 - game_state.current_player  
        return True
    
    return False


def show_rules(screen, fonts):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    running = True
    while running:
        screen.fill(WHITE)
        
        title_text = fonts['title'].render(t("K's_rules"), True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))
        rules = t("K's_Rules")
        total_height = len(rules) * 30
        start_y = max(150, (screen_height - total_height) // 2 - 50)
        
        for i, rule in enumerate(rules):
            rule_text = fonts['small'].render(rule, True, BLACK)
            screen.blit(rule_text, (screen_width // 2 - rule_text.get_width() // 2, start_y + i * 30))
        
        back_button = draw_button(screen, fonts, t("back"), screen_width // 2 - 50, screen_height - 100, 100, 40, BLUE, RED)
        
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


def start_game(screen, fonts, player1_name, player2_name, board, mode='local'):
    """
        Démarre une partie de Katarenga
    : screen : l'écran Pygame sur lequel dessiner
    : fonts : un dictionnaire de polices de caractères
    : player1_name : le nom du joueur 1
    : player2_name : le nom du joueur 2
    : board : la configuration initiale du plateau de jeu
    : mode : le mode de jeu (local, bot, etc.)
    """
    bot_player = 2 if mode == "bot" else None
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    print(board)
    
    game_state = GameState()
    
    game_state.board = draw_board(screen, fonts, board, draw_pieces=False)
    
    board_width = BOARD_SIZE * TILE_SIZE
    board_height = BOARD_SIZE * TILE_SIZE
    board_x = (screen_width - board_width) // 2
    board_y = (screen_height - board_height) // 2
    
    game_state.valid_moves = get_valid_moves(game_state, game_state.board)
    
    help_text = fonts['small'].render(t("K's_help"), True, BLACK)
    
    running = True
   
    while running:
        screen.fill(WHITE)
        
        title_text = fonts['title'].render("Katarenga", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))

        
        current_player_name = player1_name if game_state.current_player == 1 else player2_name
        current_player_color = BLACK if game_state.current_player == 1 else GRAY
        
        turn_indicator = fonts['button'].render(
            t("turn") + current_player_name,
            True,
            current_player_color
        )
        screen.blit(turn_indicator, (screen_width // 2 - turn_indicator.get_width() // 2, screen_height - 60))
        
        screen.blit(help_text, (screen_width // 2 - help_text.get_width() // 2, 100))
        
        draw_board(screen, fonts, board, draw_pieces=False)
        
        piece_radius = TILE_SIZE // 3
        
        for idx, (x, y, in_camp) in enumerate(game_state.player1_pieces):
            if in_camp is None:  
                pygame.draw.circle(screen, BLACK, (
                    board_x + x * TILE_SIZE + TILE_SIZE // 2,
                    board_y + y * TILE_SIZE + TILE_SIZE // 2
                ), piece_radius)
            else:  
                pygame.draw.circle(screen, BLACK, (
                    board_x + x * TILE_SIZE + TILE_SIZE // 2,
                    board_y + y * TILE_SIZE + TILE_SIZE // 2
                ), piece_radius)
        
        for idx, (x, y, in_camp) in enumerate(game_state.player2_pieces):
            if in_camp is None:  
                pygame.draw.circle(screen, WHITE, (
                    board_x + x * TILE_SIZE + TILE_SIZE // 2,
                    board_y + y * TILE_SIZE + TILE_SIZE // 2
                ), piece_radius)
                pygame.draw.circle(screen, BLACK, (
                    board_x + x * TILE_SIZE + TILE_SIZE // 2,
                    board_y + y * TILE_SIZE + TILE_SIZE // 2
                ), piece_radius, 1)
            else:  
                pygame.draw.circle(screen, WHITE, (
                    board_x + x * TILE_SIZE + TILE_SIZE // 2,
                    board_y + y * TILE_SIZE + TILE_SIZE // 2
                ), piece_radius)
                pygame.draw.circle(screen, BLACK, (
                    board_x + x * TILE_SIZE + TILE_SIZE // 2,
                    board_y + y * TILE_SIZE + TILE_SIZE // 2
                ), piece_radius, 1)
        
        if game_state.selected_piece_idx is not None:
            if game_state.current_player == 1:
                selected_piece = game_state.player1_pieces[game_state.selected_piece_idx]
            else:
                selected_piece = game_state.player2_pieces[game_state.selected_piece_idx]
            
            if selected_piece[2] is None:  
                x, y, _ = selected_piece
                pygame.draw.circle(screen, RED, (
                    board_x + x * TILE_SIZE + TILE_SIZE // 2,
                    board_y + y * TILE_SIZE + TILE_SIZE // 2
                ), piece_radius + 3, 2)
        
        if game_state.selected_piece_idx is not None and game_state.selected_piece_idx in game_state.valid_moves:
            for move_x, move_y, is_camp_move in game_state.valid_moves[game_state.selected_piece_idx]:
                pygame.draw.circle(screen, GREEN, (
                    board_x + move_x * TILE_SIZE + TILE_SIZE // 2,
                    board_y + move_y * TILE_SIZE + TILE_SIZE // 2
                ), piece_radius // 2, 2)
        
        back_button = draw_button(screen, fonts, t("back"), 10, screen_height - 60, 100, 40, BLUE, RED)
        
        rules_button = draw_button(screen, fonts, t("rules"), screen_width - 110, screen_height - 60 , 100, 40, GREEN, HOVER_GREEN)

        
        if game_state.game_over:
            winner_name = player1_name if game_state.winner == 1 else player2_name
            winner_text = fonts['title'].render(f"{winner_name}" + t("win"), True, BLACK)
            
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 200))
            screen.blit(overlay, (0, 0))
            
            screen.blit(winner_text, (screen_width // 2 - winner_text.get_width() // 2, screen_height // 2 - 50))
            
            new_game_button = draw_button(screen, fonts, t("new_game"), screen_width // 2 - 100, screen_height // 2 + 50, 200, 50, GREEN, HOVER_GREEN)
        
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
                    tile_x = (mouse_x - board_x) // TILE_SIZE
                    tile_y = (mouse_y - board_y) // TILE_SIZE
                    
                    if 0 <= tile_x < BOARD_SIZE and 0 <= tile_y < BOARD_SIZE:
                        if game_state.selected_piece_idx is not None:
                            move_made = False
                            
                            if game_state.selected_piece_idx in game_state.valid_moves:
                                for move_x, move_y, is_camp_move in game_state.valid_moves[game_state.selected_piece_idx]:
                                    if (move_x, move_y) == (tile_x, tile_y):
                                        if click_sound:
                                            click_sound.play()
                                        
                                        if game_state.current_player == 1:
                                            for idx, (p_x, p_y, p_camp) in enumerate(game_state.player2_pieces):
                                                if p_camp is None and (p_x, p_y) == (tile_x, tile_y):
                                                    game_state.player2_pieces.pop(idx)
                                                    break
                                            
                                            if is_camp_move:
                                                camp_idx = 1 if (tile_x, tile_y) == game_state.player1_target_camps[0] else 2
                                                game_state.player1_pieces[game_state.selected_piece_idx] = (tile_x, tile_y, camp_idx)
                                            else:
                                                game_state.player1_pieces[game_state.selected_piece_idx] = (tile_x, tile_y, None)
                                        else:
                                            for idx, (p_x, p_y, p_camp) in enumerate(game_state.player1_pieces):
                                                if p_camp is None and (p_x, p_y) == (tile_x, tile_y):
                                                    game_state.player1_pieces.pop(idx)
                                                    break
                                            
                                            if is_camp_move:
                                                camp_idx = 1 if (tile_x, tile_y) == game_state.player2_target_camps[0] else 2
                                                game_state.player2_pieces[game_state.selected_piece_idx] = (tile_x, tile_y, camp_idx)
                                            else:
                                                game_state.player2_pieces[game_state.selected_piece_idx] = (tile_x, tile_y, None)
                                        
                                        move_made = True
                                        break
                            
                            if move_made:
                                game_state.turn_count += 1
                                
                                game_state.selected_piece_idx = None
                                
                                if check_win(game_state):
                                    game_state.game_over = True
                                else:
                                    game_state.current_player = 3 - game_state.current_player  
                                    
                                    game_state.valid_moves = get_valid_moves(game_state, game_state.board)

                                    if bot_player is not None and game_state.current_player == bot_player and not game_state.game_over:
                                        pygame.time.wait(500)  
                                        bot_play(game_state)

                                        if check_win(game_state):
                                            game_state.game_over = True
                                        else:
                                            game_state.current_player = 3 - game_state.current_player
                                            game_state.valid_moves = get_valid_moves(game_state, game_state.board)

                                    
                                    if not game_state.valid_moves:
                                        game_state.game_over = True
                                        game_state.winner = 3 - game_state.current_player
                            else:
                                game_state.selected_piece_idx = None
                        else:
                            if game_state.current_player == 1:
                                for idx, (p_x, p_y, p_camp) in enumerate(game_state.player1_pieces):
                                    if p_camp is None and (p_x, p_y) == (tile_x, tile_y):
                                        if click_sound:
                                            click_sound.play()
                                        game_state.selected_piece_idx = idx
                                        break
                            else:
                                for idx, (p_x, p_y, p_camp) in enumerate(game_state.player2_pieces):
                                    if p_camp is None and (p_x, p_y) == (tile_x, tile_y):
                                        if click_sound:
                                            click_sound.play()
                                        game_state.selected_piece_idx = idx
                                        break
        
        pygame.display.flip()


def bot_play(game_state):
    """
        Fonction pour jouer un coup pour le bot
    : game_state : l'état actuel du jeu
    """
    valid_moves = game_state.valid_moves

    if not valid_moves:
        return False  

    piece_idx = random.choice(list(valid_moves.keys()))

    move_x, move_y, is_camp_move = random.choice(valid_moves[piece_idx])

    if game_state.current_player == 2:
        for idx, (p_x, p_y, p_camp) in enumerate(game_state.player1_pieces):
            if p_camp is None and (p_x, p_y) == (move_x, move_y):
                game_state.player1_pieces.pop(idx)
                break

        if is_camp_move:
            camp_idx = 1 if (move_x, move_y) == game_state.player2_target_camps[0] else 2
            game_state.player2_pieces[piece_idx] = (move_x, move_y, camp_idx)
        else:
            game_state.player2_pieces[piece_idx] = (move_x, move_y, None)

    return True