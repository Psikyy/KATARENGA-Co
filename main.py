import pygame
import sys
from settings import load_settings
from ui.animations import intro_animation
from menu.main_menu import main_menu

def main():
    pygame.init()
    
    settings = load_settings()
    
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800
    if settings.get("fullscreen", False):
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    pygame.display.set_caption("Katarenga")
    
    try:
        pygame.mixer.music.load("musique/adventure.mp3")
        pygame.mixer.music.set_volume(settings["volume"])
        pygame.mixer.music.play(-1)  
    except pygame.error:
        print("Musique de fond non trouvée.")
    
    intro_animation(screen)
    
    main_menu(screen)

if __name__ == "__main__":
    main()