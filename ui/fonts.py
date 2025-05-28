import pygame

def init_fonts():

    font = pygame.font.Font(None, 80)  
    button_font = pygame.font.Font(None, 35) 
    small_font = pygame.font.Font(None, 30)
    
    return {
        'title': font,
        'button': button_font,
        'small': small_font
    }