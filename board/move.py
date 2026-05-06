from board import Board, Pawn, Rook, Knight, Queen, King, Bishop
import numpy as np


class Move(Board):
    def __init__(self, boardstate, start_square, end_square): 
        Board.__init__(self)
        self.start = boardstate
        self.start_square = start_square
        self.end_square = end_square
        self.piece = self.start[self.start_square]

        self.legal_move_mask = None
        self.get_legal_move_mask()
        self.is_move_legal()

    def get_legal_move_mask(self):
        mask = np.zeros((8, 8), dtype = 'bool')
        moves = self.piece.get_legal_moves(self.start, self.start_square)
        for row, col in moves: 
            mask[(row, col)] = True 
        self.legal_move_mask = mask
        return mask

    def is_move_legal(self): 
        if self.legal_move_mask[self.end_square] == True:
            print(f'move is legal')
        else:
            print(f'move is not legal')

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
brett1 = Move(brett.start_position(), (-2, 4), (-3, 4))
print(brett1.move_white())



