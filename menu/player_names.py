import pygame
import sys
import time
from ui.colors import WHITE, BLACK, GREEN, GRAY, BLUE, RED, HOVER_GREEN
from ui.buttons import draw_button, click_sound
from ui.animations import loading_screen

from games.katarenga.board import configure_board as configure_katarenga_board
from games.isolation.board import configure_board as configure_isolation_board
from games.congress.board import configure_board as configure_congress_board
from games.katarenga.game import start_game as start_katarenga_game
from games.isolation.game import start_game as start_isolation_game
from games.congress.game import start_game as start_congress_game


def player_names(screen, fonts, game_name, network_mode=False, p1_name="", p2_name="", 
                network_role=None, network_manager=None):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    running = True
    
    # Si on est en mode réseau, on utilise les noms fournis
    if network_mode and p1_name and p2_name:
        player1_name = p1_name
        player2_name = p2_name
        input_active1 = False
        input_active2 = False
    else:
        player1_name = ""
        player2_name = ""
        input_active1 = True
        input_active2 = False

    while running:
        screen.fill(WHITE)

        # Titre
        title_text = fonts['title'].render(f"{game_name}", True, BLACK)
        title_x = screen_width // 2 - title_text.get_width() // 2
        title_y = 50
        screen.blit(title_text, (title_x, title_y))

        spacing_after_title = 20  

        # Instructions différentes selon le mode
        if network_mode:
            mode_text = "Mode Réseau - " + ("Hôte" if network_role == 'host' else "Client")
            instruction_text = fonts['small'].render(mode_text, True, BLACK)
        else:
            instruction_text = fonts['small'].render(
                "Entrez les noms des joueurs sans espaces ni caractères spéciaux.",
                True, BLACK)
        
        instruction_x = screen_width // 2 - instruction_text.get_width() // 2
        instruction_y = title_y + title_text.get_height() + spacing_after_title
        screen.blit(instruction_text, (instruction_x, instruction_y))


        # Zones de texte
        input_rect1 = pygame.Rect(250, 200, 300, 50)
        input_rect2 = pygame.Rect(250, 300, 300, 50)
        pygame.draw.rect(screen, GREEN if input_active1 else GRAY, input_rect1, 2)
        pygame.draw.rect(screen, GREEN if input_active2 else GRAY, input_rect2, 2)

        player1_label = fonts['small'].render("Joueur 1 (Rouge):", True, RED)
        player2_label = fonts['small'].render("Joueur 2 (Bleu):", True, BLUE)

        vertical_spacing = 10

        screen.blit(player1_label, (input_rect1.x, input_rect1.y - player1_label.get_height() - vertical_spacing))
        screen.blit(player2_label, (input_rect2.x, input_rect2.y - player2_label.get_height() - vertical_spacing))


        player1_display = fonts['button'].render(player1_name if player1_name else "Joueur 1", True, BLACK)
        player2_display = fonts['button'].render(player2_name if player2_name else "Joueur 2", True, BLACK)
        screen.blit(player1_display, (input_rect1.x + 10, input_rect1.y + 15))
        screen.blit(player2_display, (input_rect2.x + 10, input_rect2.y + 15))

        # Boutons
        validate_button = draw_button(screen, fonts, "Valider", screen_width // 2 - 50, 400, 100, 50, GREEN, HOVER_GREEN)
        back_button = draw_button(screen, fonts, "Retour", 10, screen_height - 60, 100, 40, BLUE, RED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if network_mode and network_manager:
                    network_manager.close()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Désactivation de la modification des noms en mode réseau
                if not network_mode:
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
                        player1_name = "Joueur 1"
                    if not player2_name:
                        player2_name = "Joueur 2"
                    if player1_name == player2_name:
                        player1_name += "(1)"
                        player2_name += "(2)"

                    print(f"Jeu sélectionné : {game_name}")
                    print(f"Joueur 1 : {player1_name}")
                    print(f"Joueur 2 : {player2_name}")
                    
                    # Gestion différente selon le mode de jeu et le rôle réseau
                    if network_mode:
                        # En mode réseau, seul l'hôte configure la partie
                        if network_role == 'host':
                            if game_name == "Katarenga":
                                selected_quadrants = configure_katarenga_board(screen, fonts)
                                # Envoyer les quadrants sélectionnés au client
                                network_manager.send_game_state({
                                    "type": "game_config",
                                    "game": game_name,
                                    "quadrants": selected_quadrants
                                })
                                start_katarenga_game(screen, fonts, player1_name, player2_name, 
                                                    selected_quadrants, network_mode=True, 
                                                    network_role=network_role, network_manager=network_manager)
                            elif game_name == "Isolation":
                                selected_quadrants = configure_isolation_board(screen, fonts)
                                network_manager.send_game_state({
                                    "type": "game_config",
                                    "game": game_name,
                                    "quadrants": selected_quadrants
                                })
                                start_isolation_game(screen, fonts, player1_name, player2_name, 
                                                     selected_quadrants, network_mode=True, 
                                                     network_role=network_role, network_manager=network_manager)
                            elif game_name == "Congress":
                                selected_quadrants = configure_congress_board(screen, fonts)
                                network_manager.send_game_state({
                                    "type": "game_config",
                                    "game": game_name,
                                    "quadrants": selected_quadrants
                                })
                                start_congress_game(screen, fonts, player1_name, player2_name, 
                                                    selected_quadrants, network_mode=True, 
                                                    network_role=network_role, network_manager=network_manager)
                        else:  # Client
                            # Attendre la configuration de la partie depuis l'hôte
                            loading_screen(screen, fonts, "Attente de la configuration de la partie...")
                            
                            # Définir un callback pour recevoir la configuration
                            received_config = [None]
                            
                            def on_config_received(data):
                                if data.get("type") == "game_config":
                                    received_config[0] = data
                            
                            network_manager.set_callback(on_config_received)
                            
                            # Attendre la réception
                            wait_start_time = time.time()
                            while received_config[0] is None:
                                pygame.event.pump()  # Garder l'interface réactive
                                
                                # Timeout après 30 secondes
                                if time.time() - wait_start_time > 30:
                                    print("[ERREUR] Timeout en attente de la configuration")
                                    return
                                
                                time.sleep(0.1)
                            
                            # Réinitialiser le callback
                            network_manager.set_callback(None)
                            
                            # Lancer le jeu avec la configuration reçue
                            game_config = received_config[0]
                            selected_quadrants = game_config.get("quadrants")
                            
                            if game_name == "Katarenga":
                                start_katarenga_game(screen, fonts, player1_name, player2_name, 
                                                    selected_quadrants, network_mode=True, 
                                                    network_role=network_role, network_manager=network_manager)
                            elif game_name == "Isolation":
                                start_isolation_game(screen, fonts, player1_name, player2_name, 
                                                     selected_quadrants, network_mode=True, 
                                                     network_role=network_role, network_manager=network_manager)
                            elif game_name == "Congress":
                                start_congress_game(screen, fonts, player1_name, player2_name, 
                                                    selected_quadrants, network_mode=True, 
                                                    network_role=network_role, network_manager=network_manager)
                    else:
                        # Mode solo (local)
                        if game_name == "Katarenga":
                            selected_quadrants = configure_katarenga_board(screen, fonts)
                            start_katarenga_game(screen, fonts, player1_name, player2_name, selected_quadrants)
                        elif game_name == "Isolation":
                            selected_quadrants = configure_isolation_board(screen, fonts)
                            start_isolation_game(screen, fonts, player1_name, player2_name, selected_quadrants)
                        elif game_name == "Congress":
                            selected_quadrants = configure_congress_board(screen, fonts)
                            start_congress_game(screen, fonts, player1_name, player2_name, selected_quadrants)
                    
                    return  # Sortir de la fonction après avoir lancé le jeu

                elif back_button.collidepoint((mouse_x, mouse_y)):
                    if click_sound:
                        click_sound.play()
                    return  # Retourner au menu précédent

            # Traitement clavier si la saisie des noms est active et qu'on n'est pas en mode réseau
            if not network_mode and event.type == pygame.KEYDOWN:
                if input_active1:
                    if event.key == pygame.K_BACKSPACE:
                        player1_name = player1_name[:-1]
                    elif event.key == pygame.K_TAB:
                        input_active1 = False
                        input_active2 = True
                    elif event.key == pygame.K_RETURN:
                        input_active1 = False
                        input_active2 = True
                    elif len(player1_name) < 15:  # Limite de caractères
                        # Accepte uniquement les lettres, chiffres et quelques caractères spéciaux
                        if event.unicode.isalnum() or event.unicode in '_-':
                            player1_name += event.unicode
                elif input_active2:
                    if event.key == pygame.K_BACKSPACE:
                        player2_name = player2_name[:-1]
                    elif event.key == pygame.K_TAB:
                        input_active1 = True
                        input_active2 = False
                    elif event.key == pygame.K_RETURN:
                        # Validation avec Entrée
                        if not player1_name:
                            player1_name = "Joueur 1"
                        if not player2_name:
                            player2_name = "Joueur 2"
                        if player1_name == player2_name:
                            player1_name += "(1)"
                            player2_name += "(2)"
                            
                        if game_name == "Katarenga":
                            selected_quadrants = configure_katarenga_board(screen, fonts)
                            start_katarenga_game(screen, fonts, player1_name, player2_name, selected_quadrants)
                        elif game_name == "Isolation":
                            selected_quadrants = configure_isolation_board(screen, fonts)
                            start_isolation_game(screen, fonts, player1_name, player2_name, selected_quadrants)
                        elif game_name == "Congress":
                            selected_quadrants = configure_congress_board(screen, fonts)
                            start_congress_game(screen, fonts, player1_name, player2_name, selected_quadrants)
                        return
                    elif len(player2_name) < 15:  # Limite de caractères
                        # Accepte uniquement les lettres, chiffres et quelques caractères spéciaux
                        if event.unicode.isalnum() or event.unicode in '_-':
                            player2_name += event.unicode

        pygame.display.flip()