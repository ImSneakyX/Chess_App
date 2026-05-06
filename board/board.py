import numpy as np

class Piece:
    def __init__(self, name, value, color):
        self.move = 'Can move'
        self.name = name
        self.value = value
        self.color = color

    def get_legal_moves(self, boardstate, start_square):
        pass

class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'Pawn', 1, color)

    def get_legal_moves(self, boardstate, start_square):

        moves = []
        row, col = start_square

        if self.color == 'w':  
            if row > 0 and boardstate[row-1, col] == 0:
                moves.append((row-1, col))
        else:
            if row < 7 and boardstate[row+1, col] == 0:
                moves.append((row+1, col))
        return moves 


class Knight(Piece):
    def __init__(self,color):
        Piece.__init__(self, 'Knight', 3, color)

    def get_legal_moves(self, boardstate, start_square):
        
        moves = []
        row, col = start_square

        offsets = [(-2, 1), (-2, -1), (-1, -2), (1,-2), (2,-1), (2,1), (1,2), (-1, 2)]

        for x, y in offsets:
            new_row, new_col = row + x, col + y
            if 0 <= new_row <8 and 0 <= new_col <8:
                moves.append((new_row, new_col))
        return moves
         

class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'Bishop', 3, color)

    def get_legal_moves(self, boardstate, start_square):
        
        moves = []
        row, col = start_square

        limit1 = min(row, col) #oben links
        limit2 = min(7-row, 7-col) #unten rechts
        limit3 = min(7-row, col) #unten links
        limit4 = min(row, 7-col) #oben rechts

        for i in range(1, limit1 + 1):
            new_row, new_col = row - i, col - i 
            moves.append((new_row, new_col))

        for i in range(1, limit2 + 1):
            new_row, new_col = row + i, col + i 
            moves.append((new_row, new_col))

        for i in range(1, limit3 + 1):
            new_row, new_col = row + i, col - i 
            moves.append((new_row, new_col))

        for i in range(1, limit4 + 1):
            new_row, new_col = row - i, col + i 
            moves.append((new_row, new_col))

        return moves

class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'Rook', 5, color)

    def get_legal_moves(self, boardstate, start_square):
        moves = []
        row, col = start_square

        limit1 = row # oben
        limit2 = col #links 
        limit3 = 7 - row #unten
        limit4 = 7 - col #rechts


        for i in range(1, limit1 + 1):
            new_row, new_col = row - i, col
            moves.append((new_row, new_col))

        for i in range(1, limit2 + 1):
            new_row, new_col = row, col - i
            moves.append((new_row, new_col))

        for i in range(1, limit3 + 1):
            new_row, new_col = row + i, col
            moves.append((new_row, new_col))

        for i in range(1, limit4 + 1):
            new_row, new_col = row, col + 1
            moves.append((new_row, new_col))


        return moves




class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'Queen', 9, color)

    def get_legal_moves(self, boardstate, start_square):
        moves = []
        row, col = start_square

        limit1 = row # oben
        limit2 = col #links 
        limit3 = 7 - row #unten
        limit4 = 7 - col #rechts

        limit5 = min(row, col) #oben links
        limit6 = min(7-row, 7-col) #unten rechts
        limit7 = min(7-row, col) #unten links
        limit8 = min(row, 7-col) #oben rechts

        for i in range(1, limit1 + 1):
            new_row, new_col = row - i, col
            moves.append((new_row, new_col))

        for i in range(1, limit2 + 1):
            new_row, new_col = row, col - i
            moves.append((new_row, new_col))

        for i in range(1, limit3 + 1):
            new_row, new_col = row + i, col
            moves.append((new_row, new_col))

        for i in range(1, limit4 + 1):
            new_row, new_col = row, col + 1
            moves.append((new_row, new_col))

        for i in range(1, limit5 + 1):
            new_row, new_col = row - i, col - i 
            moves.append((new_row, new_col))

        for i in range(1, limit6 + 1):
            new_row, new_col = row + i, col + i 
            moves.append((new_row, new_col))

        for i in range(1, limit7 + 1):
            new_row, new_col = row + i, col - i 
            moves.append((new_row, new_col))

        for i in range(1, limit8 + 1):
            new_row, new_col = row - i, col + i 
            moves.append((new_row, new_col))

        return moves
    
class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'King', 100, color)

    def get_legal_moves(self, boardstate, start_square):
        
        moves = []
        row, col = start_square

        offsets = [(1, 1), (1, 0), (1, -1), (0,-1), (-1,-1), (-1,0), (-1,1), (0, 1)]

        for x, y in offsets:
            new_row, new_col = row + x, col + y
            if 0 <= new_row <8 and 0 <= new_col <8:
                moves.append((new_row, new_col))
        return moves
    
class Board:
    def __init__(self):
        self.brett = np.zeros((8,8), 'object')

        #weiße Figuren
        self.pawn_w = Pawn('w')
        self.knight_w = Knight('w')
        self.bishop_w = Bishop('w')
        self.rook_w = Rook('w')
        self.queen_w = Queen('w')
        self.king_w = King('w')

        #Schwarze Figuren
        self.pawn_b = Pawn('b')
        self.knight_b = Knight('b')
        self.bishop_b = Bishop('b')
        self.rook_b = Rook('b')
        self.queen_b = Queen('b')
        self.king_b = King('b')
        
        self.start_position()

        
    def start_position(self):
        self.start = self.brett

        #Bauern
        self.start[1,:] = self.pawn_b
        self.start[-2,:] = self.pawn_w
        
        #Türme

        row = [0,0]
        col = [0, -1]
        self.start[row, col] = self.rook_b

        row = [-1,-1]
        col = [0, -1]
        self.start[row, col] = self.rook_w

        #Springer

        row = [0,0]
        col = [1, -2]
        self.start[row, col] = self.knight_b

        row = [-1, -1]
        col = [1, -2]
        self.start[row, col] = self.knight_w

        #Läufer
        row = [0,0]
        col = [2, -3]
        self.start[row, col] = self.bishop_b

        row = [-1, -1]
        col = [2, -3]
        self.start[row, col] = self.bishop_w

        #Dame
        self.start[0, 3] = self.queen_b
        self.start[-1,3] = self.queen_w

        #König
        self.start[0, 4] = self.king_b
        self.start[-1,4] = self.king_w

        return self.start


    def display(self, attribute):
        for rows, i in enumerate(self.start):
            for cols, j in enumerate(i):
                if self.start[rows, cols] == 0:
                    print(0, end=' ')
                else:
                    value = getattr(self.start[rows, cols], attribute)
                    print(f"{value}", end = ' ')
            print()

    def getposition(self, position):
        return self.start[position]
    
    

if __name__ == '__main__':
    brett = Board()
    brett.display('name')
    print(brett.start_position())