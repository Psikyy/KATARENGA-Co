import socket
import threading
import json
import time

class NetworkManager:
    """
    Gestionnaire de communication réseau pour les jeux
    Permet de synchroniser les états de jeu entre deux joueurs
    """
    def __init__(self, is_host=False):
        self.is_host = is_host
        self.socket = None
        self.connection = None
        self.connected = False
        self.server_thread = None
        self.receive_thread = None
        self.callback = None
        self.running = False
        self.port = 5555
        
    def start_server(self):
        """Démarre un serveur en attente de connexion"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(('0.0.0.0', self.port))
            self.socket.listen(1)
            
            print(f"[SERVEUR] En attente de connexion sur le port {self.port}...")
            self.connection, address = self.socket.accept()
            print(f"[SERVEUR] Connexion établie avec {address}")
            self.connected = True
            
            # Démarrer le thread de réception
            self.running = True
            self.receive_thread = threading.Thread(target=self._receive_data_loop)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            return True
        except Exception as e:
            print(f"[ERREUR SERVEUR] {e}")
            return False
            
    def connect_to_server(self, ip_address):
        """Se connecte à un serveur existant"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((ip_address, self.port))
            print(f"[CLIENT] Connecté au serveur {ip_address}:{self.port}")
            self.connected = True
            
            # Démarrer le thread de réception
            self.running = True
            self.receive_thread = threading.Thread(target=self._receive_data_loop)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            return True
        except Exception as e:
            print(f"[ERREUR CLIENT] {e}")
            return False
            
    def send_game_state(self, game_state):
        """
        Envoie l'état du jeu au joueur distant
        game_state: un dictionnaire contenant l'état du jeu
        """
        if not self.connected:
            return False
            
        try:
            # Convertir l'état du jeu en JSON
            data = json.dumps(game_state).encode()
            
            # Envoyer la taille des données suivie des données
            size = len(data)
            size_bytes = size.to_bytes(4, byteorder='big')
            
            if self.is_host:
                self.connection.sendall(size_bytes)
                self.connection.sendall(data)
            else:
                self.socket.sendall(size_bytes)
                self.socket.sendall(data)
                
            return True
        except Exception as e:
            print(f"[ERREUR ENVOI] {e}")
            self.connected = False
            return False
            
    def send_move(self, move_data):
        """
        Envoie un mouvement au joueur distant
        move_data: un dictionnaire contenant les informations du mouvement
        """
        return self.send_game_state({"type": "move", "data": move_data})
        
    def send_chat_message(self, message):
        """Envoie un message de chat à l'autre joueur"""
        return self.send_game_state({"type": "chat", "message": message})
        
    def _receive_data_loop(self):
        """Thread de réception des données"""
        connection = self.connection if self.is_host else self.socket
        
        while self.running:
            try:
                # Recevoir d'abord la taille des données
                size_bytes = self._receive_all(connection, 4)
                if not size_bytes:
                    break
                    
                size = int.from_bytes(size_bytes, byteorder='big')
                
                # Puis recevoir les données
                data = self._receive_all(connection, size)
                if not data:
                    break
                    
                # Décoder et traiter les données
                game_state = json.loads(data.decode())
                
                # Si un callback est défini, l'appeler avec les données reçues
                if self.callback:
                    self.callback(game_state)
                    
            except Exception as e:
                print(f"[ERREUR RÉCEPTION] {e}")
                break
                
        self.connected = False
        print("[RÉSEAU] Déconnecté")
        
    def _receive_all(self, sock, n):
        """Reçoit exactement n octets depuis la socket"""
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
        
    def set_callback(self, callback):
        """Définit la fonction de callback pour les données reçues"""
        self.callback = callback
        
    def close(self):
        """Ferme la connexion"""
        self.running = False
        
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
                
        self.socket = None
        self.connection = None
        self.connected = False