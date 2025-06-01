import random


def checkQuart(quart: list) -> bool:
    """
        Renvoie un booléen qui indique si le cadrant créé est valide ou non
        c'est à dire si il contient bien 4 fois 4 couleurs différentes
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
        Génère un cadrant valide aléatoire et le renvoie
        C'est à dire un cadrant de 4x4 avec 4 couleurs différentes
    """
    couleurs = ('blue', 'green', 'red', 'yellow')
    quart = [[couleurs[random.randrange(0, 4)] for j in range(4)] for i in range(4)]
    while (checkQuart(quart) == False):
        quart = [[couleurs[random.randrange(0, 4)] for j in range(4)] for i in range(4)]
    return quart


""" 
    Classe 'Case'
    Cette classe représente une case du plateau de jeu. 
"""
class Case:
    def __init__(self, couleur : str, x : int, y : int):
        self.color = couleur
        self.x = x
        self.y = y
        # Dictionnaire de déplacement pour chaque couleur
        # 'blue' se déplace comme un roi
        # 'green' se déplace comme un cavalier
        # 'red' se déplace comme une tour
        # 'yellow' se déplace comme un fou
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

    @staticmethod
    def rotate_quadrant(quadrant, rotation) -> list:
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


    def create_board(self) -> list:
        """
            Crée le plateau de jeu en combinant les 4 quadrants.
        """
        board = []
        bord_top = ['2','0', '0', '0', '0', '0', '0', '0', '0', '2'] # bordure du haut avec les emplacements capturables
        bord_bottom = ['1','0', '0', '0', '0', '0', '0', '0', '0', '1'] # bordure du bas avec les emplacements capturables
        board.append(bord_top)
        plateau = [['0'] + row[:] for row in self.q1] # Ici " '0' " est ajouté tout au long du programme pour former les bordures
        
        for i in range(4):
            plateau[i].extend(self.q2[i] + ['0'])
        
        for i in range(4):
            plateau.append(['0'] + self.q3[i])
            
        for i in range(4):
            plateau[i + 4].extend(self.q4[i] + ['0'])

        
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
    
    def affichage_test(self) -> None:
        """
            Affiche le plateau de jeu dans la console afin de pouvoir tester et verifier visuelement.
        """
        for ligne in self.plateau:
            print(" ".join(str(cell).ljust(6) for cell in ligne))
            print("\n")
    
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

    def create_board(self) -> list:
        """
            Crée le plateau de jeu avec les pions.
        """
        board = []
        bord_top = ['2', '0', '0', '0', '0', '0', '0', '0', '0', '2'] # bordure du haut avec les emplacements capturables
        bord_bottom = ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'] # bordure du bas avec les emplacements capturables
        Ekip1 = ['0', 1, 1, 1, 1, 1, 1, 1, 1, '0'] # initialisation de l'équipe 1
        Ekip2 = ['0', 2, 2, 2, 2, 2, 2, 2, 2, '0'] # initialisation de l'équipe 2
        board.append(bord_top)
        board.append(Ekip2)
        for _ in range(6):
            line = ['0', None, None, None, None, None, None, None, None, '0'] # ligne de None ou aucun pion ne s'y trouve
            board.append(line)
        board.append(Ekip1)
        board.append(bord_bottom)
        self.board = board
        return board
    
    def affichage_test(self) -> None:
        """
            Affiche le plateau de jeu dans la console afin de pouvoir tester et verifier visuelement.
        """
        for ligne in self.board:
            print(" ".join(str(cell).ljust(6) for cell in ligne))
            print("\n")
    
"""
    Fin classe 'Init_Board_Pawn'
"""

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
        Renvoie un booléen qui indique si un pion peut se déplacer sur une case 'case'
    """
    if board_pawn.board[case[0]][case[1]] == '0':
        return False
    elif board_pawn.board[case[0]][case[1]] == 1 and board_pawn.board[pawn[0]][pawn[1]] == '1':
        return False
    elif board_pawn.board[case[0]][case[1]] == 2 and board_pawn.board[pawn[0]][pawn[1]] == '2':
        return False
    x, y = pawn
    i, j = case
    if board_pawn.board[i][j] is None:
        return True
    return False

def checkCanCapture(pawn : tuple, case : tuple, board_pawn : Init_Board_Pawn) -> bool:
    """
        Renvoie un booléen qui indique si un pion peut capturer un autre pion sur la case 'case'
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
        Renvoie une liste de coordonnées où se trouve uniquement des cases jaunes du plateau
    """
    yellow_cases = []
    for i in range(10):
        for j in range(10):
            if board_color.board[i][j] == "yellow":
                yellow_cases.append((i, j))
    return yellow_cases

def checkYellow(pawn : tuple, case : tuple, tab_Y : list) -> bool:
    """
        Renvoie un booléen qui indique si un déplacement est possible pour un pion partant d'une case jaune
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
        Renvoie une liste de coordonnées où se trouve uniquement des cases rouges du plateau
    """
    red_cases = []
    for i in range(10):
        for j in range(10):
            if board_color.board[i][j] == "red":
                red_cases.append((i, j))
    return red_cases

def checkRed(pawn : tuple, case : tuple, tab_R : list) -> bool:
    """
        Renvoie un booléen qui indique si un déplacement horizontal ou vertical est possible pour un pion partant d'une case rouge,
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


def gameIsOver(board_pawn : Init_Board_Pawn) -> tuple:
    """
        Verrifie si la partie est terminée et renvoie un tuple contenant un entier et un booléen.
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

# Zone de test

Q1, Q2, Q3, Q4 = genererQuart(), genererQuart(), genererQuart(), genererQuart()
board_Color = Init_Board_Color(Q1, Q2, Q3, Q4)
board_Color.affichage_test()
print("\n")
board_Pawn = Init_Board_Pawn()
board_Pawn.affichage_test()

print(checkCanMove((1, 1), (1, 2), board_Pawn)) 
print(checkCanMove((1, 1), (2, 0), board_Pawn)) 
print(checkCanMove((1, 1), (0, 0), board_Pawn)) 
print(checkCanMove((1, 1), (8, 1), board_Pawn)) 

print(gameIsOver(board_Pawn)) 

print(checkCanCapture((1, 1), (8, 5), board_Pawn)) 

print(getYellowCases(board_Color))
print(getRedCases(board_Color))

board_Pawn.setPlayer1sPawn(1)
print(gameIsOver(board_Pawn)) 
board_Pawn.setPlayer1sPawn(8)
board_Pawn.setPlayer2sPawn(1)
print(gameIsOver(board_Pawn)) 

board_Pawn.board[0][0], board_Pawn.board[0][9] = 1, 1
print(gameIsOver(board_Pawn)) 

board_Pawn.board[0][0], board_Pawn.board[0][9] = '2', '2'
board_Pawn.board[9][0], board_Pawn.board[9][9] = 2, 2
print(gameIsOver(board_Pawn)) 