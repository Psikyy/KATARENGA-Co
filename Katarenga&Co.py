class Case:
    
    def __init__(self, couleur, x, y):
        self.color = couleur
        self.x = x
        self.y = y
        if self.couleur == 'blue':
            self.deplacement = [(self.x-1, self.y-1), (self.x-1, self.y), (self.x-1, self.y+1), (self.x, self.y+1), (self.x+1, self.y+1), (self.x+1, self.y), (self.x+1, self.y-1), (self.x, self.y-1)]
        elif self.couleur == 'green':
            self.deplacement = [(self.x-2, self.y-1), (self.x-2, self.y-1), (self.x-1, self.y+2), (self.x+1, self.y+2), (self.x+2, self.y+1), (self.x+2, self.y-1), (self.x+1, self.y-2), (self.x-1, self.y-2)]
        elif self.couleur == 'red':
            self.deplacement = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        elif self.couleur == 'yellow':
            self.deplacement = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
    
    def getColor(self):
        return self.couleur
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getMoves(self):
        return self.deplacement


class Board:
    
    def __init__(self, zob):
        self.bite = zob
    
    def symetrie(liste):
        l = []
        for ligne in liste:
            l.append(ligne[::-1])
        return l