from board import Board, Pawn, Rook, Knight, Queen, King, Bishop


class Move(Board):
    def __init__(self, boardstate, start_square, end_square): 
        Board.__init__(self)
        self.start = boardstate
        self.start_square = start_square
        self.end_square = end_square
        self.piece = self.start[self.start_square]


    def move_white(self):
        if isinstance(self.piece, (Pawn, Rook, Knight, Queen, King, Bishop)):
            if self.piece.color == 'w': 
                self.start[self.end_square] = self.piece
                self.start[self.start_square] = 0
                self.pos_new = self.start
        return self.pos_new

    def move_black(self):
        if isinstance(self.piece, (Pawn, Rook, Knight, Queen, King, Bishop)):
            if self.piece.color == 'b': 
                self.start[self.end_square] = self.piece
                self.start[self.start_square] = 0
                self.pos_new = self.start
        return self.pos_new
    
    
    
    
    
brett = Board()
brett1 = Move(brett.start_position(), (-2, 4), (-4, 4))
print(brett1.move_white())



