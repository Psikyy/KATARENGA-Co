import pygame
import sys
from ui.colors import WHITE, BLACK, BLUE, HOVER_BLUE, GREEN, HOVER_GREEN
from ui.buttons import draw_button, click_sound
from ui.animations import loading_screen

from menu.katarenga_mode_slection import katarenga_mode_selection
from menu.congress_mode_selection import congress_mode_selection
from menu.isolation_mode_selection import isolation_mode_selection

def game_selection(screen, fonts):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    running = True
    
    while running:
        screen.fill(WHITE)
        
        # Titre
        title_text = fonts['title'].render("Sélection du jeu", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))
        
        # Boutons des jeux
        katarenga_button = draw_button(screen, fonts, "Katarenga", screen_width // 2 - 150, 150, 300, 60, GREEN, HOVER_GREEN)
        congress_button = draw_button(screen, fonts, "Congress", screen_width // 2 - 150, 250, 300, 60, GREEN, HOVER_GREEN)
        isolation_button = draw_button(screen, fonts, "Isolation", screen_width // 2 - 150, 350, 300, 60, GREEN, HOVER_GREEN)
        
        # Bouton Retour
        back_button = draw_button(screen, fonts, "Retour", 10, screen_height - 60, 100, 40, BLUE, HOVER_BLUE)
        
        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if katarenga_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    loading_screen(screen, fonts, "Sélection du mode Katarenga...")
                    katarenga_mode_selection(screen, fonts)
                    return
                    
                if congress_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    loading_screen(screen, fonts, "Sélection du mode Congress...")
                    congress_mode_selection(screen, fonts)
                    return
                    
                if isolation_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    loading_screen(screen, fonts, "Sélection du mode Isolation...")
                    isolation_mode_selection(screen, fonts)
                    return
                    
                if back_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    loading_screen(screen, fonts, "Retour...")
                    return
                    
        pygame.display.flip()
