import random

def checkQuart(quart: list) -> bool:
    """
        Vérifie si un quadrant de 4x4 est valide.
        Un quadrant est valide s'il contient exactement 4 couleurs différentes,
        chacune apparaissant exactement 4 fois.
    """
    colors = {'blue': 0, 'green': 0, 'red': 0, 'yellow': 0}
    for i in range(len(quart)):
        for elt in quart[i]:
            if elt in colors.keys():
                colors[elt] += 1
    for valeurs in colors.values():
        if valeurs != 4:
            return False
    return True

def genererQuart() -> list:
    """
        Génère un quadrant valide de 4x4 avec 4 couleurs différentes.
        Chaque couleur doit apparaître exactement 4 fois.
    """
    couleurs = ('blue', 'green', 'red', 'yellow')
    quart = [[couleurs[random.randrange(0, 4)] for j in range(4)] for i in range(4)]
    while not checkQuart(quart):
        quart = [[couleurs[random.randrange(0, 4)] for j in range(4)] for i in range(4)]
    return quart

class Case:
    """
        Classe représentant une case du plateau de jeu.
        Chaque case a une couleur, des coordonnées (x, y) et un dictionnaire de déplacements possibles.
    """
    def __init__(self, couleur: str, x: int, y: int):
        self.color = couleur
        self.x = x
        self.y = y
        self.dico = {
            'blue': [(self.x - 1, self.y - 1), (self.x - 1, self.y), (self.x - 1, self.y + 1),
                     (self.x, self.y + 1), (self.x + 1, self.y + 1), (self.x + 1, self.y),
                     (self.x + 1, self.y - 1), (self.x, self.y - 1)],
            'green': [(self.x - 2, self.y - 1), (self.x - 2, self.y + 1), (self.x - 1, self.y + 2),
                      (self.x + 1, self.y + 2), (self.x + 2, self.y + 1), (self.x + 2, self.y - 1),
                      (self.x + 1, self.y - 2), (self.x - 1, self.y - 2)],
            'red': [(-1, 0), (0, 1), (1, 0), (0, -1)],
            'yellow': [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        }
        self.deplacement = self.dico[self.color]

    def getColor(self):
        return self.color

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getMoves(self):
        return self.deplacement

def init_region():
    couleurs = ["blue", "green", "red", "yellow"]
    couleurs_reparties = 4 * couleurs
    random.shuffle(couleurs_reparties)
    grille = [couleurs_reparties[i:i + 4] for i in range(0, 16, 4)]
    return grille

class Init_Board:
    """
        Classe pour initialiser le plateau de jeu à partir de 4 quadrants.
        Chaque quadrant est une liste de listes représentant une grille 4x4.
    """
    def __init__(self, quart_1, quart_2, quart_3, quart_4):
        self.q1 = quart_1
        self.q2 = quart_2
        self.q3 = quart_3
        self.q4 = quart_4
        self.board = self.assembler_plateau()

    def degres_90(self, quart):
        return [list(row) for row in zip(*quart[::-1])]

    def degres_180(self, quart):
        return [row[::-1] for row in quart[::-1]]

    def degres_270(self, quart):
        return [list(row) for row in zip(*quart)][::-1]

    def symetrie(self, quart):
        return [row[::-1] for row in quart]

    def assembler_plateau(self):
        plateau = []
        for i in range(4):
            plateau.append(self.q1[i] + self.q2[i])
        for i in range(4):
            plateau.append(self.q3[i] + self.q4[i])
        return plateau

class Board:
    """
        Classe représentant le plateau de jeu.
        Le plateau est une grille de cases, chaque case ayant une couleur et des coordonnées.
    """
    def __init__(self, plateau):
        self.plateau = plateau
        self.cases = [[Case(cell, x, y) for y, cell in enumerate(row)] for x, row in enumerate(plateau)]

    def get_case(self, x, y):
        if 0 <= x < len(self.cases) and 0 <= y < len(self.cases[0]):
            return self.cases[x][y]
        return None