import pygame
import sys
import socket
import threading
import time
from ui.colors import WHITE, BLACK, GREEN, HOVER_GREEN, BLUE, HOVER_BLUE, RED, HOVER_RED, GRAY
from ui.buttons import draw_button, click_sound
from ui.animations import loading_screen
from network import init_network

# Variables globales pour la gestion réseau
SERVER_PORT = 5555
client_socket = None
server_socket = None
connection = None
server_thread = None
is_connected = False

def start_server():
    """Démarre un serveur en attente de connexion"""
    global server_socket, connection, is_connected
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', SERVER_PORT))
    server_socket.listen(1)
    
    print(f"[SERVEUR] En attente de connexion sur le port {SERVER_PORT}...")
    connection, address = server_socket.accept()
    print(f"[SERVEUR] Connexion établie avec {address}")
    is_connected = True

def server_thread_function():
    """Fonction exécutée dans un thread séparé pour le serveur"""
    try:
        start_server()
    except Exception as e:
        print(f"[ERREUR SERVEUR] {e}")

def connect_to_server(ip_address):
    """Se connecte à un serveur existant"""
    global client_socket, is_connected
    
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_address, SERVER_PORT))
        print(f"[CLIENT] Connecté au serveur {ip_address}:{SERVER_PORT}")
        is_connected = True
        return True
    except Exception as e:
        print(f"[ERREUR CLIENT] {e}")
        return False

def send_data(data):
    """Envoie des données au joueur distant"""
    if client_socket:
        try:
            client_socket.send(str(data).encode())
            return True
        except:
            return False
    elif connection:
        try:
            connection.send(str(data).encode())
            return True
        except:
            return False
    return False

def receive_data():
    """Reçoit des données du joueur distant"""
    if client_socket:
        try:
            return client_socket.recv(1024).decode()
        except:
            return None
    elif connection:
        try:
            return connection.recv(1024).decode()
        except:
            return None
    return None

def close_connection():
    """Ferme toutes les connexions réseau"""
    global client_socket, server_socket, connection, is_connected
    
    if client_socket:
        client_socket.close()
        client_socket = None
    
    if connection:
        connection.close()
        connection = None
    
    if server_socket:
        server_socket.close()
        server_socket = None
    
    is_connected = False

def network_config(screen, fonts, game_name):
    """Menu de configuration réseau"""
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    running = True
    mode = None  # 'host' ou 'join'
    ip_address = "127.0.0.1"
    input_active = False
    connection_status = ""
    is_connected = False
    network_manager = None
    
    def start_server_thread():
        nonlocal is_connected, connection_status, network_manager
        try:
            network_manager = init_network(is_host=True)
            if network_manager.start_server():
                is_connected = True
                connection_status = "Joueur connecté! Prêt à commencer."
            else:
                connection_status = "Échec du démarrage du serveur."
        except Exception as e:
            connection_status = f"Erreur: {str(e)}"
    
    while running:
        screen.fill(WHITE)
        
        # Titre
        title_text = fonts['title'].render(f"{game_name} - Mode Réseau", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))
        
        if mode is None:
            # Choix du mode
            host_button = draw_button(screen, fonts, "Héberger une partie", screen_width // 2 - 150, 150, 300, 60, GREEN, HOVER_GREEN)
            join_button = draw_button(screen, fonts, "Rejoindre une partie", screen_width // 2 - 150, 250, 300, 60, BLUE, HOVER_BLUE)
        elif mode == 'host':
            # Afficher l'IP locale
            local_ip = socket.gethostbyname(socket.gethostname())
            ip_text = fonts['button'].render(f"Votre IP: {local_ip}", True, BLACK)
            screen.blit(ip_text, (screen_width // 2 - ip_text.get_width() // 2, 150))
            
            status_text = fonts['button'].render("En attente d'un joueur...", True, BLACK)
            screen.blit(status_text, (screen_width // 2 - status_text.get_width() // 2, 200))
            
            if connection_status:
                status_msg = fonts['small'].render(connection_status, True, GREEN if is_connected else RED)
                screen.blit(status_msg, (screen_width // 2 - status_msg.get_width() // 2, 250))
                
            if is_connected:
                start_game_button = draw_button(screen, fonts, "Commencer la partie", screen_width // 2 - 150, 300, 300, 60, GREEN, HOVER_GREEN)
        elif mode == 'join':
            # Saisie de l'adresse IP
            ip_label = fonts['button'].render("Adresse IP du serveur:", True, BLACK)
            screen.blit(ip_label, (screen_width // 2 - 150, 150))
            
            input_rect = pygame.Rect(screen_width // 2 - 150, 200, 300, 50)
            pygame.draw.rect(screen, GREEN if input_active else GRAY, input_rect, 2)
            
            ip_display = fonts['button'].render(ip_address, True, BLACK)
            screen.blit(ip_display, (input_rect.x + 10, input_rect.y + 15))
            
            connect_button = draw_button(screen, fonts, "Se connecter", screen_width // 2 - 100, 280, 200, 50, GREEN, HOVER_GREEN)
            
            if connection_status:
                status_msg = fonts['small'].render(connection_status, True, GREEN if is_connected else RED)
                screen.blit(status_msg, (screen_width // 2 - status_msg.get_width() // 2, 350))
                
            if is_connected:
                ready_button = draw_button(screen, fonts, "Prêt", screen_width // 2 - 100, 400, 200, 50, GREEN, HOVER_GREEN)
        
        # Bouton retour toujours présent
        back_button = draw_button(screen, fonts, "Retour", 10, screen_height - 60, 100, 40, RED, HOVER_RED)
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if network_manager:
                    network_manager.close()
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode is None:
                    if host_button.collidepoint(event.pos):
                        if click_sound:
                            click_sound.play()
                        mode = 'host'
                        # Lancer le serveur dans un thread séparé
                        server_thread = threading.Thread(target=start_server_thread)
                        server_thread.daemon = True
                        server_thread.start()
                        
                    if join_button.collidepoint(event.pos):
                        if click_sound:
                            click_sound.play()
                        mode = 'join'
                        
                elif mode == 'host':
                    if is_connected and 'start_game_button' in locals() and start_game_button.collidepoint(event.pos):
                        if click_sound:
                            click_sound.play()
                        # On retourne au menu précédent avec les infos de connexion
                        return True, 'host', network_manager
                        
                elif mode == 'join':
                    if input_rect.collidepoint(event.pos):
                        input_active = True
                        
                    if 'connect_button' in locals() and connect_button.collidepoint(event.pos):
                        if click_sound:
                            click_sound.play()
                        # Tenter de se connecter au serveur
                        connection_status = "Connexion en cours..."
                        network_manager = init_network(is_host=False)
                        if network_manager.connect_to_server(ip_address):
                            is_connected = True
                            connection_status = "Connecté! En attente du début de la partie..."
                        else:
                            connection_status = "Échec de la connexion."
                            
                    if is_connected and 'ready_button' in locals() and ready_button.collidepoint(event.pos):
                        if click_sound:
                            click_sound.play()
                        # On retourne au menu précédent avec les infos de connexion
                        return True, 'client', network_manager
                
                if back_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    if network_manager:
                        network_manager.close()
                    return False, None, None
                    
            if event.type == pygame.KEYDOWN and mode == 'join' and input_active:
                if event.key == pygame.K_BACKSPACE:
                    ip_address = ip_address[:-1]
                elif event.key == pygame.K_RETURN:
                    input_active = False
                elif event.unicode.isprintable():
                    ip_address += event.unicode
        
        pygame.display.flip()