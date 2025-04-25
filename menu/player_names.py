import pygame
import sys
from ui.colors import WHITE, BLACK, GREEN, GRAY, BLUE, RED
from ui.buttons import draw_button, click_sound
from ui.animations import loading_screen
from games.katarenga.board import configure_board

def start_game(screen, fonts, player1_name, player2_name, game_name, selected_quadrants=None):
    """
    Démarre le jeu avec les noms des joueurs et la configuration du plateau (si applicable).
    """
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    running = True

    while running:
        screen.fill(WHITE)

        # Titre du jeu
        title_text = fonts['title'].render(f"{game_name}", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))

        # Affichage des joueurs
        player_text1 = fonts['small'].render(f"Joueur 1 : {player1_name}", True, BLACK)
        player_text2 = fonts['small'].render(f"Joueur 2 : {player2_name}", True, BLACK)
        screen.blit(player_text1, (screen_width // 2 - player_text1.get_width() // 2, 200))
        screen.blit(player_text2, (screen_width // 2 - player_text2.get_width() // 2, 250))

        # Dessiner le plateau si c'est Katarenga
        if game_name == "Katarenga" and selected_quadrants:
            from games.katarenga.board import draw_board
            draw_board(screen, fonts, selected_quadrants)

        # Bouton Retour
        back_button = draw_button(screen, fonts, "Retour", 10, screen_height - 60, 100, 40, BLUE, RED)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    loading_screen(screen, fonts, "Retour...")
                    return

        pygame.display.flip()

def player_names(screen, fonts, game_name):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    running = True
    player1_name = ""
    player2_name = ""
    input_active1 = True
    input_active2 = False

    while running:
        screen.fill(WHITE)

        # Titre
        title_text = fonts['title'].render(f"{game_name}", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))

        # Instructions
        instruction_text = fonts['small'].render("Entrez les noms des joueurs sans espaces ni caractères spéciaux.", True, BLACK)
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, 100))

        # Zones de texte pour les noms
        input_rect1 = pygame.Rect(250, 200, 300, 50)
        input_rect2 = pygame.Rect(250, 300, 300, 50)
        pygame.draw.rect(screen, GREEN if input_active1 else GRAY, input_rect1, 2)
        pygame.draw.rect(screen, GREEN if input_active2 else GRAY, input_rect2, 2)

        # Texte des zones de saisie
        player1_display = fonts['title'].render(player1_name if player1_name else "Joueur 1", True, BLACK)
        player2_display = fonts['title'].render(player2_name if player2_name else "Joueur 2", True, BLACK)
        screen.blit(player1_display, (input_rect1.x + 10, input_rect1.y + 10))
        screen.blit(player2_display, (input_rect2.x + 10, input_rect2.y + 10))

        # Bouton Retour
        back_button = draw_button(screen, fonts, "Retour", 10, screen_height - 60, 100, 40, BLUE, RED)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Activer ou désactiver les zones de saisie
                if input_rect1.collidepoint((mouse_x, mouse_y)):
                    input_active1 = True
                    input_active2 = False
                elif input_rect2.collidepoint((mouse_x, mouse_y)):
                    input_active1 = False
                    input_active2 = True

                # Retour
                if back_button.collidepoint(event.pos):
                    loading_screen(screen, fonts, "Retour...")
                    return

            if event.type == pygame.KEYDOWN:
                if input_active1:
                    if event.key == pygame.K_BACKSPACE:
                        player1_name = player1_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        input_active1 = False
                        input_active2 = True
                    elif event.unicode.isalnum():  # Empêche les espaces et caractères spéciaux
                        player1_name += event.unicode
                elif input_active2:
                    if event.key == pygame.K_BACKSPACE:
                        player2_name = player2_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        # Validation des noms
                        if not player1_name:
                            player1_name = "Joueur 1"
                        if not player2_name:
                            player2_name = "Joueur 2"
                        
                        # Ajouter des suffixes si les noms sont identiques
                        if player1_name == player2_name:
                            player1_name += "(1)"
                            player2_name += "(2)"
                        
                        # Afficher les noms dans la console
                        print(f"Jeu sélectionné : {game_name}")
                        print(f"Joueur 1 : {player1_name}")
                        print(f"Joueur 2 : {player2_name}")

                        # Démarrer le jeu après la validation des noms
                        if game_name == "Katarenga":
                            selected_quadrants = configure_board(screen, fonts)  # Appelle la configuration du plateau
                            start_game(screen, fonts, player1_name, player2_name, game_name, selected_quadrants)
                        else:
                            start_game(screen, fonts, player1_name, player2_name, game_name)
                        return
                    elif event.unicode.isalnum():  # Empêche les espaces et caractères spéciaux
                        player2_name += event.unicode

        pygame.display.flip()