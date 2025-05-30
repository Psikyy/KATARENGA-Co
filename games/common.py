import pygame
from ui.colors import BLACK, WHITE, RED, BLUE, GREEN, HOVER_GREEN
from ui.buttons import draw_button, click_sound
from menu.settings import t


def draw_centered_text(screen, font, text, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen_width = screen.get_width()
    screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, y))

def display_player_turn(screen, fonts, player_name):
    turn_text = fonts['button'].render(t("turn") + player_name, True, player_color)
    screen_width = screen.get_width()
    screen.blit(turn_text, (screen_width // 2 - turn_text.get_width() // 2, 100))

def display_game_over(screen, fonts, winner_name, show_new_game_button=True):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 200))
    screen.blit(overlay, (0, 0))
    
    winner_text = fonts['title'].render(winner_name + t("win"), True, BLACK)
    screen.blit(winner_text, (screen_width // 2 - winner_text.get_width() // 2, screen_height // 2 - 50))
    
    if show_new_game_button:
        new_game_button = draw_button(screen, fonts, t("new_game"), screen_width // 2 - 100, screen_height // 2 + 50, 200, 50, GREEN, HOVER_GREEN)
        return new_game_button
    return None

def display_players(screen, fonts, player1_name, player2_name):
    screen_width = screen.get_width()
    
    player1_text = fonts['small'].render(player1_name + t("red"), True, RED)
    player2_text = fonts['small'].render(player2_name + t("blue"), True, BLUE)
    
    screen.blit(player1_text, (50, 100))
    screen.blit(player2_text, (screen_width - 50 - player2_text.get_width(), 100))

def create_back_button(screen, fonts, y_position=None):
    screen_height = screen.get_height()
    if y_position is None:
        y_position = screen_height - 60
    
    back_button = draw_button(screen, fonts, t("back"), 10, y_position, 100, 40, BLUE, RED)
    return back_button

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