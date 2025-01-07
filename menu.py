import pygame
import sys
import re

# Initialisation de Pygame
pygame.init()

# Définir les dimensions de l'écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu Principal")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Polices
font = pygame.font.Font(None, 40)
button_font = pygame.font.Font(None, 30)

# Définir les boutons
def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    
    if button_rect.collidepoint((mouse_x, mouse_y)):
        pygame.draw.rect(screen, hover_color, button_rect)
    else:
        pygame.draw.rect(screen, color, button_rect)
    
    text_surface = button_font.render(text, True, WHITE)
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))
    
    return button_rect

# Fonction principale
def main_menu():
    running = True
    while running:
        screen.fill(BLUE)  # Fond d'écran

        # Afficher le titre
        title_text = font.render("Katarenga", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Afficher les boutons
        start_button = draw_button("Start Game", 300, 200, 200, 50, GREEN, RED)
        load_button = draw_button("Load Game", 300, 300, 200, 50, GREEN, RED)
        quit_button = draw_button("Quit", 300, 400, 200, 50, GREEN, RED)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    start_game()  # Fonction à implémenter pour démarrer le jeu
                if load_button.collidepoint(event.pos):
                    load_game()  # Fonction à implémenter pour charger le jeu
                if quit_button.collidepoint(event.pos):
                    running = False

        pygame.display.flip()

# Fonction pour démarrer un jeu
def start_game():
    print("Démarrer le jeu")  # Implémenter le démarrage du jeu

# Fonction pour charger un jeu
def load_game():
    print("Charger le jeu")  # Implémenter le chargement du jeu

# Lancer le menu principal
if __name__ == "__main__":
    main_menu()
    pygame.quit()
    sys.exit()
