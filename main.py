import pygame
import sys
from settings import load_settings
from ui.animations import intro_animation
from menu.main_menu import main_menu

def main():
    '''Initialise le jeu, lance l'animation d'introduction et le menu principal'''
    pygame.init()

    settings = load_settings()

    info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

    fullscreen = settings.get("fullscreen", False)
    
    flags = pygame.FULLSCREEN if fullscreen else 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
    
    pygame.display.set_caption("Katarenga")

    try:
        pygame.mixer.music.load("musique/adventure.mp3")
        pygame.mixer.music.set_volume(settings["volume"])
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("Musique de fond non trouvée.")
    
    intro_animation(screen)

    running = True
    while running:
        main_menu(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((1000, 800))
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()