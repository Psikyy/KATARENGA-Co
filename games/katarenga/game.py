import pygame
import random
import sys
from ui.colors import WHITE, BLACK, BLUE, RED, GREEN, HOVER_GREEN
from ui.buttons import draw_button, click_sound
from games.katarenga.board import BOARD_SIZE, TILE_SIZE, draw_board


# Positions des pièces sur le plateau
class GameState:
    def __init__(self):
        self.board = None
        # Chaque joueur a 8 pions, stockés comme des tuples (x, y, in_camp)
        # où in_camp est None si le pion n'est pas dans un camp, ou 1 ou 2 pour indiquer le camp
        self.player1_pieces = [(i, 0, None) for i in range(8)]  # Pions du joueur 1 (Noir)
        self.player2_pieces = [(i, 7, None) for i in range(8)]  # Pions du joueur 2 (Blanc)
        self.current_player = 1    # Joueur 1 commence
        self.valid_moves = {}      # Dictionnaire: {pion_index: [mouvements valides]}
        self.game_over = False     # Indique si le jeu est terminé
        self.winner = None         # Indique le vainqueur (1 ou 2)
        self.turn_count = 0        # Compte les tours pour savoir si c'est le premier tour
        self.selected_piece_idx = None  # Indice du pion sélectionné
        
        # Définir les positions des camps et des lignes de base
        self.camp1_positions = [(0, 0), (7, 0)]  # Camps du joueur 1 (Noir)
        self.camp2_positions = [(0, 7), (7, 7)]  # Camps du joueur 2 (Blanc)
        self.base_line1 = [(i, 0) for i in range(8)]  # Ligne de base du joueur 1
        self.base_line2 = [(i, 7) for i in range(8)]  # Ligne de base du joueur 2

# Obtenir les mouvements valides pour un joueur
def get_valid_moves(game_state, board):
    valid_moves = {}
    
    if game_state.current_player == 1:
        player_pieces = game_state.player1_pieces
        opponent_pieces = game_state.player2_pieces
        opponent_base_line = game_state.base_line2
        opponent_camps = game_state.camp2_positions
    else:
        player_pieces = game_state.player2_pieces
        opponent_pieces = game_state.player1_pieces
        opponent_base_line = game_state.base_line1
        opponent_camps = game_state.camp1_positions
    
    # Position des pions adverses (pour vérifier les captures)
    opponent_positions = [(x, y) for x, y, in_camp in opponent_pieces if in_camp is None]
    
    # Pour chaque pion du joueur actuel qui n'est pas dans un camp
    for idx, (x, y, in_camp) in enumerate(player_pieces):
        if in_camp is not None:
            continue  # Ignorer les pions déjà dans un camp
        
        piece_moves = []
        
        # Si le pion est sur la ligne de base adverse, il peut rejoindre un camp
        if (x, y) in opponent_base_line:
            for camp_x, camp_y in opponent_camps:
                # Vérifier si le camp est libre
                camp_occupied = False
                for p_idx, (p_x, p_y, p_camp) in enumerate(player_pieces):
                    if p_camp is not None and p_x == camp_x and p_y == camp_y:
                        camp_occupied = True
                        break
                
                if not camp_occupied:
                    piece_moves.append((camp_x, camp_y, True))  # True indique un mouvement spécial vers un camp
            
        # Mouvements normaux selon le type de case
        tile_type = board[y][x]
        
        # Mouvements selon le type de case
        if tile_type == 'A':  # Case rouge : tour avec arrêt sur la première case rouge
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dx, dy in directions:
                step = 1
                while True:
                    new_x = x + dx * step
                    new_y = y + dy * step
                    if not (0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE):
                        break  # Hors du plateau

                    # Vérifie si une pièce alliée bloque
                    if any(px == new_x and py == new_y and pcamp is None for px, py, pcamp in player_pieces):
                        break  # Bloqué par un allié

                    is_capture = (new_x, new_y) in opponent_positions
                    if game_state.turn_count == 0 and is_capture:
                        break  # Interdit de capturer au premier tour

                    piece_moves.append((new_x, new_y, False))

                    # Si on tombe sur une autre case rouge, on s'arrête
                    if board[new_y][new_x] == 'A':
                        break

                    # Si c’est une capture, on s’arrête aussi
                    if is_capture:
                        break

                    step += 1

        elif tile_type == 'B':  # Diagonale spéciale : "comme un fou", arrêt sur première case jaune
            directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
            for dx, dy in directions:
                step = 1
                while True:
                    new_x = x + dx * step
                    new_y = y + dy * step
                    if not (0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE):
                        break  # Hors du plateau

                    # Vérifie si une pièce alliée bloque
                    if any(px == new_x and py == new_y and pcamp is None for px, py, pcamp in player_pieces):
                        break  # Bloqué par un allié

                    is_capture = (new_x, new_y) in opponent_positions
                    if game_state.turn_count == 0 and is_capture:
                        break  # Interdit de capturer au premier tour

                    # Ajoute le mouvement valide
                    piece_moves.append((new_x, new_y, False))

                    # Si la case atteinte est aussi une case 'B' (jaune), on s’arrête là
                    if board[new_y][new_x] == 'B':
                        break

                    # Si c'est une capture, on s'arrête aussi
                    if is_capture:
                        break

                    step += 1
        elif tile_type == 'C':  # Cavalier
            directions = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        elif tile_type == 'D':  # Toutes directions
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
        
        # Vérifier les mouvements possibles
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            # Vérifier si la nouvelle position est dans le plateau
            if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                # Vérifier si la case est occupée par un pion ami
                occupied_by_friend = False
                for p_x, p_y, p_camp in player_pieces:
                    if p_camp is None and (p_x, p_y) == (new_x, new_y):
                        occupied_by_friend = True
                        break
                
                if not occupied_by_friend:
                    # Vérifier si c'est une capture
                    is_capture = (new_x, new_y) in opponent_positions
                    
                    # Au premier tour, pas de capture autorisée
                    if game_state.turn_count == 0 and is_capture:
                        continue
                    
                    piece_moves.append((new_x, new_y, False))  # False indique un mouvement normal
        
        if piece_moves:
            valid_moves[idx] = piece_moves
    
    return valid_moves

# Vérifier si un joueur a gagné
def check_win(game_state):
    # Victoire si un joueur occupe les deux camps adverses
    camps1_occupied = 0
    camps2_occupied = 0
    
    for _, _, in_camp in game_state.player1_pieces:
        if in_camp is not None:
            camps2_occupied += 1
    
    for _, _, in_camp in game_state.player2_pieces:
        if in_camp is not None:
            camps1_occupied += 1
    
    # Si le joueur 1 occupe les deux camps adverses, il gagne
    if camps2_occupied == 2:
        game_state.winner = 1
        return True
    
    # Si le joueur 2 occupe les deux camps adverses, il gagne
    if camps1_occupied == 2:
        game_state.winner = 2
        return True
    
    # Si un joueur n'a plus de pions ou ne peut plus bouger, il perd
    remaining_pieces1 = sum(1 for x, y, in_camp in game_state.player1_pieces if in_camp is None)
    remaining_pieces2 = sum(1 for x, y, in_camp in game_state.player2_pieces if in_camp is None)
    
    # Si le joueur 1 n'a plus assez de pions pour gagner
    if remaining_pieces1 == 0 or (remaining_pieces1 < 2 and camps2_occupied < 2):
        game_state.winner = 2
        return True
    
    # Si le joueur 2 n'a plus assez de pions pour gagner
    if remaining_pieces2 == 0 or (remaining_pieces2 < 2 and camps1_occupied < 2):
        game_state.winner = 1
        return True
    
    # Vérifier si un joueur ne peut plus se déplacer
    if len(game_state.valid_moves) == 0:
        game_state.winner = 3 - game_state.current_player  # Le joueur adverse gagne
        return True
    
    return False

# Afficher les règles du jeu
def show_rules(screen, fonts):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    running = True
    while running:
        screen.fill(WHITE)
        
        # Titre
        title_text = fonts['title'].render("Règles du Katarenga", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))
        
        # Règles
        rules = [
            "Katarenga est un jeu de stratégie pour deux joueurs.",
            "Chaque joueur contrôle 8 pions qui se déplacent selon la case où ils se trouvent:",
            "",
            "Case A (Gris clair): Mouvements orthogonaux (comme une tour aux échecs)",
            "Case B (Marron): Mouvements diagonaux (comme un fou aux échecs)",
            "Case C (Vert): Mouvements en L (comme un cavalier aux échecs)",
            "Case D (Bleu acier): Mouvements dans toutes directions (comme une dame aux échecs)",
            "",
            "But du jeu: Occuper les deux camps adverses ou empêcher l'adversaire de jouer",
            "en capturant suffisamment de ses pions.",
            "",
            "Pour occuper un camp adverse :",
            "1. Amener d'abord un pion sur la ligne de base adverse",
            "2. Puis déplacer ce pion dans un camp adverse (déplacement spécial)",
            "3. Une fois dans un camp, le pion y reste jusqu'à la fin de la partie",
            "",
            "Les captures sont autorisées sauf lors du premier tour de jeu.",
            "La capture se fait en déplaçant un de ses pions sur une case occupée par un pion adverse.",
        ]

        total_height = len(rules) * 30
        start_y = max(150, (screen_height - total_height) // 2 - 50)
        
        for i, rule in enumerate(rules):
            rule_text = fonts['small'].render(rule, True, BLACK)
            screen.blit(rule_text, (screen_width // 2 - rule_text.get_width() // 2, start_y + i * 30))
        
        back_button = draw_button(screen, fonts, "Retour", screen_width // 2 - 50, screen_height - 100, 100, 40, BLUE, RED)
        
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

# Démarrer le jeu Katarenga
def start_katarenga_game(screen, fonts, player1_name, player2_name, board, mode='local'):
    bot_player = 2 if mode == "bot" else None
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    print(board)
    # Initialiser l'état du jeu
    game_state = GameState()
    
    # Dessiner le plateau et l'obtenir
    game_state.board = draw_board(screen, fonts, board, draw_pieces=False)
    
    # Calculer la position du plateau pour le centrer
    board_width = BOARD_SIZE * TILE_SIZE
    board_height = BOARD_SIZE * TILE_SIZE
    board_x = (screen_width - board_width) // 2
    board_y = (screen_height - board_height) // 2
    
    # Obtenir les mouvements valides pour le joueur actuel
    game_state.valid_moves = get_valid_moves(game_state, game_state.board)
    
    # Texte d'aide
    help_text = fonts['small'].render("Cliquez sur un de vos pions puis sur une case valide pour le déplacer", True, BLACK)
    
    # Boucle principale du jeu
    running = True
   
    while running:
        screen.fill(WHITE)
        
        # Titre
        title_text = fonts['title'].render("Katarenga", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))

        
        # Afficher le joueur actuel
        current_player_name = player1_name if game_state.current_player == 1 else player2_name
        current_player_color = BLACK if game_state.current_player == 1 else WHITE
        
        # Afficher l'indicateur du tour en bas également
        turn_indicator = fonts['button'].render(
            f"Au tour de: {current_player_name}",
            True,
            current_player_color
        )
        screen.blit(turn_indicator, (screen_width // 2 - turn_indicator.get_width() // 2, screen_height - 60))
        
        # Afficher le texte d'aide
        screen.blit(help_text, (screen_width // 2 - help_text.get_width() // 2, 100))
        

        # Dessiner le plateau sans les pions
        draw_board(screen, fonts, board, draw_pieces=False)
        
        # Dessiner les pièces
        piece_radius = TILE_SIZE // 3
        
        # Dessiner les pions du joueur 1 (Noir)
        for idx, (x, y, in_camp) in enumerate(game_state.player1_pieces):
            if in_camp is None:  # Pion sur le plateau
                pygame.draw.circle(screen, BLACK, (
                    board_x + x * TILE_SIZE + TILE_SIZE // 2,
                    board_y + y * TILE_SIZE + TILE_SIZE // 2
                ), piece_radius)
            else:  # Pion dans un camp
                camp_x, camp_y = game_state.camp2_positions[in_camp - 1]
                pygame.draw.circle(screen, BLACK, (
                    board_x + camp_x * TILE_SIZE + TILE_SIZE // 2,
                    board_y + camp_y * TILE_SIZE + TILE_SIZE // 2
                ), piece_radius)
        
        # Dessiner les pions du joueur 2 (Blanc)
        for idx, (x, y, in_camp) in enumerate(game_state.player2_pieces):
            if in_camp is None:  # Pion sur le plateau
                pygame.draw.circle(screen, WHITE, (
                    board_x + x * TILE_SIZE + TILE_SIZE // 2,
                    board_y + y * TILE_SIZE + TILE_SIZE // 2
                ), piece_radius)
                # Ajouter un contour noir pour mieux voir les pions blancs
                pygame.draw.circle(screen, BLACK, (
                    board_x + x * TILE_SIZE + TILE_SIZE // 2,
                    board_y + y * TILE_SIZE + TILE_SIZE // 2
                ), piece_radius, 1)
            else:  # Pion dans un camp
                camp_x, camp_y = game_state.camp1_positions[in_camp - 1]
                pygame.draw.circle(screen, WHITE, (
                    board_x + camp_x * TILE_SIZE + TILE_SIZE // 2,
                    board_y + camp_y * TILE_SIZE + TILE_SIZE // 2
                ), piece_radius)
                # Ajouter un contour noir pour mieux voir les pions blancs
                pygame.draw.circle(screen, BLACK, (
                    board_x + camp_x * TILE_SIZE + TILE_SIZE // 2,
                    board_y + camp_y * TILE_SIZE + TILE_SIZE // 2
                ), piece_radius, 1)
        
        if game_state.selected_piece_idx is not None:
            if game_state.current_player == 1:
                selected_piece = game_state.player1_pieces[game_state.selected_piece_idx]
            else:
                selected_piece = game_state.player2_pieces[game_state.selected_piece_idx]
            
            if selected_piece[2] is None:  # Si le pion n'est pas dans un camp
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
        
        back_button = draw_button(screen, fonts, "Retour", 10, screen_height - 60, 100, 40, BLUE, RED)
        
        rules_button = draw_button(screen, fonts, "Règles", screen_width - 110, screen_height - 60, 100, 40, GREEN, HOVER_GREEN)
        
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
                    # Obtenir la position de la case cliquée
                    tile_x = (mouse_x - board_x) // TILE_SIZE
                    tile_y = (mouse_y - board_y) // TILE_SIZE
                    
                    # Vérifier si la position est valide
                    if 0 <= tile_x < BOARD_SIZE and 0 <= tile_y < BOARD_SIZE:
                        # Si un pion est déjà sélectionné
                        if game_state.selected_piece_idx is not None:
                            move_made = False
                            
                            # Vérifier si un mouvement valide a été sélectionné
                            if game_state.selected_piece_idx in game_state.valid_moves:
                                for move_x, move_y, is_camp_move in game_state.valid_moves[game_state.selected_piece_idx]:
                                    if (move_x, move_y) == (tile_x, tile_y):
                                        if click_sound:
                                            click_sound.play()
                                        
                                        # Effectuer le mouvement
                                        if game_state.current_player == 1:
                                            # Vérifier s'il s'agit d'une capture
                                            for idx, (p_x, p_y, p_camp) in enumerate(game_state.player2_pieces):
                                                if p_camp is None and (p_x, p_y) == (tile_x, tile_y):
                                                    # Supprimer le pion capturé
                                                    game_state.player2_pieces.pop(idx)
                                                    break
                                            
                                            # Mettre à jour la position du pion
                                            x, y, _ = game_state.player1_pieces[game_state.selected_piece_idx]
                                            
                                            if is_camp_move:
                                                # Déterminer quel camp est occupé (1 ou 2)
                                                camp_idx = 1 if (tile_x, tile_y) == game_state.camp2_positions[0] else 2
                                                game_state.player1_pieces[game_state.selected_piece_idx] = (tile_x, tile_y, camp_idx)
                                            else:
                                                game_state.player1_pieces[game_state.selected_piece_idx] = (tile_x, tile_y, None)
                                        else:
                                            # Vérifier s'il s'agit d'une capture
                                            for idx, (p_x, p_y, p_camp) in enumerate(game_state.player1_pieces):
                                                if p_camp is None and (p_x, p_y) == (tile_x, tile_y):
                                                    # Supprimer le pion capturé
                                                    game_state.player1_pieces.pop(idx)
                                                    break
                                            
                                            # Mettre à jour la position du pion
                                            x, y, _ = game_state.player2_pieces[game_state.selected_piece_idx]
                                            
                                            if is_camp_move:
                                                # Déterminer quel camp est occupé (1 ou 2)
                                                camp_idx = 1 if (tile_x, tile_y) == game_state.camp1_positions[0] else 2
                                                game_state.player2_pieces[game_state.selected_piece_idx] = (tile_x, tile_y, camp_idx)
                                            else:
                                                game_state.player2_pieces[game_state.selected_piece_idx] = (tile_x, tile_y, None)
                                        
                                        move_made = True
                                        break
                            
                            if move_made:
                                # Incrémenter le compteur de tours
                                game_state.turn_count += 1
                                
                                # Réinitialiser la sélection
                                game_state.selected_piece_idx = None
                                
                                # Vérifier si un joueur a gagné
                                if check_win(game_state):
                                    game_state.game_over = True
                                else:
                                    # Changer de joueur
                                    game_state.current_player = 3 - game_state.current_player  # Alterne entre 1 et 2
                                    
                                    # Mettre à jour les mouvements valides
                                    game_state.valid_moves = get_valid_moves(game_state, game_state.board)

                                    # Si c'est au bot de jouer (mode bot)
                                    if bot_player is not None and game_state.current_player == bot_player and not game_state.game_over:
                                        pygame.time.wait(500)  # Petite pause pour voir l'action du bot (500ms)
                                        bot_play(game_state)

                                        # Vérifie victoire après action du bot
                                        if check_win(game_state):
                                            game_state.game_over = True
                                        else:
                                            # Repasser au joueur humain
                                            game_state.current_player = 3 - game_state.current_player
                                            game_state.valid_moves = get_valid_moves(game_state, game_state.board)

                                    
                                    # Si le nouveau joueur n'a pas de mouvement valide, il perd
                                    if not game_state.valid_moves:
                                        game_state.game_over = True
                                        game_state.winner = 3 - game_state.current_player
                            else:
                                # Si le joueur clique ailleurs, désélectionner le pion
                                game_state.selected_piece_idx = None
                        else:
                            # Vérifier si le joueur a cliqué sur l'un de ses pions
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
    # Obtenir les mouvements valides pour le bot
    valid_moves = game_state.valid_moves

    if not valid_moves:
        return False  # Aucun coup possible

    # Choisir un pion au hasard parmi ceux qui ont des coups valides
    piece_idx = random.choice(list(valid_moves.keys()))

    # Choisir un mouvement au hasard pour ce pion
    move_x, move_y, is_camp_move = random.choice(valid_moves[piece_idx])

    # Effectuer le mouvement (même logique que pour le joueur)
    if game_state.current_player == 2:
        # Vérifier s'il s'agit d'une capture
        for idx, (p_x, p_y, p_camp) in enumerate(game_state.player1_pieces):
            if p_camp is None and (p_x, p_y) == (move_x, move_y):
                game_state.player1_pieces.pop(idx)
                break

        # Mettre à jour la position du pion
        x, y, _ = game_state.player2_pieces[piece_idx]
        if is_camp_move:
            camp_idx = 1 if (move_x, move_y) == game_state.camp1_positions[0] else 2
            game_state.player2_pieces[piece_idx] = (move_x, move_y, camp_idx)
        else:
            game_state.player2_pieces[piece_idx] = (move_x, move_y, None)

    return True  # Coup joué
        

# Pour la compatibilité avec l'ancienne version
def start_game(screen, fonts, player1_name, player2_name, board, mode="local"):
    start_katarenga_game(screen, fonts, player1_name, player2_name, board, mode=mode)