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
        self.pawn = Pawn('w')
        self.knight = Knight('w')
        self.bishop = Bishop('w')
        self.rook = Rook('w')
        self.queen = Queen('w')
        self.king = King('w')
        self.start_position('w')
        self.color()
    def start_position(self):
        self.start = self.brett

        #Bauern
        self.start[1,:] = self.pawn
        self.start[-2,:] = self.pawn
        
        #Türme

        row = [0,-1, 0,-1]
        col = [0, 0, -1, -1]

        self.start[row, col] = self.rook

        #Springer
        col = [1, 1, -2, -2]
        row = [0,-1, 0, -1]
        self.start[row, col] = self.knight

        #Läufer
        col = [2, 2, -3, -3]
        row = [0, -1, 0, -1]
        self.start[row, col] = self.bishop

        #Dame
        row = [0, -1]
        col = [3, 3]
        self.start[row, col] = self.queen

        #König
        row = [0, -1]
        col = [4,4]
        self.start[row, col] = self.king


    def color(self):
        self.color = self.brett
        
brett = Board()
print(brett.start)
        