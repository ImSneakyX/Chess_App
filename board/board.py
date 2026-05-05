import numpy as np

class Piece:
    def __init__(self, name, value):
        self.move = 'Can move'
        self.name = name
        self.value = value


class Pawn(Piece):
    def __init__(self):
        Piece.__init__(self, 'Pawn', 1)

class Knight(Piece):
    def __init__(self):
        Piece.__init__(self, 'Knight', 3)

class Bishop(Piece):
    def __init__(self):
        Piece.__init__(self, 'Bishop', 3)


class Rook(Piece):
    def __init__(self):
        Piece.__init__(self, 'Rook', 5)


class Queen(Piece):
    def __init__(self):
        Piece.__init__(self, 'Queen', 9)


class King(Piece):
    def __init__(self):
        Piece.__init__(self, 'King', np.inf)


class White:
    pass

class Black: 
    pass


class Board:
    def __init__(self):
        self.brett = np.zeros(64, dtype = 'object')
        self.brett = self.brett.reshape(8,8)
        self.pawn = Pawn()
        self.knight = Knight()
        self.bishop = Bishop()
        self.rook = Rook()
        self.queen = Queen()
        self.king = King()
        self.start_position()
        
    def start_position(self):
        self.start = self.brett

        #Bauern
        self.start[1,:] = self.pawn.value
        self.start[-2,:] = self.pawn.value
        #Türme

        row = [0,-1, 0,-1]
        col = [0, 0, -1, -1]

        self.start[row, col] = self.rook.value

        #Springer
        col = [1, 1, -2, -2]
        row = [0,-1, 0, -1]
        self.start[row, col] = self.knight.value

        #Läufer
        col = [2, 2, -3, -3]
        row = [0, -1, 0, -1]
        self.start[row, col] = self.bishop.value

        #Dame
        row = [0, -1]
        col = [3, 3]
        self.start[row, col] = self.queen.value

        #König
        row = [0, -1]
        col = [4,4]
        self.start[row, col] = self.king.value
        
brett = Board()
print(brett.start)
        