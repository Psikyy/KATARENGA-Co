import pygame
from ui.colors import WHITE, BLACK

click_sound = None
hover_sound = None

def init_sounds():
    global click_sound, hover_sound
    try:
        click_sound = pygame.mixer.Sound("assets/musique/click.wav")  
        hover_sound = pygame.mixer.Sound("assets/musique/hover.wav")  
    except pygame.error:
        print("Sons non trouvés. Les effets sonores seront désactivés.")


def draw_button(screen, fonts, text, x, y, width, height, color, hover_color, text_color=WHITE, disabled=False):
    '''dessine un bouton avec du texte, une couleur de fond, une couleur de survol et une couleur de texte
    Args:
        screen (pygame.Surface): la surface sur laquelle dessiner le bouton
        fonts (dict): dictionnaire de polices de caractères
        text (str): le texte à afficher sur le bouton
        x (int): position x du bouton
        y (int): position y du bouton
        width (int): largeur du bouton
        height (int): hauteur du bouton
        color (tuple): couleur de fond du bouton
        hover_color (tuple): couleur de fond lorsque la souris survole le bouton
        text_color (tuple, optional): couleur du texte. Defaults to WHITE.
        disabled (bool, optional): si True, le bouton est désactivé et grisé. Defaults to False.'''
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    if disabled:
        disabled_color = (150, 150, 150)  
        pygame.draw.rect(screen, disabled_color, button_rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, button_rect, width=3, border_radius=15)  
        final_text_color = (200, 200, 200)  
    else:
        if button_rect.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(screen, hover_color, button_rect, border_radius=15)
            pygame.draw.rect(screen, WHITE, button_rect, width=3, border_radius=15) 
            if hover_sound:
                if not hasattr(draw_button, 'last_hovered') or draw_button.last_hovered != button_rect:
                    hover_sound.play()
                    draw_button.last_hovered = button_rect
        else:
            pygame.draw.rect(screen, color, button_rect, border_radius=15)
            pygame.draw.rect(screen, BLACK, button_rect, width=3, border_radius=15) 
        final_text_color = text_color

    text_surface = fonts['button'].render(text, True, final_text_color)
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

    return button_rect