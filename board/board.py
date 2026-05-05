import numpy as np

class Piece:
    def __init__(self, name, value, color):
        self.move = 'Can move'
        self.name = name
        self.value = value
        self.color = color

class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'Pawn', 1, color)

class Knight(Piece):
    def __init__(self,color):
        Piece.__init__(self, 'Knight', 3, color)

class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'Bishop', 3, color)


class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'Rook', 5, color)


class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'Queen', 9, color)


class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'King', 100, color)


class Board:
    def __init__(self):
        self.brett = np.zeros(64, 'object')
        self.brett = self.brett.reshape(8,8)

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

    def display(self, attribute):
        for rows, i in enumerate(self.start):
            for cols, j in enumerate(i):
                if self.start[rows, cols] == 0:
                    print(0, end=' ')
                else:
                    value = getattr(self.start[rows, cols], attribute)
                    print(f"{value}", end = ' ')
            print()

if __name__ == '__main__':
    brett = Board()
    brett.display('color')