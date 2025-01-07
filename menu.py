import pygame
import sys
import time

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

# Animation de chargement
def loading_screen(message="Chargement..."):
    screen.fill(GRAY)
    text = font.render(message, True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    time.sleep(1)  # Simulation de chargement

# Fonction pour dessiner les boutons
def draw_button(text, x, y, width, height, color, hover_color):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    if button_rect.collidepoint((mouse_x, mouse_y)):
        pygame.draw.rect(screen, hover_color, button_rect)
    else:
        pygame.draw.rect(screen, color, button_rect)

    text_surface = button_font.render(text, True, WHITE)
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

    return button_rect

# Saisie des noms des joueurs
def player_names(game_name):
    running = True
    input_box1 = pygame.Rect(300, 200, 200, 50)
    input_box2 = pygame.Rect(300, 300, 200, 50)
    color_inactive = GRAY
    color_active = GREEN
    color1 = color_inactive
    color2 = color_inactive
    active1 = False
    active2 = False
    text1 = ""
    text2 = ""

    while running:
        screen.fill(WHITE)

        # Titre
        title_text = font.render(f"{game_name} - Noms des joueurs", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Boutons pour Règles et Retour
        rules_button = draw_button("Règles", SCREEN_WIDTH - 120, SCREEN_HEIGHT - 60, 100, 40, BLUE, RED)
        back_button = draw_button("Retour", 10, SCREEN_HEIGHT - 60, 100, 40, BLUE, RED)

        # Entrées de texte
        pygame.draw.rect(screen, color1, input_box1, 2)
        pygame.draw.rect(screen, color2, input_box2, 2)
        name1_text = button_font.render(text1 if text1 else "Joueur 1", True, BLACK)
        name2_text = button_font.render(text2 if text2 else "Joueur 2", True, BLACK)
        screen.blit(name1_text, (input_box1.x + 10, input_box1.y + 10))
        screen.blit(name2_text, (input_box2.x + 10, input_box2.y + 10))

        # Bouton pour démarrer le jeu
        start_button = draw_button("Commencer", 300, 400, 200, 50, GREEN, RED)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Activation des boîtes de saisie
                active1 = input_box1.collidepoint(event.pos)
                active2 = input_box2.collidepoint(event.pos)
                color1 = color_active if active1 else color_inactive
                color2 = color_active if active2 else color_inactive

                # Boutons
                if rules_button.collidepoint(event.pos):
                    show_rules(game_name)
                if back_button.collidepoint(event.pos):
                    loading_screen("Retour...")
                    return
                if start_button.collidepoint(event.pos):
                    name1 = text1 if text1.strip() else "Joueur 1"
                    name2 = text2 if text2.strip() else "Joueur 2"
                    print(f"Le jeu démarre avec : {name1} et {name2}")
                    return

            if event.type == pygame.KEYDOWN:
                # Entrée de texte
                if active1:
                    if event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode
                elif active2:
                    if event.key == pygame.K_BACKSPACE:
                        text2 = text2[:-1]
                    else:
                        text2 += event.unicode

        pygame.display.flip()

# Afficher les règles
def show_rules(game_name):
    running = True
    while running:
        screen.fill(WHITE)

        # Titre
        title_text = font.render(f"Règles de {game_name}", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Exemple de règles
        rules_text = small_font.render("Voici les règles de ce jeu...", True, BLACK)
        screen.blit(rules_text, (50, 150))

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

        pygame.display.flip()

# Sélection de jeu
def game_selection():
    running = True
    while running:
        screen.fill(GRAY)

        # Titre
        title_text = font.render("Choisissez un jeu", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Boutons de jeu
        katarenga_button = draw_button("Katarenga", 150, 200, 200, 100, GREEN, RED)
        congress_button = draw_button("Congress", 400, 200, 200, 100, GREEN, RED)
        isolation_button = draw_button("Isolation", 275, 350, 200, 100, GREEN, RED)

        # Bouton Retour
        back_button = draw_button("Retour", 10, SCREEN_HEIGHT - 60, 100, 40, BLUE, RED)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    loading_screen("Retour...")
                    return
                if katarenga_button.collidepoint(event.pos):
                    loading_screen("Chargement...")
                    player_names("Katarenga")
                if congress_button.collidepoint(event.pos):
                    loading_screen("Chargement...")
                    player_names("Congress")
                if isolation_button.collidepoint(event.pos):
                    loading_screen("Chargement...")
                    player_names("Isolation")

        pygame.display.flip()

# Menu principal
def main_menu():
    running = True
    while running:
        screen.fill(BLUE)

        # Titre
        title_text = font.render("Katarenga", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Boutons
        start_button = draw_button("Lancer le jeu", 300, 200, 200, 50, GREEN, RED)
        quit_button = draw_button("Quitter", 300, 300, 200, 50, GREEN, RED)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_selection()
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

# Lancer le programme
if __name__ == "__main__":
    main_menu()
