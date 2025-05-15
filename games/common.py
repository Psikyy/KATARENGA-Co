import pygame
from ui.colors import BLACK, WHITE, RED, BLUE, GREEN, HOVER_GREEN
from ui.buttons import draw_button, click_sound

# Fonction pour dessiner un texte centré
def draw_centered_text(screen, font, text, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen_width = screen.get_width()
    screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, y))

# Fonction pour afficher le tour du joueur
def display_player_turn(screen, fonts, player_name):
    turn_text = fonts['button'].render(f"Tour de {player_name}", True, player_color)
    screen_width = screen.get_width()
    screen.blit(turn_text, (screen_width // 2 - turn_text.get_width() // 2, 100))

# Fonction pour afficher l'écran de fin de jeu
def display_game_over(screen, fonts, winner_name, show_new_game_button=True):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    # Fond semi-transparent
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 200))
    screen.blit(overlay, (0, 0))
    
    # Message de victoire
    winner_text = fonts['title'].render(f"{winner_name} a gagné !", True, BLACK)
    screen.blit(winner_text, (screen_width // 2 - winner_text.get_width() // 2, screen_height // 2 - 50))
    
    # Bouton Nouvelle Partie
    if show_new_game_button:
        new_game_button = draw_button(screen, fonts, "Nouvelle Partie", screen_width // 2 - 100, screen_height // 2 + 50, 200, 50, GREEN, HOVER_GREEN)
        return new_game_button
    return None

# Fonction pour afficher les joueurs
def display_players(screen, fonts, player1_name, player2_name):
    screen_width = screen.get_width()
    
    player1_text = fonts['small'].render(f"{player1_name} (Rouge)", True, RED)
    player2_text = fonts['small'].render(f"{player2_name} (Bleu)", True, BLUE)
    
    screen.blit(player1_text, (50, 100))
    screen.blit(player2_text, (screen_width - 50 - player2_text.get_width(), 100))

# Fonction pour créer un bouton retour
def create_back_button(screen, fonts, y_position=None):
    screen_height = screen.get_height()
    if y_position is None:
        y_position = screen_height - 60
    
    back_button = draw_button(screen, fonts, "Retour", 10, y_position, 100, 40, BLUE, RED)
    return back_button

# Fonction pour traiter les événements communs
def handle_common_events(event, back_button=None, new_game_button=None):
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()
        
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos
        
        if back_button and back_button.collidepoint(mouse_pos):
            if click_sound:
                click_sound.play()
            return "back"
            
        if new_game_button and new_game_button.collidepoint(mouse_pos):
            if click_sound:
                click_sound.play()
            return "new_game"
            
    return None