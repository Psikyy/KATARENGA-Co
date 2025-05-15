import pygame
import sys
from ui.colors import WHITE, BLACK, BLUE, RED
from ui.buttons import draw_button
from ui.animations import loading_screen
from menu.settings import translations, settings, save_settings, t, current_language, set_language


def settings_menu(screen, fonts):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    global settings, current_language
    running = True
    language_options = list(translations.keys())
    language_index = language_options.index(current_language)

    while running:
        screen.fill(WHITE)

        # Titre
        title_text = fonts['title'].render(t("settings"), True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))

        # Langue
        language_label = fonts['button'].render(t("language") + ":", True, BLACK)
        screen.blit(language_label, (200, 200))
        current_language_text = fonts['small'].render(current_language, True, BLACK)
        screen.blit(current_language_text, (350, 200))
        next_language_button = draw_button(screen, fonts, ">", 450, 195, 40, 40, BLUE, RED)

        # Bouton Retour
        back_button = draw_button(screen, fonts, t("back"), 10, screen_height - 60, 100, 40, BLUE, RED)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Changer de langue
                if next_language_button.collidepoint(event.pos):
                    language_index = (language_index + 1) % len(language_options)
                    new_lang = language_options[language_index]
                    set_language(new_lang)
                    current_language = new_lang

                # Retour
                if back_button.collidepoint(event.pos):
                    loading_screen(screen, fonts, t("back") + "...")
                    return

        pygame.display.flip()