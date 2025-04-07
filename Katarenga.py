import random


def checkQuart(quart: list) -> bool:
    """
        Renvoie un booléen qui indique si le cadrant créé est valide ou non
    """
    colors = {'blue': 0, 'green': 0, 'red': 0, 'yellow': 0}
    for i in range(len(quart)):
        for elt in quart[i]:
            if elt in colors.keys():
                colors[elt]+=1
    for valeurs in colors.values():
        if valeurs != 4:
            return False
    return True

def genererQuart() -> list:
    """
        Génère un cadrant valide
    """
    couleurs = ('blue', 'green', 'red', 'yellow')
    quart = [[couleurs[random.randrange(0, 4)] for j in range(4)] for i in range(4)]
    while (checkQuart(quart) == False):
        quart = [[couleurs[random.randrange(0, 4)] for j in range(4)] for i in range(4)]
    return quart


def generate_quadrants():
    """
    Génère 4 quadrants aléatoires.
    """
    return [genererQuart() for _ in range(4)]


""" 
    Classe 'Case' 
"""
class Case:
    def __init__(self, couleur : str, x : int, y : int):
        self.color = couleur
        self.x = x
        self.y = y
        self.dico = Dico_deplacement = {'blue': [(self.x-1, self.y-1), (self.x-1, self.y), (self.x-1, self.y+1), (self.x, self.y+1), (self.x+1, self.y+1), (self.x+1, self.y), (self.x+1, self.y-1), (self.x, self.y-1)],
                                        'green': [(self.x-2, self.y-1), (self.x-2, self.y-1), (self.x-1, self.y+2), (self.x+1, self.y+2), (self.x+2, self.y+1), (self.x+2, self.y-1), (self.x+1, self.y-2), (self.x-1, self.y-2)],
                                        'red': [(-1, 0), (0, 1), (1, 0), (0, -1)],
                                        'yellow': [(-1, -1), (-1, 1), (1, 1), (1, -1)]
                                       }
        self.deplacement = Dico_deplacement[self.color]
    
    def getColor(self):
        return self.color
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getMoves(self):
        return self.deplacement
"""
    Fin classe 'Case'
"""


def init_region() -> list:
    couleurs = ["blue", "green", "red", "yellow"]
    couleurs_reparties = 4*couleurs
    random.shuffle(couleurs_reparties)
    grille = [couleurs_reparties[i:i+4] for i in range(0, 16, 4)]
    return grille

"""
    Classe 'Init_Board'
"""
class Init_Board:
    def __init__(self, quart_1: list, quart_2: list, quart_3: list, quart_4: list):
        self.q1 = quart_1
        self.q2 = quart_2
        self.q3 = quart_3
        self.q4 = quart_4
        self.board = self.create_board()

class Init_Board:
    def __init__(self, quart_1: list, quart_2: list, quart_3: list, quart_4: list):
        self.q1 = quart_1
        self.q2 = quart_2
        self.q3 = quart_3
        self.q4 = quart_4
        self.board = self.create_board()

    @staticmethod
    def rotate_quadrant(quadrant, rotation):
        """
        Applique une rotation à un quadrant.
        :param quadrant: Le quadrant à tourner.
        :param rotation: 0 (0°), 1 (90°), 2 (180°), 3 (270°).
        :return: Le quadrant tourné.
        """
        if rotation == 0:
            return quadrant
        elif rotation == 1:
            return [list(row) for row in zip(*quadrant[::-1])]  # 90°
        elif rotation == 2:
            return [row[::-1] for row in quadrant[::-1]]  # 180°
        elif rotation == 3:
            return [list(row) for row in zip(*quadrant)][::-1]  # 270°
        else:
            raise ValueError("Rotation invalide. Doit être 0, 1, 2 ou 3.")

    def create_board(self) -> list:
        """
        Combine les 4 quadrants pour former le plateau complet.
        """
        board = []
        for i in range(4):
            board.append(self.q1[i] + self.q2[i])
        for i in range(4):
            board.append(self.q3[i] + self.q4[i])
        return board

    def rotate_quadrant(self, quadrant: list, rotation: int) -> list:
        """
        Applique une rotation à un quadrant.
        :param quadrant: Le quadrant à tourner.
        :param rotation: 0 (0°), 1 (90°), 2 (180°), 3 (270°).
        :return: Le quadrant tourné.
        """
        if rotation == 0:
            return quadrant
        elif rotation == 1:
            return self.degres_90(quadrant)
        elif rotation == 2:
            return self.degres_180(quadrant)
        elif rotation == 3:
            return self.degres_270(quadrant)
        else:
            raise ValueError("Rotation invalide. Doit être 0, 1, 2 ou 3.")

    def degres_90(self, quart: list) -> list:
        """
        Renvoie un quadrant tourné à 90° vers la gauche.
        """
        return [list(row) for row in zip(*quart[::-1])]

    def degres_180(self, quart: list) -> list:
        """
        Renvoie un quadrant tourné à 180°.
        """
        return [row[::-1] for row in quart[::-1]]

    def degres_270(self, quart: list) -> list:
        """
        Renvoie un quadrant tourné à 90° vers la droite.
        """
        return [list(row) for row in zip(*quart)][::-1]
"""
    Fin classe 'Init_Board'
"""

# Première version des fonctions de déplacement et de verrification de déplacement

def movePawn(pawn : tuple, case : tuple, board : list) -> None:
    """
        Déplace un pion 'pawn' sur une case 'case' dans un plateau de jeu 'board'
    """
    x, y = pawn
    i, j = case
    board[i][j] = board[x][y]
    board[x][y] = 0

def checkCaseIsEmpty(pawn : tuple, case : tuple, board : list) -> bool:
    """
        Vérifie si la case où l'on veut déplacer un pion est vide
    """
    x, y = pawn
    i, j = case
    if board[i][j] == 0:
        return True
    return False

def getYellowCases(board : list) -> list:
    """
        Renvoie la liste des cases jaunes du plateau de jeu
    """
    yellow_cases = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == "yellow":
                yellow_cases.append((i, j))
    return yellow_cases

def checkYellow(pawn : tuple, case : tuple, board : list, tab_Y : list) -> bool:
    """
        Vérifie si un déplacement est possible pour un pion partant d'une case jaune
        en s'assurant qu'il ne traverse pas d'autres cases jaunes.
    """
    temp_yellow = [elt for elt in tab_Y if elt != pawn]
    x, y = pawn
    i, j = case
    if abs(i - x) != abs(j - y):
        return False
    dx = 1 if i > x else -1
    dy = 1 if j > y else -1
    current_x, current_y = x, y
    while (current_x, current_y) != (i, j):
        current_x += dx
        current_y += dy
        if (current_x, current_y) in temp_yellow:
            return False
    return True

def getRedCases(board : list) -> list:
    """
        Renvoie la liste des cases rouges du plateau de jeu
    """
    red_cases = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == "red":
                red_cases.append((i, j))
    return red_cases

def checkRed(pawn : tuple, case : tuple, board : list, tab_R : list) -> bool:
    """
        Vérifie si un déplacement horizontal ou vertical est possible pour un pion partant d'une case rouge,
        en s'assurant qu'il ne traverse pas d'autres cases rouges.
    """
    temp_red = [elt for elt in tab_R if elt != pawn]
    x, y = pawn
    i, j = case
    if x != i and y != j:
        return False
    dx = 1 if i > x else -1 if i < x else 0
    dy = 1 if j > y else -1 if j < y else 0
    current_x, current_y = x, y
    while (current_x, current_y) != (i, j):
        current_x += dx
        current_y += dy
        if (current_x, current_y) in temp_red:
            return False
    return True




class Board:

    def __init__(self, plateau : list, board : list):
        self.plateau = plateau
        self.board = board


# regions de test 
q1 = [[1, 2, 3, 4],
      [9, 10, 11, 12],
      [17, 18, 19, 20],
      [25, 26, 27, 28]
     ]

q2 = [[5, 6, 7, 8],
      [13, 14, 15, 16],
      [21, 22, 23, 24],
      [29, 30, 31, 32]
     ]

q3 = [[33, 34, 35, 36],
      [41, 42, 43, 44],
      [49, 50, 51, 52],
      [57, 58, 59, 60]
     ]

q4 = [[37, 38, 39, 40],
      [45, 46, 47, 48],
      [53, 54, 55, 56],
      [61, 62, 63, 64]
     ]

class RestartGame:
    "On regenere différents quart pour recommencer une partie"
    def __init__(self):
        self.restart()

    "On relance la partie avec un nouveau plateau"
    def restart(self):
        self.quart1 = genererQuart()
        self.quart2 = genererQuart()
        self.quart3 = genererQuart()
        self.quart4 = genererQuart()
        self.board = Init_Board(self.quart1, self.quart2, self.quart3, self.quart4)
        return self.board

    def get_board(self):
        return self.board