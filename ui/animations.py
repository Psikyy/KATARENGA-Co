import pygame
import time
from ui.colors import BLACK, WHITE, GRAY

# Animation d'intro
def intro_animation(screen):
    '''Affiche une animation d'introduction avec le logo "Smart Games" qui s'affiche progressivement.
    arg: 
        screen: l'écran sur lequel l'animation sera affichée.
    '''
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    screen.fill(BLACK)
    logo_font = pygame.font.Font(None, 100)
    text_surface = logo_font.render("Smart Games", True, WHITE)

    alpha = 0
    fade_in_speed = 5
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(BLACK)

        if alpha < 255:
            alpha += fade_in_speed
        else:
            time.sleep(1)
            running = False

        text_surface.set_alpha(alpha)
        screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, screen_height // 2 - text_surface.get_height() // 2))

        pygame.display.flip()
        clock.tick(30)

    time.sleep(1) 

def loading_screen(screen, fonts, message="Chargement..."):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    screen.fill(GRAY)
    text = fonts['title'].render(message, True, BLACK)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
    pygame.display.flip()
    time.sleep(1)

def animate_rotation(quadrant, current_rotation, target_rotation):
    """
    Anime la rotation d'un quadrant de current_rotation à target_rotation.
    """
    step = 9 
    if current_rotation < target_rotation:
        current_rotation += step
    elif current_rotation > target_rotation:
        current_rotation -= step
    return current_rotation % 360