import pygame
from ui.colors import WHITE, BLACK

# Variables pour le son
click_sound = None
hover_sound = None

def init_sounds():
    global click_sound, hover_sound
    try:
        click_sound = pygame.mixer.Sound("assets/musique/click.wav")  # Son de clic
        hover_sound = pygame.mixer.Sound("assets/musique/hover.wav")  # Son de survol
    except pygame.error:
        print("Sons non trouvés. Les effets sonores seront désactivés.")

# Fonction pour dessiner les boutons avec des effets de survol
# ui/buttons.py

def draw_button(screen, fonts, text, x, y, width, height, color, hover_color, text_color=WHITE, disabled=False):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    # Couleur grisée si désactivé
    if disabled:
        disabled_color = (150, 150, 150)  # Gris clair
        pygame.draw.rect(screen, disabled_color, button_rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, button_rect, width=3, border_radius=15)  # Bordure noire
        final_text_color = (200, 200, 200)  # Gris plus clair pour le texte
    else:
        # Si survol
        if button_rect.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(screen, hover_color, button_rect, border_radius=15)
            pygame.draw.rect(screen, WHITE, button_rect, width=3, border_radius=15)  # Bordure blanche
            if hover_sound:
                if not hasattr(draw_button, 'last_hovered') or draw_button.last_hovered != button_rect:
                    hover_sound.play()
                    draw_button.last_hovered = button_rect
        else:
            pygame.draw.rect(screen, color, button_rect, border_radius=15)
            pygame.draw.rect(screen, BLACK, button_rect, width=3, border_radius=15)  # Bordure noire
        final_text_color = text_color

    # Texte centré
    text_surface = fonts['button'].render(text, True, final_text_color)
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

    return button_rect