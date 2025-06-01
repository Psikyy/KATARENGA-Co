import socket
import threading
import json
import uuid

class GameServer:
    def __init__(self, host='0.0.0.0', port=12345):  # Changé de 'localhost' à '0.0.0.0'
        self.host = host
        self.port = port
        self.clients = {}
        self.rooms = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        """Démarre le serveur"""
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        
        # Affichage de l'IP locale pour que votre ami puisse s'y connecter
        local_ip = self.get_local_ip()
        print(f"Serveur démarré sur {self.host}:{self.port}")
        print(f"Votre ami peut se connecter à : {local_ip}:{self.port}")
        
        while True:
            client_socket, addr = self.socket.accept()
            print(f"Nouvelle connexion de {addr}")
            
            client_id = str(uuid.uuid4())
            self.clients[client_id] = {
                'socket': client_socket,
                'address': addr,
                'room_id': None
            }
            
            self.send_to_client(client_id, {
                'type': 'player_id',
                'id': client_id
            })
            
            thread = threading.Thread(
                target=self.handle_client,
                args=(client_id,),
                daemon=True
            )
            thread.start()

    def get_local_ip(self):
        """Récupère l'IP locale de la machine"""
        try:
            # Créer une connexion temporaire pour obtenir l'IP locale
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            temp_socket.connect(("8.8.8.8", 80))
            local_ip = temp_socket.getsockname()[0]
            temp_socket.close()
            return local_ip
        except:
            return "127.0.0.1"

    def handle_client(self, client_id):
        """Gère les messages d'un client"""
        client = self.clients[client_id]
        
        while True:
            try:
                data = client['socket'].recv(1024).decode('utf-8')
                if not data:
                    break
                    
                message = json.loads(data)
                self.process_message(client_id, message)
                
            except Exception as e:
                print(f"Erreur avec le client {client_id}: {e}")
                break
        
        self.disconnect_client(client_id)

    def process_message(self, client_id, message):
        msg_type = message.get('type')
        
        if msg_type == 'create_room':
            self.create_room(client_id, message.get('room_name', 'Room sans nom'))
        elif msg_type == 'join_room':
            self.join_room(client_id, message.get('room_id'))
        elif msg_type == 'get_rooms':
            self.send_room_list(client_id)
        elif msg_type == 'game_move':
            self.broadcast_game_move(client_id, message)

    def create_room(self, client_id, room_name):
        room_id = str(uuid.uuid4())[:8]
        self.rooms[room_id] = {
            'id': room_id,
            'name': room_name,
            'players': [client_id],
            'max_players': 2,
            'game_state': None
        }
        self.clients[client_id]['room_id'] = room_id
        self.send_to_client(client_id, {
            'type': 'room_created',
            'room_id': room_id,
            'room_name': room_name
        })
        print(f"Room '{room_name}' créée avec l'ID: {room_id}")

    def join_room(self, client_id, room_id):
        if room_id not in self.rooms:
            self.send_to_client(client_id, {
                'type': 'error',
                'message': 'Room introuvable'
            })
            return
        
        room = self.rooms[room_id]
        if len(room['players']) >= room['max_players']:
            self.send_to_client(client_id, {
                'type': 'error',
                'message': 'Room pleine'
            })
            return
        
        if client_id not in room['players']:
            room['players'].append(client_id)
        
        self.clients[client_id]['room_id'] = room_id
        self.send_to_client(client_id, {
            'type': 'room_joined',
            'room_id': room_id,
            'room_name': room['name']
        })

        for player_id in room['players']:
            if player_id != client_id:
                self.send_to_client(player_id, {
                    'type': 'player_joined',
                    'player_id': client_id
                })

    def send_room_list(self, client_id):
        available_rooms = []
        for room_id, room in self.rooms.items():
            if len(room['players']) < room['max_players']:
                available_rooms.append({
                    'id': room_id,
                    'name': room['name'],
                    'players': len(room['players']),
                    'max_players': room['max_players']
                })
        self.send_to_client(client_id, {
            'type': 'room_list',
            'rooms': available_rooms
        })

    def broadcast_game_move(self, sender_id, message):
        sender = self.clients[sender_id]
        room_id = sender['room_id']
        if not room_id or room_id not in self.rooms:
            return
        room = self.rooms[room_id]
        for player_id in room['players']:
            if player_id != sender_id:
                self.send_to_client(player_id, message)

    def send_to_client(self, client_id, message):
        if client_id in self.clients:
            try:
                self.clients[client_id]['socket'].send(
                    json.dumps(message).encode('utf-8')
                )
            except Exception as e:
                print(f"Erreur envoi message à {client_id}: {e}")

    def disconnect_client(self, client_id):
        if client_id not in self.clients:
            return
        
        client = self.clients[client_id]
        room_id = client['room_id']
        
        if room_id and room_id in self.rooms:
            room = self.rooms[room_id]
            if client_id in room['players']:
                room['players'].remove(client_id)
            if not room['players']:
                del self.rooms[room_id]
            else:
                for player_id in room['players']:
                    self.send_to_client(player_id, {
                        'type': 'player_left',
                        'player_id': client_id
                    })
        try:
            client['socket'].close()
        except:
            pass
        del self.clients[client_id]
        print(f"Client {client_id} déconnecté")

if __name__ == "__main__":
    server = GameServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nArrêt du serveur...")
        server.socket.close()

# import socket
# import threading
# import json
# import uuid

# class GameServer:
#     def __init__(self, host='localhost', port=12345):
#         self.host = host
#         self.port = port
#         self.clients = {}
#         self.rooms = {}
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#     def start(self):
#         """Démarre le serveur"""
#         self.socket.bind((self.host, self.port))
#         self.socket.listen(5)
#         print(f"Serveur démarré sur {self.host}:{self.port}")
        
#         while True:
#             client_socket, addr = self.socket.accept()
#             print(f"Nouvelle connexion de {addr}")
            
#             client_id = str(uuid.uuid4())
#             self.clients[client_id] = {
#                 'socket': client_socket,
#                 'address': addr,
#                 'room_id': None
#             }
            
#             self.send_to_client(client_id, {
#                 'type': 'player_id',
#                 'id': client_id
#             })
            
#             thread = threading.Thread(
#                 target=self.handle_client,
#                 args=(client_id,),
#                 daemon=True
#             )
#             thread.start()

#     def handle_client(self, client_id):
#         """Gère les messages d'un client"""
#         client = self.clients[client_id]
        
#         while True:
#             try:
#                 data = client['socket'].recv(1024).decode('utf-8')
#                 if not data:
#                     break
                    
#                 message = json.loads(data)
#                 self.process_message(client_id, message)
                
#             except Exception as e:
#                 print(f"Erreur avec le client {client_id}: {e}")
#                 break
        
#         self.disconnect_client(client_id)

#     def process_message(self, client_id, message):
#         msg_type = message.get('type')
        
#         if msg_type == 'create_room':
#             self.create_room(client_id, message.get('room_name', 'Room sans nom'))
#         elif msg_type == 'join_room':
#             self.join_room(client_id, message.get('room_id'))
#         elif msg_type == 'get_rooms':
#             self.send_room_list(client_id)
#         elif msg_type == 'game_move':
#             self.broadcast_game_move(client_id, message)

#     def create_room(self, client_id, room_name):
#         room_id = str(uuid.uuid4())[:8]
#         self.rooms[room_id] = {
#             'id': room_id,
#             'name': room_name,
#             'players': [client_id],
#             'max_players': 2,
#             'game_state': None
#         }
#         self.clients[client_id]['room_id'] = room_id
#         self.send_to_client(client_id, {
#             'type': 'room_created',
#             'room_id': room_id,
#             'room_name': room_name
#         })
#         print(f"Room '{room_name}' créée avec l'ID: {room_id}")

#     def join_room(self, client_id, room_id):
#         if room_id not in self.rooms:
#             self.send_to_client(client_id, {
#                 'type': 'error',
#                 'message': 'Room introuvable'
#             })
#             return
        
#         room = self.rooms[room_id]
#         if len(room['players']) >= room['max_players']:
#             self.send_to_client(client_id, {
#                 'type': 'error',
#                 'message': 'Room pleine'
#             })
#             return
        
#         if client_id not in room['players']:
#             room['players'].append(client_id)
        
#         self.clients[client_id]['room_id'] = room_id
#         self.send_to_client(client_id, {
#             'type': 'room_joined',
#             'room_id': room_id,
#             'room_name': room['name']
#         })

#         for player_id in room['players']:
#             if player_id != client_id:
#                 self.send_to_client(player_id, {
#                     'type': 'player_joined',
#                     'player_id': client_id
#                 })

#     def send_room_list(self, client_id):
#         available_rooms = []
#         for room_id, room in self.rooms.items():
#             if len(room['players']) < room['max_players']:
#                 available_rooms.append({
#                     'id': room_id,
#                     'name': room['name'],
#                     'players': len(room['players']),
#                     'max_players': room['max_players']
#                 })
#         self.send_to_client(client_id, {
#             'type': 'room_list',
#             'rooms': available_rooms
#         })

#     def broadcast_game_move(self, sender_id, message):
#         sender = self.clients[sender_id]
#         room_id = sender['room_id']
#         if not room_id or room_id not in self.rooms:
#             return
#         room = self.rooms[room_id]
#         for player_id in room['players']:
#             if player_id != sender_id:
#                 self.send_to_client(player_id, message)

#     def send_to_client(self, client_id, message):
#         if client_id in self.clients:
#             try:
#                 self.clients[client_id]['socket'].send(
#                     json.dumps(message).encode('utf-8')
#                 )
#             except Exception as e:
#                 print(f"Erreur envoi message à {client_id}: {e}")

#     def disconnect_client(self, client_id):
#         if client_id not in self.clients:
#             return
        
#         client = self.clients[client_id]
#         room_id = client['room_id']
        
#         if room_id and room_id in self.rooms:
#             room = self.rooms[room_id]
#             if client_id in room['players']:
#                 room['players'].remove(client_id)
#             if not room['players']:
#                 del self.rooms[room_id]
#             else:
#                 for player_id in room['players']:
#                     self.send_to_client(player_id, {
#                         'type': 'player_left',
#                         'player_id': client_id
#                     })
#         try:
#             client['socket'].close()
#         except:
#             pass
#         del self.clients[client_id]
#         print(f"Client {client_id} déconnecté")

# if __name__ == "__main__":
#     server = GameServer()
#     try:
#         server.start()
#     except KeyboardInterrupt:
#         print("\nArrêt du serveur...")
#         server.socket.close()
