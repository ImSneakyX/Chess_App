import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.board import Board
from chessboard.pieces import Pawn, Rook, Knight, Queen, King, Bishop, Empty
import numpy as np

class Move(Board):
    def __init__(self, boardstate, start_square, end_square): 
        Board.__init__(self)
        self.start = boardstate
        self.start_square = start_square
        self.end_square = end_square
        self.piece = self.start[self.start_square]

        self.vision = None
        self.legal_move_mask = None
        self.order()

    def oder(self):
        pass

    def visions(self):
        pass

    def get_legal_move_mask(self):
        pass

    def is_move_legal(self): 
        pass


    def move(self):
        self.start1 = self.start.copy()
        legal = self.is_move_legal()
        if legal == True:
            self.start1[self.end_square] = self.piece
            self.start1[self.start_square] = self.empty
            self.pos_new = self.start1
            self.display('name', self.pos_new)
        else: 
            self.pos_new = self.start1
        return self.pos_new
    
    

class Move_White(Move):
    def __init__(self, boardstate, start_square, end_square): 
        Move.__init__(self, boardstate, start_square, end_square)


    def order(self):
        self.visions()
        self.get_legal_move_mask()
        self.move()
        

    def get_legal_move_mask(self):
        mask = np.zeros((8, 8), dtype = 'bool')
        if self.piece.color == 'w':
            moves, moves_for_vision = self.piece.get_legal_moves(self.start, self.start_square, self.vision)
            for row, col in moves: 
                mask[(row, col)] = True 
        self.legal_move_mask = mask
        return mask
    
    def visions(self):
        self.vision = np.zeros((8, 8), dtype = 'bool')
        for row, i in enumerate(self.start):
            for col, j in enumerate(i):
                if self.start[(row, col)].color == 'b' and isinstance(self.start[(row, col)], (Knight, Rook, Queen, Bishop)):
                    moves, moves_for_vision = self.start[(row, col)].get_legal_moves(self.start, (row, col), None)
                    for x, y in moves: 
                        self.vision[(x, y)] = True
                    for x, y in moves_for_vision:
                        self.vision[(x, y)] = True
                if self.start[(row, col)].color == 'b' and isinstance(self.start[(row, col)], Pawn):
                    if 0 <= col - 1 < 8:
                        self.vision[(row + 1, col - 1)] = True
                    if 0 <= col + 1 < 8:
                        self.vision[(row + 1, col + 1)] = True
                if self.start[(row, col)].color == 'b' and isinstance(self.start[(row, col)], King):
                    offsets = [(1, 1), (1, 0), (1, -1), (0,-1), (-1,-1), (-1,0), (-1,1), (0, 1)]
                    for x, y in offsets:
                        new_row, new_col = row + x, col + y
                        if 0 <= new_row <8 and 0 <= new_col <8:
                            self.vision[(new_row, new_col)] = True
        return self.vision
    
    def is_move_legal(self): 
        if self.legal_move_mask[self.end_square] == True and self.vision[self.find_piece(self.start, King, 'w')[0]] == False:
            print(f'Move is legal :)')
            legal = True
        else:
            print(f'Move is not legal! Try another one!')
            legal = False
        return legal

    

            

    
class Move_Black(Move):
    def __init__(self, boardstate, start_square, end_square): 
        Move.__init__(self, boardstate, start_square, end_square)

    def order(self):
        self.visions()
        square = self.find_piece(self.start, King, 'b')[0] # steht schwarz im Schach?
        if self.vision[square] == True:
            self.check()
        else: 
            self.get_legal_move_mask()
        self.is_move_legal()
        self.move()


    def get_legal_move_mask(self):
        mask = np.zeros((8, 8), dtype = 'bool')
        if self.piece.color == 'b':
            moves, moves_for_vision = self.piece.get_legal_moves(self.start, self.start_square, self.vision)
            for row, col in moves: 
                mask[(row, col)] = True 
        self.legal_move_mask = mask
        return mask
    
    def visions(self):
        self.vision = np.zeros((8, 8), dtype = 'bool')
        for row, i in enumerate(self.start):
            for col, j in enumerate(i):
                if self.start[(row, col)].color == 'w' and isinstance(self.start[(row, col)], (Rook, Knight, Bishop, Queen)):
                    moves, moves_for_vision = self.start[(row, col)].get_legal_moves(self.start, (row, col), None)
                    for x, y in moves: 
                        self.vision[(x, y)] = True
                    for x, y in moves_for_vision:
                        self.vision[(x, y)] = True
                if self.start[(row, col)].color == 'w' and isinstance(self.start[(row, col)], Pawn):
                    if 0 <= col - 1 < 8:
                        self.vision[(row - 1, col - 1)] = True
                    if 0 <= col + 1 < 8:
                        self.vision[(row - 1, col + 1)] = True
                if self.start[(row, col)].color == 'w' and isinstance(self.start[(row, col)], King):
                    offsets = [(1, 1), (1, 0), (1, -1), (0,-1), (-1,-1), (-1,0), (-1,1), (0, 1)]
                    for x, y in offsets:
                        new_row, new_col = row + x, col + y
                        if 0 <= new_row <8 and 0 <= new_col <8:
                            self.vision[(new_row, new_col)] = True
        return self.vision
    
    def is_move_legal(self): 
        if self.legal_move_mask[self.end_square] == True and self.vision[self.find_piece(self.start, King, 'b')[0]] == False:
            print(f'Move is legal :)')
            legal = True
        else:
            print(f'Move is not legal! Try another one!')
            legal = False
        return legal

    
    
if __name__ == '__main__':
    brett = Board()
    brett.start_position()
    brett1 = Move_White(brett.start, (7, 6), (5, 5))
    
    print(brett1.get_legal_move_mask())
    print(brett1.vision)






