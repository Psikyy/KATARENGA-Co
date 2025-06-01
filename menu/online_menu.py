import pygame
import sys
import threading
import socket
import json
from ui.colors import WHITE, BLACK, BLUE, HOVER_BLUE, GREEN, HOVER_GREEN, GREY, RED, HOVER_RED
from ui.buttons import draw_button, click_sound
from ui.animations import loading_screen
from menu.settings import t

class OnlineManager:
    def __init__(self):
        self.socket = None
        self.connected = False
        self.rooms = []
        self.current_room = None
        self.player_id = None
        self.server_host = "localhost"
        self.server_port = 12345

    def connect_to_server(self):
        """Se connecte au serveur de jeu"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
            self.connected = True
            
            # Démarrer le thread d'écoute
            listen_thread = threading.Thread(target=self.listen_server, daemon=True)
            listen_thread.start()
            
            return True
        except Exception as e:
            print(f"Erreur de connexion au serveur: {e}")
            self.connected = False
            return False

    def listen_server(self):
        """Écoute les messages du serveur"""
        while self.connected:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if data:
                    message = json.loads(data)
                    self.handle_server_message(message)
            except Exception as e:
                print(f"Erreur lors de l'écoute du serveur: {e}")
                self.connected = False
                break

    def handle_server_message(self, message):
        """Traite les messages reçus du serveur"""
        msg_type = message.get('type')
        
        if msg_type == 'room_list':
            self.rooms = message.get('rooms', [])
        elif msg_type == 'room_created':
            self.current_room = message.get('room_id')
        elif msg_type == 'room_joined':
            self.current_room = message.get('room_id')
        elif msg_type == 'player_id':
            self.player_id = message.get('id')

    def send_message(self, message):
        """Envoie un message au serveur"""
        if self.connected and self.socket:
            try:
                self.socket.send(json.dumps(message).encode('utf-8'))
            except Exception as e:
                print(f"Erreur lors de l'envoi du message: {e}")

    def create_room(self, room_name):
        """Crée une nouvelle room"""
        message = {
            'type': 'create_room',
            'room_name': room_name
        }
        self.send_message(message)

    def join_room(self, room_id):
        """Rejoint une room existante"""
        message = {
            'type': 'join_room',
            'room_id': room_id
        }
        self.send_message(message)

    def get_rooms(self):
        """Demande la liste des rooms disponibles"""
        message = {'type': 'get_rooms'}
        self.send_message(message)

    def disconnect(self):
        """Se déconnecte du serveur"""
        if self.socket:
            self.socket.close()
        self.connected = False

def draw_text_input(screen, fonts, text, x, y, width, height, active=False):
    """Dessine un champ de saisie de texte"""
    color = BLUE if active else GREY
    pygame.draw.rect(screen, WHITE, (x, y, width, height))
    pygame.draw.rect(screen, color, (x, y, width, height), 2)
    
    text_surface = fonts['medium'].render(text, True, BLACK)
    screen.blit(text_surface, (x + 10, y + height//2 - text_surface.get_height()//2))
    
    return pygame.Rect(x, y, width, height)

def katarenga_online_menu(screen, fonts):
    """Menu principal du mode en ligne"""
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    online_manager = OnlineManager()
    running = True
    connecting = False
    
    # Variables pour la création de room
    room_name_input = ""
    room_name_active = False
    show_create_room = False
    
    # Variables pour rejoindre une room
    room_id_input = ""
    room_id_active = False
    
    button_width = 300
    button_height = 60
    
    while running:
        screen.fill(WHITE)
        
        # Titre
        title_text = fonts['title'].render("Mode En Ligne - Katarenga", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 30))
        
        if not online_manager.connected and not connecting:
            # Écran de connexion
            connect_text = fonts['medium'].render("Connexion au serveur requise", True, BLACK)
            screen.blit(connect_text, (screen_width // 2 - connect_text.get_width() // 2, 150))
            
            connect_button = draw_button(
                screen, fonts, "Se connecter",
                screen_width // 2 - button_width // 2, 200,
                button_width, button_height,
                GREEN, HOVER_GREEN
            )
            
        elif connecting:
            # Écran de chargement
            loading_text = fonts['medium'].render("Connexion en cours...", True, BLACK)
            screen.blit(loading_text, (screen_width // 2 - loading_text.get_width() // 2, 250))
            
        elif online_manager.connected:
            # Menu principal en ligne
            status_text = fonts['medium'].render("Connecté au serveur", True, GREEN)
            screen.blit(status_text, (screen_width // 2 - status_text.get_width() // 2, 100))
            
            # Section rejoindre une room
            join_title = fonts['large'].render("Rejoindre une Room", True, BLACK)
            screen.blit(join_title, (50, 150))
            
            # Champ pour l'ID de la room
            room_id_label = fonts['medium'].render("ID de la Room:", True, BLACK)
            screen.blit(room_id_label, (50, 200))
            
            room_id_rect = draw_text_input(
                screen, fonts, room_id_input or "Entrez l'ID de la room",
                50, 230, 300, 40, room_id_active
            )
            
            join_button = draw_button(
                screen, fonts, "Rejoindre",
                370, 230, 120, 40,
                BLUE, HOVER_BLUE
            )
            
            # Section créer une room
            create_title = fonts['large'].render("Créer une Room", True, BLACK)
            screen.blit(create_title, (50, 320))
            
            create_room_button = draw_button(
                screen, fonts, "Créer une nouvelle room",
                50, 360, button_width, button_height,
                GREEN, HOVER_GREEN
            )
            
            # Si on est en train de créer une room
            if show_create_room:
                # Champ pour le nom de la room
                room_name_label = fonts['medium'].render("Nom de la Room:", True, BLACK)
                screen.blit(room_name_label, (50, 450))
                
                room_name_rect = draw_text_input(
                    screen, fonts, room_name_input or "Entrez le nom de la room",
                    50, 480, 300, 40, room_name_active
                )
                
                confirm_create_button = draw_button(
                    screen, fonts, "Créer",
                    370, 480, 120, 40,
                    GREEN, HOVER_GREEN
                )
                
                cancel_create_button = draw_button(
                    screen, fonts, "Annuler",
                    500, 480, 120, 40,
                    RED, HOVER_RED
                )
            
            # Liste des rooms disponibles
            rooms_title = fonts['large'].render("Rooms Disponibles", True, BLACK)
            screen.blit(rooms_title, (screen_width - 400, 150))
            
            # Bouton pour rafraîchir la liste
            refresh_button = draw_button(
                screen, fonts, "Actualiser",
                screen_width - 400, 180, 150, 30,
                BLUE, HOVER_BLUE
            )
            
            # Afficher les rooms
            y_offset = 220
            for i, room in enumerate(online_manager.rooms[:5]):  # Limiter à 5 rooms
                room_text = fonts['small'].render(f"Room: {room.get('name', 'Sans nom')} (ID: {room.get('id', 'N/A')})", True, BLACK)
                screen.blit(room_text, (screen_width - 400, y_offset + i * 30))
        
        # Bouton retour
        back_button = draw_button(
            screen, fonts, t("back"),
            10, screen_height - 60,
            100, 40,
            BLUE, HOVER_BLUE
        )
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                online_manager.disconnect()
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                    online_manager.disconnect()
                    return
                
                if not online_manager.connected and not connecting:
                    if connect_button.collidepoint(event.pos):
                        if click_sound:
                            click_sound.play()
                        connecting = True
                        # Tenter la connexion dans un thread séparé
                        def connect():
                            nonlocal connecting
                            success = online_manager.connect_to_server()
                            connecting = False
                            if success:
                                online_manager.get_rooms()
                        
                        connect_thread = threading.Thread(target=connect, daemon=True)
                        connect_thread.start()
                
                elif online_manager.connected:
                    # Gestion des clics dans le menu en ligne
                    if room_id_rect.collidepoint(event.pos):
                        room_id_active = True
                        room_name_active = False
                    elif join_button.collidepoint(event.pos) and room_id_input.strip():
                        if click_sound:
                            click_sound.play()
                        online_manager.join_room(room_id_input.strip())
                    elif create_room_button.collidepoint(event.pos):
                        if click_sound:
                            click_sound.play()
                        show_create_room = not show_create_room
                        room_name_input = ""
                    elif refresh_button.collidepoint(event.pos):
                        if click_sound:
                            click_sound.play()
                        online_manager.get_rooms()
                    
                    if show_create_room:
                        if room_name_rect.collidepoint(event.pos):
                            room_name_active = True
                            room_id_active = False
                        elif confirm_create_button.collidepoint(event.pos) and room_name_input.strip():
                            if click_sound:
                                click_sound.play()
                            online_manager.create_room(room_name_input.strip())
                            show_create_room = False
                            room_name_input = ""
                        elif cancel_create_button.collidepoint(event.pos):
                            if click_sound:
                                click_sound.play()
                            show_create_room = False
                            room_name_input = ""
                    else:
                        room_name_active = False
            
            if event.type == pygame.KEYDOWN:
                if room_id_active:
                    if event.key == pygame.K_BACKSPACE:
                        room_id_input = room_id_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        if room_id_input.strip():
                            online_manager.join_room(room_id_input.strip())
                    else:
                        room_id_input += event.unicode
                
                elif room_name_active:
                    if event.key == pygame.K_BACKSPACE:
                        room_name_input = room_name_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        if room_name_input.strip():
                            online_manager.create_room(room_name_input.strip())
                            show_create_room = False
                            room_name_input = ""
                    else:
                        room_name_input += event.unicode

        pygame.display.flip()

if __name__ == "__main__":
    # Test du module
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Test Online Menu")
    
    fonts = {
        'title': pygame.font.Font(None, 48),
        'large': pygame.font.Font(None, 36),
        'medium': pygame.font.Font(None, 24),
        'small': pygame.font.Font(None, 18)
    }
    
    katarenga_online_menu(screen, fonts)