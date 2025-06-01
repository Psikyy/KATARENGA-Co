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
        self.current_room_name = None
        self.player_id = None
        self.players_in_room = []
        self.is_room_creator = False
        self.server_host = "localhost"
        self.server_port = 12345

    def connect_to_server(self):
        """Connection au serv"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
            self.connected = True
            
            listen_thread = threading.Thread(target=self.listen_server, daemon=True)
            listen_thread.start()
            
            return True
        except Exception as e:
            print(f"Erreur de connexion au serveur: {e}")
            self.connected = False
            return False

    def listen_server(self):
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
        
        if msg_type == 'player_id':
            self.player_id = message.get('id')
            
        elif msg_type == 'room_list':
            self.rooms = message.get('rooms', [])
            
        elif msg_type == 'room_created':
            self.current_room = message.get('room_id')
            self.current_room_name = message.get('room_name')
            self.is_room_creator = True
            self.players_in_room = [{'id': self.player_id, 'name': 'Vous (Créateur)'}]
            
        elif msg_type == 'room_joined':
            self.current_room = message.get('room_id')
            self.current_room_name = message.get('room_name')
            self.is_room_creator = False
            self.players_in_room = [{'id': self.player_id, 'name': 'Vous'}]
            
        elif msg_type == 'room_players':
            other_players = message.get('players', [])
            
            for player_id in other_players:
                if player_id != self.player_id:
                    self.players_in_room.append({
                        'id': player_id, 
                        'name': f'Joueur {player_id[:8]}...'
                    })
            
        elif msg_type == 'player_joined':
            new_player_id = message.get('player_id')
            
            if not any(p['id'] == new_player_id for p in self.players_in_room):
                self.players_in_room.append({
                    'id': new_player_id,
                    'name': f'Joueur {new_player_id[:8]}...'
                })
                
        elif msg_type == 'player_left':
            player_id = message.get('player_id')
            self.players_in_room = [p for p in self.players_in_room if p.get('id') != player_id]
            
        elif msg_type == 'game_start':
            print("Jeu démarré!")
            
        elif msg_type == 'error':
            error_msg = message.get('message', 'Erreur inconnue')
            print(f"Erreur du serveur: {error_msg}")

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

    def leave_room(self):
        """Quitte la room actuelle"""
        if self.current_room:
            message = {
                'type': 'leave_room',
                'room_id': self.current_room
            }
            self.send_message(message)
            self.current_room = None
            self.current_room_name = None
            self.players_in_room = []
            self.is_room_creator = False

    def start_game(self):
        """Démarre le jeu (seulement pour le créateur)"""
        if self.is_room_creator and self.current_room:
            message = {
                'type': 'start_game',
                'room_id': self.current_room
            }
            self.send_message(message)

    def get_rooms(self):
        """Demande la liste des rooms disponibles"""
        message = {'type': 'get_rooms'}
        self.send_message(message)

    def disconnect(self):
        """Se déconnecte du serveur"""
        if self.current_room:
            self.leave_room()
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

def draw_room_waiting_screen(screen, fonts, online_manager):
    """Affiche l'écran d'attente dans une room"""
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    screen.fill(WHITE)
    
    title_text = fonts['title'].render(f"Room: {online_manager.current_room_name}", True, BLACK)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))
    
    if online_manager.is_room_creator:
        status_text = fonts['large'].render("Vous êtes l'hôte - En attente de joueurs...", True, GREEN)
    else:
        status_text = fonts['large'].render("En attente du début de partie...", True, BLUE)
    
    screen.blit(status_text, (screen_width // 2 - status_text.get_width() // 2, 120))
    
    players_title = fonts['large'].render(f"Joueurs connectés ({len(online_manager.players_in_room)}/2):", True, BLACK)
    screen.blit(players_title, (screen_width // 2 - players_title.get_width() // 2, 180))
    
    y_offset = 220
    for i, player in enumerate(online_manager.players_in_room):
        player_name = player.get('name', f"Joueur {player.get('id', 'Inconnu')[:8]}...")
        color = GREEN  
        
        player_text = fonts['medium'].render(f"• {player_name}", True, color)
        screen.blit(player_text, (screen_width // 2 - player_text.get_width() // 2, y_offset + i * 40))
    
    button_y = screen_height - 150
    
    if online_manager.is_room_creator and len(online_manager.players_in_room) >= 2:
        start_button = draw_button(
            screen, fonts, "Démarrer la partie",
            screen_width // 2 - 150, button_y,
            300, 50,
            GREEN, HOVER_GREEN
        )
    else:
        start_button = None
        if online_manager.is_room_creator:
            waiting_text = fonts['medium'].render("En attente d'au moins 2 joueurs pour démarrer", True, GREY)
            screen.blit(waiting_text, (screen_width // 2 - waiting_text.get_width() // 2, button_y + 10))
    
    leave_button = draw_button(
        screen, fonts, "Quitter la room",
        screen_width // 2 - 100, button_y + 70,
        200, 40,
        RED, HOVER_RED
    )
    
    return start_button, leave_button

def katarenga_online_menu(screen, fonts):
    """Menu principal du mode en ligne"""
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    online_manager = OnlineManager()
    running = True
    connecting = False
    
    room_name_input = ""
    room_name_active = False
    show_create_room = False
    
    button_width = 300
    button_height = 60
    
    while running:
        screen.fill(WHITE)
        
        if online_manager.current_room:
            start_button, leave_button = draw_room_waiting_screen(screen, fonts, online_manager)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    online_manager.disconnect()
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if leave_button.collidepoint(event.pos):
                        if click_sound:
                            click_sound.play()
                        online_manager.leave_room()
                    elif start_button and start_button.collidepoint(event.pos):
                        if click_sound:
                            click_sound.play()
                        online_manager.start_game()
                        print("Démarrage du jeu!")
            
            pygame.display.flip()
            continue
        
        title_text = fonts['title'].render("Mode En Ligne - Katarenga", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 30))
        
        room_name_rect = None
        create_room_button = None
        confirm_create_button = None
        cancel_create_button = None
        refresh_button = None
        connect_button = None
        
        if not online_manager.connected and not connecting:
            connect_text = fonts['medium'].render("Connexion au serveur requise", True, BLACK)
            screen.blit(connect_text, (screen_width // 2 - connect_text.get_width() // 2, 150))
            
            connect_button = draw_button(
                screen, fonts, "Se connecter",
                screen_width // 2 - button_width // 2, 200,
                button_width, button_height,
                GREEN, HOVER_GREEN
            )
            
        elif connecting:
            loading_text = fonts['medium'].render("Connexion en cours...", True, BLACK)
            screen.blit(loading_text, (screen_width // 2 - loading_text.get_width() // 2, 250))
            
        elif online_manager.connected:
            status_text = fonts['medium'].render("Connecté au serveur", True, GREEN)
            screen.blit(status_text, (screen_width // 2 - status_text.get_width() // 2, 100))
            
            create_title = fonts['large'].render("Créer une Room", True, BLACK)
            screen.blit(create_title, (50, 150))
            
            create_room_button = draw_button(
                screen, fonts, "Créer une nouvelle room",
                50, 190, button_width, button_height,
                GREEN, HOVER_GREEN
            )
            
            if show_create_room:
                room_name_label = fonts['medium'].render("Nom de la Room:", True, BLACK)
                screen.blit(room_name_label, (50, 280))
                
                room_name_rect = draw_text_input(
                    screen, fonts, room_name_input or "Entrez le nom de la room",
                    50, 310, 300, 40, room_name_active
                )
                
                confirm_create_button = draw_button(
                    screen, fonts, "Créer",
                    370, 310, 120, 40,
                    GREEN, HOVER_GREEN
                )
                
                cancel_create_button = draw_button(
                    screen, fonts, "Annuler",
                    500, 310, 120, 40,
                    RED, HOVER_RED
                )

            rooms_title = fonts['large'].render("Rooms Disponibles", True, BLACK)
            screen.blit(rooms_title, (screen_width - 400, 150))
            
            refresh_button = draw_button(
                screen, fonts, "Actualiser",
                screen_width - 400, 180, 150, 30,
                BLUE, HOVER_BLUE
            )
            
            y_offset = 220
            room_buttons = []
            for i, room in enumerate(online_manager.rooms[:5]):  
                room_name = room.get('name', 'Sans nom')
                room_id = room.get('id', 'N/A')
                players_count = room.get('players', 0)
                max_players = room.get('max_players', 2)
                
                room_text = fonts['small'].render(f"{room_name} ({players_count}/{max_players})", True, BLACK)
                screen.blit(room_text, (screen_width - 400, y_offset + i * 60))
                
                if players_count < max_players:
                    join_room_button = draw_button(
                        screen, fonts, "Rejoindre",
                        screen_width - 400, y_offset + i * 60 + 20, 100, 30,
                        BLUE, HOVER_BLUE
                    )
                    room_buttons.append((join_room_button, room_id))
                else:
                    full_text = fonts['small'].render("Pleine", True, RED)
                    screen.blit(full_text, (screen_width - 400, y_offset + i * 60 + 25))
        
        back_button = draw_button(
            screen, fonts, t("back"),
            10, screen_height - 60,
            100, 40,
            BLUE, HOVER_BLUE
        )
        
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
                    if connect_button and connect_button.collidepoint(event.pos):
                        if click_sound:
                            click_sound.play()
                        connecting = True
                        def connect():
                            nonlocal connecting
                            success = online_manager.connect_to_server()
                            connecting = False
                            if success:
                                online_manager.get_rooms()
                        
                        connect_thread = threading.Thread(target=connect, daemon=True)
                        connect_thread.start()
                
                elif online_manager.connected:
                    for button, room_id in room_buttons:
                        if button.collidepoint(event.pos):
                            if click_sound:
                                click_sound.play()
                            online_manager.join_room(room_id)
                            break
                    
                    if create_room_button and create_room_button.collidepoint(event.pos):
                        if click_sound:
                            click_sound.play()
                        show_create_room = not show_create_room
                        room_name_input = ""
                        room_name_active = False
                    elif refresh_button and refresh_button.collidepoint(event.pos):
                        if click_sound:
                            click_sound.play()
                        online_manager.get_rooms()
                    
                    if show_create_room:
                        if room_name_rect and room_name_rect.collidepoint(event.pos):
                            room_name_active = True
                        elif confirm_create_button and confirm_create_button.collidepoint(event.pos) and room_name_input.strip():
                            if click_sound:
                                click_sound.play()
                            online_manager.create_room(room_name_input.strip())
                            show_create_room = False
                            room_name_input = ""
                            room_name_active = False
                        elif cancel_create_button and cancel_create_button.collidepoint(event.pos):
                            if click_sound:
                                click_sound.play()
                            show_create_room = False
                            room_name_input = ""
                            room_name_active = False
                    else:
                        if room_name_active:
                            room_name_active = False
            
            if event.type == pygame.KEYDOWN:
                if room_name_active:
                    if event.key == pygame.K_BACKSPACE:
                        room_name_input = room_name_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        if room_name_input.strip():
                            online_manager.create_room(room_name_input.strip())
                            show_create_room = False
                            room_name_input = ""
                            room_name_active = False
                    else:
                        room_name_input += event.unicode

        pygame.display.flip()

if __name__ == "__main__":
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