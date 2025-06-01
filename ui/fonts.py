import pygame

def init_fonts():
    return {
        'title': pygame.font.Font(None, 80),
        'large': pygame.font.Font(None, 48),   
        'medium': pygame.font.Font(None, 36),
        'button': pygame.font.Font(None, 30),
        'small': pygame.font.Font(None, 24),
    }
