import pygame
import sys
from settings import load_settings
from ui.animations import intro_animation
from menu import main_menu

def main():
    # Initialisation de Pygame
    pygame.init()
    
    # Charger les paramètres
    settings = load_settings()
    
    # Configurer l'écran
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    if settings.get("fullscreen", False):
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    pygame.display.set_caption("Katarenga")
    
    # Charger la musique de fond
    try:
        pygame.mixer.music.load("assets/musique/adventure.mp3")
        pygame.mixer.music.set_volume(settings["volume"])
        pygame.mixer.music.play(-1)  # Boucle infinie
    except pygame.error:
        print("Musique de fond non trouvée.")
    
    # Animation d'intro
    intro_animation(screen)
    
    # Démarrer le menu principal
    main_menu(screen)

if __name__ == "__main__":
    main()