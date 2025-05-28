import pygame
import sys
from ui.colors import WHITE, GREEN, HOVER_GREEN, BLUE, HOVER_BLUE, RED, HOVER_RED
from ui.buttons import draw_button, click_sound
from ui.fonts import init_fonts
from menu.settings_menu import settings_menu
from menu.game_selection import game_selection
from menu.settings import t


def main_menu(screen):
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    fonts = init_fonts()

    try:
        background_image = pygame.image.load("img/Image_du_jeu.png")
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    except pygame.error:
        print("Image de fond non trouvée.")
        background_image = pygame.Surface((screen_width, screen_height))
        background_image.fill((0, 0, 0))
    
    running = True
    title_alpha = 255
    fade_out = True  

    while running:
        screen.blit(background_image, (0, 0))  
        if fade_out:
            title_alpha -= 3
            if title_alpha <= 100:
                fade_out = False
        else:
            title_alpha += 3
            if title_alpha >= 255:
                fade_out = True

        start_button = draw_button(screen, fonts, t("start_game"), screen_width // 2 - 150, 250, 300, 60, GREEN, HOVER_GREEN)
        settings_button = draw_button(screen, fonts, t("settings"), screen_width // 2 - 150, 350, 300, 60, BLUE, HOVER_BLUE)
        quit_button = draw_button(screen, fonts, t("quit"), screen_width // 2 - 150, 450, 300, 60, RED, HOVER_RED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    game_selection(screen, fonts) 
                if settings_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    settings_menu(screen, fonts)
                if quit_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()