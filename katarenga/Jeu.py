import sys
import pygame
import os

# Ajouter le répertoire parent au chemin de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importer le module quadrants
from quadrants import genererQuart, Init_Board, Case, Board

# Le reste du code de Jeu.py
# ...

# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Katarenga")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (52, 152, 219)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
GRAY = (200, 200, 200)

# Taille des cases
CASE_SIZE = 60

# Police
font = pygame.font.Font(None, 36)

class Katarenga:
    def __init__(self):
        # Générer les quadrants
        q1 = genererQuart()
        q2 = genererQuart()
        q3 = genererQuart()
        q4 = genererQuart()

        # Initialiser le plateau
        init_board = Init_Board(q1, q2, q3, q4)
        self.plateau = init_board.board

        # Créer le plateau de jeu
        self.board = Board(self.plateau)
        self.pions = {'Joueur 1': [], 'Joueur 2': []}  # Stocker les pions des joueurs

        # Placer les pions initiaux
        self.placer_pion('Joueur 1', 0, 0)
        self.placer_pion('Joueur 1', 0, 1)
        self.placer_pion('Joueur 2', 7, 7)
        self.placer_pion('Joueur 2', 7, 6)

    def placer_pion(self, joueur, x, y):
        if self.board.get_case(x, y) and not any(pion['position'] == (x, y) for pion in self.pions[joueur]):
            self.pions[joueur].append({'position': (x, y), 'capture': False})
            return True
        return False

    def deplacer_pion(self, joueur, x_depart, y_depart, x_arrivee, y_arrivee):
        case_depart = self.board.get_case(x_depart, y_depart)
        case_arrivee = self.board.get_case(x_arrivee, y_arrivee)

        if not case_depart or not case_arrivee:
            return False

        # Vérifier si le déplacement est valide
        if (x_arrivee, y_arrivee) in case_depart.getMoves():
            # Vérifier si la case d'arrivée est occupée par un pion adverse
            for autre_joueur, pions in self.pions.items():
                if autre_joueur != joueur:
                    for pion in pions:
                        if pion['position'] == (x_arrivee, y_arrivee):
                            pion['capture'] = True  # Capturer le pion adverse
                            break

            # Mettre à jour la position du pion
            for pion in self.pions[joueur]:
                if pion['position'] == (x_depart, y_depart):
                    pion['position'] = (x_arrivee, y_arrivee)
                    break
            return True
        return False

    def verifier_victoire(self, joueur):
        # Vérifier si le joueur a atteint les camps adverses
        camps_adverses = [(0, 0), (0, 1), (1, 0), (1, 1)] if joueur == 'Joueur 1' else [(7, 7), (7, 6), (6, 7), (6, 6)]
        for pion in self.pions[joueur]:
            if pion['position'] in camps_adverses:
                return True
        return False

    def afficher_plateau(self):
        for x in range(8):
            for y in range(8):
                case = self.board.get_case(x, y)
                couleur_case = BLUE if case.getColor() == 'blue' else GREEN if case.getColor() == 'green' else RED if case.getColor() == 'red' else WHITE
                pygame.draw.rect(screen, couleur_case, (y * CASE_SIZE, x * CASE_SIZE, CASE_SIZE, CASE_SIZE))
                pygame.draw.rect(screen, BLACK, (y * CASE_SIZE, x * CASE_SIZE, CASE_SIZE, CASE_SIZE), 2)

        # Afficher les pions
        for joueur, pions in self.pions.items():
            for pion in pions:
                x, y = pion['position']
                couleur_pion = BLUE if joueur == 'Joueur 1' else RED
                pygame.draw.circle(screen, couleur_pion, (y * CASE_SIZE + CASE_SIZE // 2, x * CASE_SIZE + CASE_SIZE // 2), CASE_SIZE // 3)

# Fonction principale du jeu
def jouer_katarenga():
    jeu = Katarenga()
    clock = pygame.time.Clock()
    joueur_actuel = 'Joueur 1'
    running = True

    while running:
        screen.fill(WHITE)
        jeu.afficher_plateau()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x_case = y // CASE_SIZE
                y_case = x // CASE_SIZE

                if hasattr(jouer_katarenga, 'x_depart'):
                    x_arrivee, y_arrivee = x_case, y_case
                    if jeu.deplacer_pion(joueur_actuel, jouer_katarenga.x_depart, jouer_katarenga.y_depart, x_arrivee, y_arrivee):
                        if jeu.verifier_victoire(joueur_actuel):
                            print(f"{joueur_actuel} a gagné !")
                            running = False
                        joueur_actuel = 'Joueur 2' if joueur_actuel == 'Joueur 1' else 'Joueur 1'
                    del jouer_katarenga.x_depart
                else:
                    jouer_katarenga.x_depart, jouer_katarenga.y_depart = x_case, y_case

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Lancer le jeu
if __name__ == "__main__":
    jouer_katarenga()