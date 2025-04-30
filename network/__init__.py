# Module d'initialisation pour le réseau
from network.network_manager import NetworkManager

# Instance globale du gestionnaire réseau
network_manager = None

def init_network(is_host=False):
    """Initialise le gestionnaire réseau"""
    global network_manager
    network_manager = NetworkManager(is_host)
    return network_manager

def get_network_manager():
    """Retourne l'instance du gestionnaire réseau"""
    global network_manager
    if not network_manager:
        network_manager = NetworkManager()
    return network_manager