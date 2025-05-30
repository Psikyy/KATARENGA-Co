import pygame
import sys
from ui.colors import WHITE, GREEN, HOVER_GREEN, BLUE, HOVER_BLUE, RED, HOVER_RED
from ui.buttons import draw_button, click_sound
from ui.fonts import init_fonts
from menu.settings_menu import settings_menu
from menu.game_selection import game_selection
from menu.settings import t


def main_menu(screen):
    '''Affiche le menu principal du jeu.'''
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    fonts = init_fonts()

    try:
        background_image = pygame.image.load("img/image_du_jeu.png").convert()
        image_ratio = background_image.get_width() / background_image.get_height()
        screen_ratio = screen_width / screen_height

        if image_ratio > screen_ratio:
            new_width = screen_width
            new_height = int(screen_width / image_ratio)
        else:
            new_height = screen_height
            new_width = int(screen_height * image_ratio)

        background_image = pygame.transform.smoothscale(background_image, (new_width, new_height))
    except pygame.error:
        print("Image de fond non trouvée.")
        background_image = pygame.Surface((screen_width, screen_height))
        background_image.fill((0, 0, 0))

    running = True
    title_alpha = 255
    fade_out = True  

    button_width = 400
    button_height = 80
    button_spacing = 40
    total_height = 3 * button_height + 2 * button_spacing
    start_y = (screen_height - total_height) // 2

    while running:
        screen.fill((0, 0, 0))
        bg_x = (screen_width - background_image.get_width()) // 2
        bg_y = (screen_height - background_image.get_height()) // 2
        screen.blit(background_image, (bg_x, bg_y))

        if fade_out:
            title_alpha -= 3
            if title_alpha <= 100:
                fade_out = False
        else:
            title_alpha += 3
            if title_alpha >= 255:
                fade_out = True

        start_button = draw_button(screen, fonts, t("start_game"),
                                   (screen_width - button_width) // 2,
                                   start_y,
                                   button_width, button_height, GREEN, HOVER_GREEN)

        settings_button = draw_button(screen, fonts, t("settings"),
                                      (screen_width - button_width) // 2,
                                      start_y + button_height + button_spacing,
                                      button_width, button_height, BLUE, HOVER_BLUE)

        quit_button = draw_button(screen, fonts, t("quit"),
                                  (screen_width - button_width) // 2,
                                  start_y + 2 * (button_height + button_spacing),
                                  button_width, button_height, RED, HOVER_RED)

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
