import pygame
import sys
from ui.colors import WHITE, GREEN, HOVER_GREEN, BLUE, HOVER_BLUE, RED, HOVER_RED
from ui.buttons import draw_button, click_sound
from ui.fonts import init_fonts
from ui.animations import loading_screen
from menu.settings_menu import settings_menu
from menu.game_selection import game_selection

def main_menu(screen):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    # Initialiser les polices
    fonts = init_fonts()
    
    # Charger et redimensionner l'image de fond
    try:
        background_image = pygame.image.load("img/Image_du_jeu.png")
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    except pygame.error:
        print("Image de fond non trouvée.")
        background_image = pygame.Surface((screen_width, screen_height))
        background_image.fill((0, 0, 0))
    
    running = True
    title_alpha = 255  # Opacité du titre
    fade_out = True  # Direction de l'animation du titre

    while running:
        screen.blit(background_image, (0, 0))  # Affiche l'image de fond

        # Animation du titre
        if fade_out:
            title_alpha -= 3
            if title_alpha <= 100:
                fade_out = False
        else:
            title_alpha += 3
            if title_alpha >= 255:
                fade_out = True

        # # Titre
        # title_surface = fonts['title'].render("Katarenga", True, WHITE)
        # title_surface.set_alpha(title_alpha)  # Appliquer la transparence
        # screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, 50))

        # Boutons
        start_button = draw_button(screen, fonts, "Lancer le jeu", screen_width // 2 - 150, 250, 300, 60, GREEN, HOVER_GREEN)
        settings_button = draw_button(screen, fonts, "Paramètres", screen_width // 2 - 150, 350, 300, 60, BLUE, HOVER_BLUE)
        quit_button = draw_button(screen, fonts, "Quitter", screen_width // 2 - 150, 450, 300, 60, RED, HOVER_RED)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    game_selection(screen, fonts)  # Sélection du jeu
                if settings_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    settings_menu(screen, fonts)  # Menu des paramètres
                if quit_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()