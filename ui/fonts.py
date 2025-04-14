import pygame

def init_fonts():
    # Polices
    font = pygame.font.Font(None, 80)  # Grande police pour le titre
    button_font = pygame.font.Font(None, 40)  # Police pour les boutons
    small_font = pygame.font.Font(None, 30)  # Police plus petite pour les textes secondaires
    
    return {
        'title': font,
        'button': button_font,
        'small': small_font
    }