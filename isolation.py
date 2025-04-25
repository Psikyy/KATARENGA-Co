class PlacementGame:
    def __init__(self, size=8):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.current_player = 1  
        
    def position(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size
        
    def attaqué(self, x, y, pieces):
        for piece_x in range(self.size):
            for piece_y in range(self.size):
                if self.board[piece_x][piece_y] is not None:
                    piece = pieces[piece_x][piece_y]
                    #recupere les deplacements possibles de la piece
                    moves = piece.getMoves()
                    #regarde si la position (x, y) est attaquée par la piece
                    for move_x, move_y in moves:
                        attack_x = piece_x + move_x
                        attack_y = piece_y + move_y
                        if (attack_x, attack_y) == (x, y):
                            return True
        return False
    
    def placement_plossible(self, pieces):
        valid_moves = []
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] is None and not self.attaqué(x, y, pieces):
                    valid_moves.append((x, y))
        return valid_moves
    
    def place_piece(self, x, y, pieces):
        if not self.position(x, y):
            return False, "Position en dehors du plateau"
            
        if self.board[x][y] is not None:
            return False, "Position deja occupee"
            
        if self.attaqué(x, y, pieces):
            return False, "Position attaquée"
            
        self.board[x][y] = self.current_player # Place la piece sur le plateau
        
        self.current_player = 3 - self.current_player  # echanger entre joueur 1 et joueur 2
        
        return True, "Piece placée avec succès"
    
    def fin(self, pieces):
        return len(self.placement_plossible(pieces)) == 0
    
    def vainqueur(self, pieces):
        if not self.fin(pieces):
            return None
        return 3 - self.current_player
    
    def plateau(self):
        for row in self.board:
            print(['-' if cell is None else f'P{cell}' for cell in row])