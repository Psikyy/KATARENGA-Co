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
    Cette classe représente une case du plateau de jeu. 
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


"""
    Classe 'Init_Board_Color'
    Cette classe initialise le plateau de jeu avec les 4 quadrants.
"""
class Init_Board_Color:
    def __init__(self, quart_1: list, quart_2: list, quart_3: list, quart_4: list):
        self.q1 = quart_1
        self.q2 = quart_2
        self.q3 = quart_3
        self.q4 = quart_4
        self.board = self.create_board()
    
    def getQuart1(self) -> list:
        return self.q1
    
    def getQuart2(self) -> list:
        return self.q2
    
    def getQuart3(self) -> list:
        return self.q3
    
    def getQuart4(self) -> list:
        return self.q4
    
    def getBoard(self) -> list:
        return self.board

    @staticmethod
    def rotate_quadrant(quadrant, rotation):
        """
            Applique une rotation à un quadrant.
            :param quadrant: Le quadrant à tourner.
            :param rotation: 0 (0°), 1 (90°), 2 (180°), 3 (270°), 4 en mirroir (ou symétrie axiale).
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
        elif rotation == 4:
            return [row[::-1] for row in quadrant] # Mirroir horizontal
        else:
            raise ValueError("Rotation invalide. Doit être 0, 1, 2 ou 3.")

    def create_board(self):
        board = []
        bord_top = ['2','0', '0', '0', '0', '0', '0', '0', '0', '2']
        bord_bottom = ['1','0', '0', '0', '0', '0', '0', '0', '0', '1']
        board.append(bord_top)
        plateau = [['0'] + row[:] for row in self.quart1]
        
        for i in range(4):
            plateau[i].extend(self.quart2[i] + ['0'])
        
        for i in range(4):
            plateau.append(['0'] + self.quart3[i])
            
        for i in range(4):
            plateau[i + 4].extend(self.quart4[i] + ['0'])

        
        for i in range(8):
            board.append(plateau[i])
        
        board.append(bord_bottom)
        self.plateau = board
        return self.plateau

    def rotate_quadrant(self, quadrant: list, rotation: int) -> list:
        """
            Applique une rotation à un quadrant.
            :param quadrant: Le quadrant à tourner.
            :param rotation: 0 (0°), 1 (90°), 2 (180°), 3 (270°), 4 en mirroir.
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
        elif rotation == 4:
            return self.mirroir(quadrant)
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
    
    def mirroir(self, liste : list) -> list:
        """
            Renvoie un cadrant après avoir appliqué un effet mirroir dessus
        """
        l = []
        for ligne in liste:
            l.append(ligne[::-1])
        return l
"""
    Fin classe 'Init_Board'
"""



"""
    Classe 'Init_Board_Pawn'
    Cette classe initialise le plateau de jeu avec les pions.
"""
class Init_Board_Pawn:
    def __init__(self, P1sPawn = 8, P2sPawn = 8):
        self.P1sPawn = P1sPawn
        self.P2sPawn = P2sPawn
        self.board = self.create_board()
    
    def getPlayer1sPawn(self) -> int:
        return self.P1sPawn
    
    def getPlayer2sPawn(self) -> int:
        return self.P2sPawn
    
    def getBoard(self) -> list:
        return self.board
    
    def setPlayer1sPawn(self, P1sPawn: int) -> None:
        self.P1sPawn = P1sPawn
    
    def setPlayer2sPawn(self, P2sPawn: int) -> None:
        self.P2sPawn = P2sPawn

    def create_board(self):
        board = []
        bord_top = ['2', '0', '0', '0', '0', '0', '0', '0', '0', '2']
        bord_bottom = ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1']
        Ekip1 = ['0', 1, 1, 1, 1, 1, 1, 1, 1, '0']
        Ekip2 = ['0', 2, 2, 2, 2, 2, 2, 2, 2, '0']
        board.append(bord_top)
        board.append(Ekip2)
        for _ in range(6):
            board.append([None] * 10)
        board.append(Ekip1)
        board.append(bord_bottom)
        self.board = board
        return board
"""
    Fin classe 'Init_Board_Pawn'
"""

# Première version des fonctions de déplacement et de verrification de déplacement

def movePawn(pawn : tuple, case : tuple, board_pawn : Init_Board_Pawn) -> None:
    """
        Déplace un pion 'pawn' sur une case 'case' dans un plateau de jeu 'board_pawn'
    """
    x, y = pawn
    i, j = case
    board_pawn.board[i][j] = board_pawn.board[x][y]
    board_pawn.board[x][y] = None

def checkCanMove(pawn : tuple, case : tuple, board_pawn : Init_Board_Pawn) -> bool:
    """
        Vérifie si un pion peut se déplacer sur une case 'case'
    """
    if board_pawn.board[case[0]][case[1]] == '0':
        return False
    x, y = pawn
    i, j = case
    if board_pawn.board[i][j] is None:
        return True
    return False

def checkNoAllyInCase(pawn : tuple, case : tuple, board_pawn : Init_Board_Pawn) -> bool:
    """
        Vérifie si la case où l'on veut déplacer un pion est vide
    """
    if board_pawn.board[case[0]][case[1]] == '0':
        return False
    x, y = pawn
    i, j = case
    if board_pawn.board[i][j] == 0:
        return True
    return False

def checkCanCapture(pawn : tuple, case : tuple, board_pawn : Init_Board_Pawn) -> bool:
    """
        Vérifie si un pion peut capturer un autre pion sur la case 'case'
    """
    if board_pawn.board[case[0]][case[1]] == '0':
        return False
    x, y = pawn
    i, j = case
    if board_pawn.board[i][j] is not None and board_pawn.board[i][j] != board_pawn.board[x][y]:
        return True
    return False

def getYellowCases(board_color : Init_Board_Color) -> list:
    """
        Renvoie la liste des cases jaunes du plateau de jeu
    """
    yellow_cases = []
    for i in range(10):
        for j in range(10):
            if board_color.board[i][j] == "yellow":
                yellow_cases.append((i, j))
    return yellow_cases

def checkYellow(pawn : tuple, case : tuple, tab_Y : list) -> bool:
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

def getRedCases(board_color : Init_Board_Color) -> list:
    """
        Renvoie la liste des cases rouges du plateau de jeu
    """
    red_cases = []
    for i in range(10):
        for j in range(10):
            if board_color.board[i][j] == "red":
                red_cases.append((i, j))
    return red_cases

def checkRed(pawn : tuple, case : tuple, tab_R : list) -> bool:
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

# Première version de la win condition

def gameIsOver(board_pawn : Init_Board_Pawn) -> tuple:
    """
        Verrifie si la partie est terminée
        Si un des joueur à capturé le camp adverse ou si il ne reste qu'un pion ou moins à l'un des joueurs
    """
    if board_pawn.board[0][0] == 1 and board_pawn.board[0][9] == 1:
        return (1, True)
    elif board_pawn.board[9][0] == 2 and board_pawn.board[9][9] == 2:
        return (2, True)
    elif board_pawn.P2sPawn <= 1:
        return (1, True)
    elif board_pawn.P1sPawn <= 1:
        return (2, True)
    else:
        return False

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
        self.board_Color = Init_Board_Color(self.quart1, self.quart2, self.quart3, self.quart4)
        self.board_Pawn = Init_Board_Pawn()
        return self.board_Color, self.board_Pawn

    def get_board(self):
        return self.board_Color, self.board_Pawn