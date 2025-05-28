import pygame
import sys
from ui.colors import WHITE, BLACK, BLUE, HOVER_BLUE, GREEN, HOVER_GREEN
from ui.buttons import draw_button, click_sound
from ui.animations import loading_screen

from menu.katarenga_mode_slection import katarenga_mode_selection
from menu.congress_mode_selection import congress_mode_selection
from menu.isolation_mode_selection import isolation_mode_selection
from menu.settings import t

def game_selection(screen, fonts):
    '''affiche le menu de sélection du jeu
    args:
        screen: l'écran Pygame sur lequel dessiner
        fonts: un dictionnaire de polices de caractères
    '''
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    running = True
    
    while running:
        screen.fill(WHITE)

        # Titre
        title_text = fonts['title'].render(t("select_game"), True, BLACK)

        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))

        katarenga_button = draw_button(screen, fonts, "Katarenga", screen_width // 2 - 150, 150, 300, 60, GREEN, HOVER_GREEN)
        congress_button = draw_button(screen, fonts, "Congress", screen_width // 2 - 150, 250, 300, 60, GREEN, HOVER_GREEN)
        isolation_button = draw_button(screen, fonts, "Isolation", screen_width // 2 - 150, 350, 300, 60, GREEN, HOVER_GREEN)
        
        # Bouton Retour
        back_button = draw_button(screen, fonts, t("back"), 10, screen_height - 60, 100, 40, BLUE, HOVER_BLUE)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if katarenga_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    loading_screen(screen, fonts, t("selecting_game") + "Katarenga...")
                    katarenga_mode_selection(screen, fonts)
                    return
                    
                if congress_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    loading_screen(screen, fonts, t("selecting_game") + "Congress...")
                    congress_mode_selection(screen, fonts)
                    return
                    
                if isolation_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    loading_screen(screen, fonts, t("selecting_game") + "Isolation...")
                    isolation_mode_selection(screen, fonts)
                    return
                    
                if back_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    loading_screen(screen, fonts, t("back_loading"))
                    return
                    
        pygame.display.flip()
