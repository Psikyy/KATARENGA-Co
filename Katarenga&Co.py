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
    
    def __init__(self, quart_1 : list, quart_2 : list, quart_3 : int, quart_4 : int):
        self.q1 = quart_1
        self.q2 = quart_2
        self.q3 = quart_3
        self.q4 = quart_4
        self.board = None
    
    

    def degres_90(self, quart : list) -> list:
        """
            Renvoie un cadrant tourné à 90° vers la gauche
        """
        l = [[], [], [], []]
        for i in range(4):
            for j in range(3, -1, -1):
                l[i].append(quart[j][i])
        return l

    def degres_180(self, quart : list) -> list:
        """
            Renvoie cadrant tourné à 180°
        """
        l = [[], [], [], []]
        k = 0
        for i in range(3, -1, -1):
            for j in range(3, -1, -1):
                l[k].append(quart[i][j])
            k+=1
        return l

    def degres_270(self, quart : list) -> list:
        """
            Renvoie renvoie un cadrant tourné à 90° vers la droite
        """
        l = [[], [], [], []]
        k = 0
        for i in range(3, -1, -1):
            for j in range(4):
                l[k].append(quart[j][i])
            k+=1
        return l
        
    def symetrie(self, liste : list) -> list:
        """
            Renvoie un cadrant après avoir appliqué un effet mirroir dessus
        """
        l = []
        for ligne in liste:
            l.append(ligne[::-1])
        return l

    def board(self):
        liste = self.quart1
        k = 0
        for lignes in liste:
            for i in range(4):
                lignes.append(int(self.quart2[k][i]))
            k+=1
        liste_bis = self.quart3
        k = 0
        for lignes in liste_bis:
            for i in range(4):
                lignes.append(int(self.quart4[k][i]))
            k+=1
        return liste + liste_bis
"""
    Fin classe 'Init_Board'
"""




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
