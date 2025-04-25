import pygame
import sys
from ui.colors import WHITE, BLACK, BLUE, RED, GREEN, HOVER_GREEN
from ui.buttons import draw_button, click_sound
from games.katarenga.board import BOARD_SIZE, TILE_SIZE, TILE_TYPES, draw_board

# Positions des pièces sur le plateau
class GameState:
    def __init__(self):
        self.board = None
        self.player1_pos = (0, 0)  # Position de la pièce du joueur 1 (Rouge)
        self.player2_pos = (7, 7)  # Position de la pièce du joueur 2 (Bleu)
        self.current_player = 1    # Joueur 1 commence
        self.valid_moves = []      # Mouvements valides pour le joueur actuel
        self.game_over = False     # Indique si le jeu est terminé
        self.winner = None         # Indique le vainqueur (1 ou 2)

# Obtenir les mouvements valides pour un joueur
def get_valid_moves(game_state, board):
    valid_moves = []
    
    if game_state.current_player == 1:
        player_pos = game_state.player1_pos
    else:
        player_pos = game_state.player2_pos
    
    x, y = player_pos
    tile_type = board[y][x]
    
    # Mouvements selon le type de case
    if tile_type == 'A':  # Orthogonal
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    elif tile_type == 'B':  # Diagonal
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
    elif tile_type == 'C':  # Cavalier
        directions = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
    elif tile_type == 'D':  # Toutes directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
    
    # Vérifier les mouvements possibles
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        
        # Vérifier si la nouvelle position est dans le plateau
        if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
            # Vérifier si la case est occupée
            if (new_x, new_y) != game_state.player1_pos and (new_x, new_y) != game_state.player2_pos:
                valid_moves.append((new_x, new_y))
    
    return valid_moves

# Vérifier si un joueur a gagné
def check_win(game_state):
    # Vérifier si un joueur a atteint le côté opposé
    player1_x, player1_y = game_state.player1_pos
    player2_x, player2_y = game_state.player2_pos
    
    if player1_y == BOARD_SIZE - 1:  # Joueur 1 a atteint le bord inférieur
        return 1
    elif player2_y == 0:  # Joueur 2 a atteint le bord supérieur
        return 2
    
    # Vérifier si un joueur ne peut plus se déplacer
    if not game_state.valid_moves:
        return 2 if game_state.current_player == 1 else 1
    
    return None

# Démarrer le jeu Katarenga
def start_katarenga_game(screen, fonts, player1_name, player2_name, selected_quadrants):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    # Initialiser l'état du jeu
    game_state = GameState()
    
    # Dessiner le plateau et l'obtenir
    game_state.board = draw_board(screen, fonts, selected_quadrants)
    
    # Calculer la position du plateau pour le centrer
    board_width = BOARD_SIZE * TILE_SIZE
    board_height = BOARD_SIZE * TILE_SIZE
    board_x = (screen_width - board_width) // 2
    board_y = (screen_height - board_height) // 2
    
    # Obtenir les mouvements valides pour le joueur actuel
    game_state.valid_moves = get_valid_moves(game_state, game_state.board)
    
    # Texte d'aide
    help_text = fonts['small'].render("Cliquez sur une case pour déplacer votre pièce", True, BLACK)
    
    # Boucle principale du jeu
    running = True
    while running:
        screen.fill(WHITE)
        
        # Titre
        title_text = fonts['title'].render("Katarenga", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))
        
        # Afficher les joueurs
        player1_text = fonts['small'].render(f"{player1_name} (Rouge)", True, RED)
        player2_text = fonts['small'].render(f"{player2_name} (Bleu)", True, BLUE)
        
        screen.blit(player1_text, (50, 100))
        screen.blit(player2_text, (screen_width - 50 - player2_text.get_width(), 100))
        
        # Afficher le joueur actuel
        current_player_text = fonts['button'].render(
            f"Tour de {player1_name}" if game_state.current_player == 1 else f"Tour de {player2_name}",
            True,
            RED if game_state.current_player == 1 else BLUE
        )
        screen.blit(current_player_text, (screen_width // 2 - current_player_text.get_width() // 2, 100))
        
        # Afficher le texte d'aide
        screen.blit(help_text, (screen_width // 2 - help_text.get_width() // 2, 140))
        
        # Dessiner le plateau
        draw_board(screen, fonts, selected_quadrants)
        
        # Dessiner les pièces
        piece_radius = TILE_SIZE // 3
        
        # Joueur 1 (Rouge)
        pygame.draw.circle(screen, RED, (
            board_x + game_state.player1_pos[0] * TILE_SIZE + TILE_SIZE // 2,
            board_y + game_state.player1_pos[1] * TILE_SIZE + TILE_SIZE // 2
        ), piece_radius)
        
        # Joueur 2 (Bleu)
        pygame.draw.circle(screen, BLUE, (
            board_x + game_state.player2_pos[0] * TILE_SIZE + TILE_SIZE // 2,
            board_y + game_state.player2_pos[1] * TILE_SIZE + TILE_SIZE // 2
        ), piece_radius)
        
        # Dessiner les mouvements valides
        for move_x, move_y in game_state.valid_moves:
            pygame.draw.circle(screen, GREEN, (
                board_x + move_x * TILE_SIZE + TILE_SIZE // 2,
                board_y + move_y * TILE_SIZE + TILE_SIZE // 2
            ), piece_radius // 2, 2)
        
        # Bouton Retour
        back_button = draw_button(screen, fonts, "Retour", 10, screen_height - 60, 100, 40, BLUE, RED)
        
        # Afficher le message de fin de partie si le jeu est terminé
        if game_state.game_over:
            winner_name = player1_name if game_state.winner == 1 else player2_name
            winner_text = fonts['title'].render(f"{winner_name} a gagné !", True, BLACK)
            
            # Fond semi-transparent
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 200))
            screen.blit(overlay, (0, 0))
            
            # Message de victoire
            screen.blit(winner_text, (screen_width // 2 - winner_text.get_width() // 2, screen_height // 2 - 50))
            
            # Bouton Nouvelle Partie
            new_game_button = draw_button(screen, fonts, "Nouvelle Partie", screen_width // 2 - 100, screen_height // 2 + 50, 200, 50, GREEN, HOVER_GREEN)
        
        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                
                # Retour au menu
                if back_button.collidepoint(mouse_x, mouse_y):
                    if click_sound:
                        click_sound.play()
                    return
                
                # Si le jeu est terminé
                if game_state.game_over:
                    if 'new_game_button' in locals() and new_game_button.collidepoint(mouse_x, mouse_y):
                        if click_sound:
                            click_sound.play()
                        return
                else:
                    # Vérifier si un mouvement valide a été sélectionné
                    for move_x, move_y in game_state.valid_moves:
                        move_rect = pygame.Rect(
                            board_x + move_x * TILE_SIZE,
                            board_y + move_y * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE
                        )
                        
                        if move_rect.collidepoint(mouse_x, mouse_y):
                            if click_sound:
                                click_sound.play()
                            
                            # Mettre à jour la position du joueur
                            if game_state.current_player == 1:
                                game_state.player1_pos = (move_x, move_y)
                            else:
                                game_state.player2_pos = (move_x, move_y)
                            
                            # Vérifier si un joueur a gagné
                            winner = check_win(game_state)
                            if winner:
                                game_state.game_over = True
                                game_state.winner = winner
                            else:
                                # Changer de joueur
                                game_state.current_player = 3 - game_state.current_player  # Alterne entre 1 et 2
                                
                                # Mettre à jour les mouvements valides
                                game_state.valid_moves = get_valid_moves(game_state, game_state.board)
                                
                                # Si le nouveau joueur n'a pas de mouvement valide, il perd
                                if not game_state.valid_moves:
                                    game_state.game_over = True
                                    game_state.winner = 3 - game_state.current_player
                            
                            break
        
        pygame.display.flip()