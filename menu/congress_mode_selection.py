# menu/congress_mode_selection.py

import pygame
import sys
from ui.colors import WHITE, BLACK, BLUE, HOVER_BLUE, GREEN, HOVER_GREEN, GREY
from ui.buttons import draw_button, click_sound
from ui.animations import loading_screen
from menu.player_names import player_names
from menu.settings import t

def congress_mode_selection(screen, fonts):
    '''affiche le menu de sélection du mode de jeu pour Congress
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
        title_text = fonts['title'].render(t("game_mode") + "Congress", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))
        
        # Boutons des modes de jeu
        local_button = draw_button(screen, fonts, t("mode_local"), screen_width // 2 - 150, 150, 300, 60, GREEN, HOVER_GREEN)
        online_button = draw_button(screen, fonts, t("mode_online"), screen_width // 2 - 150, 250, 300, 60, GREY, GREY, disabled=True)
        bot_button = draw_button(screen, fonts, t("mode_bot"), screen_width // 2 - 150, 350, 300, 60, GREEN, HOVER_GREEN)


        # Bouton Retour
        back_button = draw_button(screen, fonts, t("back"), 10, screen_height - 60, 100, 40, BLUE, HOVER_BLUE)
        
        # Gérer les événements

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if local_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    loading_screen(screen, fonts, t("mode_local_loading"))
                    player_names(screen, fonts, "Congress", mode="local")
                    return

                if bot_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    loading_screen(screen, fonts, t("mode_bot_loading"))
                    player_names(screen, fonts, "Congress", mode="bot")
                    return

                if back_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    loading_screen(screen, fonts, t("back_loading"))
                    return

        pygame.display.flip()
