from board import Board, Pawn


class Move(Board):
    def __init__(self, start, square): 
        Board.__init__(self)
        self.start = start
        self.square = square
        self.piece = self.start[self.square]

    def move_pawn(self):
        if isinstance(self.piece, Pawn):
            self.new_square = list(self.square)
            if self.piece.color == 'w':
                self.new_square[0] -= 1
            else:
                self.new_square[0] += 1
            self.new_square = tuple(self.new_square)
        self.start[self.new_square] = self.piece
        self.start[self.square] = 0
        self.pos_new = self.start
        return self.pos_new
    
    
    
    
    
    
brett = Board()
brett1 = Move(brett.start_position(), (-2, 4))
print(brett1.move_pawn())



