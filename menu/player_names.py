import pygame
import sys
from ui.colors import WHITE, BLACK, GREEN, GRAY, BLUE, RED
from ui.buttons import draw_button, click_sound
from ui.animations import loading_screen

from games.katarenga.board import configure_board as configure_katarenga_board
from games.isolation.board import configure_board as configure_isolation_board
from games.katarenga.game import start_game as start_katarenga_game
from games.isolation.game import start_game as start_isolation_game





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

        # Zones de texte
        input_rect1 = pygame.Rect(250, 200, 300, 50)
        input_rect2 = pygame.Rect(250, 300, 300, 50)
        pygame.draw.rect(screen, GREEN if input_active1 else GRAY, input_rect1, 2)
        pygame.draw.rect(screen, GREEN if input_active2 else GRAY, input_rect2, 2)

        # Affichage du texte
        player1_display = fonts['title'].render(player1_name if player1_name else "Joueur 1", True, BLACK)
        player2_display = fonts['title'].render(player2_name if player2_name else "Joueur 2", True, BLACK)
        screen.blit(player1_display, (input_rect1.x + 10, input_rect1.y + 10))
        screen.blit(player2_display, (input_rect2.x + 10, input_rect2.y + 10))

        # Bouton Retour
        back_button = draw_button(screen, fonts, "Retour", 10, screen_height - 60, 100, 40, BLUE, RED)

        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect1.collidepoint(event.pos):
                    input_active1 = True
                    input_active2 = False
                elif input_rect2.collidepoint(event.pos):
                    input_active1 = False
                    input_active2 = True

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
                    elif event.unicode.isalnum():
                        player1_name += event.unicode
                elif input_active2:
                    if event.key == pygame.K_BACKSPACE:
                        player2_name = player2_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if not player1_name:
                            player1_name = "Joueur 1"
                        if not player2_name:
                            player2_name = "Joueur 2"
                        if player1_name == player2_name:
                            player1_name += "(1)"
                            player2_name += "(2)"

                        print(f"Jeu sélectionné : {game_name}")
                        print(f"Joueur 1 : {player1_name}")
                        print(f"Joueur 2 : {player2_name}")

                        if game_name == "Katarenga":
                            selected_quadrants = configure_katarenga_board(screen, fonts)
                            start_katarenga_game(screen, fonts, player1_name, player2_name, selected_quadrants)
                        elif game_name == "Isolation":
                            selected_quadrants = configure_isolation_board(screen, fonts)
                            start_isolation_game(screen, fonts, player1_name, player2_name, selected_quadrants)
                        else:
                            print(f"[ERREUR] Mode inconnu : {game_name}")
                        return
                    elif event.unicode.isalnum():
                        player2_name += event.unicode

        pygame.display.flip()
