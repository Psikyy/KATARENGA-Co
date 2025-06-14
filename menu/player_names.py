import pygame
import sys
from ui.colors import WHITE, BLACK, GREEN, GRAY, BLUE, RED, HOVER_GREEN
from ui.buttons import draw_button, click_sound
from ui.animations import loading_screen

from menu.settings import t

from games.katarenga.board import configure_board as configure_katarenga_board
from games.isolation.board import configure_board as configure_isolation_board
from games.congress.board import configure_board as configure_congress_board
from games.katarenga.game import start_game as start_katarenga_game
from games.isolation.game import start_game as start_isolation_game
from games.congress.game import start_game as start_congress_game


def player_names(screen, fonts, game_name, mode=None):
    """
        Affiche le menu de saisie des noms des joueurs.
    : screen : l'écran Pygame sur lequel dessiner
    : fonts : un dictionnaire de polices de caractères
    : game_name : le nom du jeu sélectionné
    : mode : le mode de jeu (local, bot, etc.)
    """
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    running = True
    player1_name = ""
    player2_name = ""
    input_active1 = True
    input_active2 = False

    while running:
        screen.fill(WHITE)

        title_text = fonts['title'].render(f"{game_name}", True, BLACK)
        title_x = screen_width // 2 - title_text.get_width() // 2
        title_y = 50
        screen.blit(title_text, (title_x, title_y))

        spacing_after_title = 20  

        instruction_text = fonts['small'].render(
            t("enter_names"),
            True, BLACK)
        instruction_x = screen_width // 2 - instruction_text.get_width() // 2
        instruction_y = title_y + title_text.get_height() + spacing_after_title
        screen.blit(instruction_text, (instruction_x, instruction_y))

        input_rect1 = pygame.Rect(250, 200, 300, 50)
        input_rect2 = pygame.Rect(250, 300, 300, 50)
        pygame.draw.rect(screen, GREEN if input_active1 else GRAY, input_rect1, 2)
        pygame.draw.rect(screen, GREEN if input_active2 else GRAY, input_rect2, 2)

        player1_label = fonts['small'].render(t("enter_player1"), True, RED)
        player2_label = fonts['small'].render(t("enter_player2"), True, BLUE)

        vertical_spacing = 10

        screen.blit(player1_label, (input_rect1.x, input_rect1.y - player1_label.get_height() - vertical_spacing))
        screen.blit(player2_label, (input_rect2.x, input_rect2.y - player2_label.get_height() - vertical_spacing))


        player1_display = fonts['button'].render(player1_name if player1_name else t("default_player1"), True, BLACK)
        player2_display = fonts['button'].render(player2_name if player2_name else t("default_player2"), True, BLACK)
        screen.blit(player1_display, (input_rect1.x + 10, input_rect1.y + 15))
        screen.blit(player2_display, (input_rect2.x + 10, input_rect2.y + 15))

        validate_button = draw_button(screen, fonts, t("validate"), screen_width // 2 - 50, 400, 100, 50, GREEN, HOVER_GREEN)
        back_button = draw_button(screen, fonts, t("back"), 10, screen_height - 60, 100, 40, BLUE, RED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                if input_rect1.collidepoint(event.pos):
                    input_active1 = True
                    input_active2 = False
                elif input_rect2.collidepoint(event.pos):
                    input_active1 = False
                    input_active2 = True

                if validate_button.collidepoint((mouse_x, mouse_y)):
                    if click_sound:
                        click_sound.play()

                    if not player1_name:
                        player1_name = t("default_player1")
                    if not player2_name:
                        player2_name = t("default_player2")
                    if player1_name == player2_name:
                        player1_name += "(1)"
                        player2_name += "(2)"

                    print(t("game_selected") + game_name)
                    print(t("default_player1") + player1_name)
                    print(t("default_player2") + player2_name)

                    if game_name == "Katarenga":
                        selected_quadrants = configure_katarenga_board(screen, fonts)
                        start_katarenga_game(screen, fonts, player1_name, player2_name, selected_quadrants, mode=mode)
                    elif game_name == "Isolation":
                        selected_quadrants = configure_isolation_board(screen, fonts)
                        start_isolation_game(screen, fonts, player1_name, player2_name, selected_quadrants, mode=mode)
                    elif game_name == "Congress":
                        selected_quadrants = configure_congress_board(screen, fonts)
                        start_congress_game(screen, fonts, player1_name, player2_name, selected_quadrants, mode=mode)
                    else:
                        print(f"[ERREUR] Mode inconnu : {game_name}")
                    return

                if back_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    loading_screen(screen, fonts, t("back_loading"))
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
                            player1_name = t("default_player1")
                        if not player2_name:
                            player2_name = t("default_player2")
                        if player1_name == player2_name:
                            player1_name += "(1)"
                            player2_name += "(2)"

                        print(t("game_selected") + game_name)
                        print(t("default_player1") + player1_name)
                        print(t("default_player2") + player2_name)

                        if game_name == "Katarenga":
                            selected_quadrants = configure_katarenga_board(screen, fonts)
                            start_katarenga_game(screen, fonts, player1_name, player2_name, selected_quadrants, mode=mode)
                        elif game_name == "Isolation":
                            selected_quadrants = configure_isolation_board(screen, fonts)
                            start_isolation_game(screen, fonts, player1_name, player2_name, selected_quadrants, mode=mode)
                        elif game_name == "Congress":
                            selected_quadrants = configure_congress_board(screen, fonts)
                            start_congress_game(screen, fonts, player1_name, player2_name, selected_quadrants, mode=mode)   
                        else:
                            print(f"[ERREUR] Mode inconnu : {game_name}")
                        return
                    elif event.unicode.isalnum():
                        player2_name += event.unicode

        pygame.display.flip()
