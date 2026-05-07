import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.board import Board
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
        self.move()

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


    def move(self):
        self.start1 = self.start.copy()
        if self.legal_move_mask[self.end_square] == True:
            self.start1[self.end_square] = self.piece
            self.start1[self.start_square] = self.empty
            self.pos_new = self.start1
            self.display('name', self.pos_new)
        else: self.pos_new = self.start1
        return self.pos_new

    
    
if __name__ == '__main__':
    brett = Board()
    brett.start_position()
    brett1 = Move(brett.start, (7, 6), (5, 5))
    print(brett1.get_legal_move_mask())





