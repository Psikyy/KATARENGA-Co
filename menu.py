import pygame
import sys
import re


# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Katarenga")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Polices
font = pygame.font.Font(None, 40)
button_font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 20)

# Variables globales
fullscreen = False
volume = 50

# Fonction pour dessiner les boutons
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

# Menu principal
def main_menu():
    running = True
    while running:
        screen.fill(BLUE)  # Fond d'écran

        # Titre
        title_text = font.render("Katarenga", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Boutons
        start_button = draw_button("Lancer le jeu", 300, 200, 200, 50, GREEN, RED)
        settings_button = draw_button("Paramètres", 300, 300, 200, 50, GREEN, RED)
        quit_button = draw_button("Quitter", 300, 400, 200, 50, GREEN, RED)

        # Copyright
        copyright_text = small_font.render("© Skibidigalio Team", True, WHITE)
        screen.blit(copyright_text, (10, SCREEN_HEIGHT - 30))

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_selection()
                if settings_button.collidepoint(event.pos):
                    settings_menu()
                if quit_button.collidepoint(event.pos):
                    running = False

        pygame.display.flip()

# Sélection de jeu
def game_selection():
    running = True
    while running:
        screen.fill(GRAY)  # Fond d'écran

        # Titre
        title_text = font.render("Choisissez un jeu", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Carrés pour les jeux
        katarenga_box = draw_button("Katarenga", 150, 200, 200, 100, GREEN, RED)
        congress_box = draw_button("Congress", 400, 200, 200, 100, GREEN, RED)
        isolation_box = draw_button("Isolation", 275, 350, 200, 100, GREEN, RED)

        # Bouton Retour
        back_button = draw_button("Retour", 10, SCREEN_HEIGHT - 60, 100, 40, BLUE, RED)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return
                if katarenga_box.collidepoint(event.pos):
                    print("Katarenga sélectionné !")
                if congress_box.collidepoint(event.pos):
                    print("Congress sélectionné !")
                if isolation_box.collidepoint(event.pos):
                    print("Isolation sélectionné !")

        pygame.display.flip()

# Menu des paramètres
def settings_menu():
    global fullscreen, volume
    running = True
    while running:
        screen.fill(GRAY)  # Fond d'écran

        # Titre
        title_text = font.render("Paramètres", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Options
        fullscreen_button = draw_button(f"Plein écran : {'Oui' if fullscreen else 'Non'}", 250, 200, 300, 50, GREEN, RED)
        volume_button = draw_button(f"Volume : {volume}%", 250, 300, 300, 50, GREEN, RED)

        # Bouton Retour
        back_button = draw_button("Retour", 10, SCREEN_HEIGHT - 60, 100, 40, BLUE, RED)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return
                if fullscreen_button.collidepoint(event.pos):
                    fullscreen = not fullscreen
                    if fullscreen:
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    else:
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                if volume_button.collidepoint(event.pos):
                    volume = (volume + 10) % 110

        pygame.display.flip()

# Lancer le menu principal
if __name__ == "__main__":
    main_menu()
    pygame.quit()
    sys.exit()
