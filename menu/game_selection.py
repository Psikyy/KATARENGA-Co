import pygame
import sys
from ui.colors import WHITE, BLACK, GREEN, RED, BLUE, HOVER_GREEN
from ui.buttons import draw_button, click_sound
from menu.player_names import player_names


def game_selection(screen, fonts, network_mode=False, network_role=None, network_manager=None):
    """
    Affiche l'écran de sélection de jeu et retourne le jeu sélectionné
    """
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    running = True
    
    while running:
        screen.fill(WHITE)
        
        # Titre
        title_text = fonts['title'].render("Sélection du jeu", True, BLACK)
        title_x = screen_width // 2 - title_text.get_width() // 2
        title_y = 50
        screen.blit(title_text, (title_x, title_y))
        
        # Instructions
        mode_text = "Mode Réseau - " + ("Hôte" if network_role == 'host' else "Client") if network_mode else "Mode Local"
        instruction_text = fonts['small'].render(mode_text, True, BLACK)
        instruction_x = screen_width // 2 - instruction_text.get_width() // 2
        instruction_y = title_y + title_text.get_height() + 20
        screen.blit(instruction_text, (instruction_x, instruction_y))
        
        # Boutons de jeu
        button_width = 200
        button_height = 60
        button_spacing = 30
        start_y = 150
        
        katarenga_button = draw_button(screen, fonts, "Katarenga", 
                                      screen_width // 2 - button_width // 2, 
                                      start_y, 
                                      button_width, button_height, 
                                      GREEN, HOVER_GREEN)
        
        isolation_button = draw_button(screen, fonts, "Isolation", 
                                     screen_width // 2 - button_width // 2, 
                                     start_y + button_height + button_spacing, 
                                     button_width, button_height, 
                                     GREEN, HOVER_GREEN)
        
        congress_button = draw_button(screen, fonts, "Congress", 
                                    screen_width // 2 - button_width // 2, 
                                    start_y + 2 * (button_height + button_spacing), 
                                    button_width, button_height, 
                                    GREEN, HOVER_GREEN)
        
        back_button = draw_button(screen, fonts, "Retour", 
                                10, screen_height - 60, 
                                100, 40, 
                                BLUE, RED)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if network_mode and network_manager:
                    network_manager.close()
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                
                if katarenga_button.collidepoint((mouse_x, mouse_y)):
                    if click_sound:
                        click_sound.play()
                    player_names(screen, fonts, "Katarenga", network_mode, 
                                network_role=network_role, network_manager=network_manager)
                
                elif isolation_button.collidepoint((mouse_x, mouse_y)):
                    if click_sound:
                        click_sound.play()
                    player_names(screen, fonts, "Isolation", network_mode, 
                                network_role=network_role, network_manager=network_manager)
                
                elif congress_button.collidepoint((mouse_x, mouse_y)):
                    if click_sound:
                        click_sound.play()
                    player_names(screen, fonts, "Congress", network_mode, 
                                network_role=network_role, network_manager=network_manager)
                
                elif back_button.collidepoint((mouse_x, mouse_y)):
                    if click_sound:
                        click_sound.play()
                    return  # Retour au menu principal
                
        pygame.display.flip()