import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.board import Board
from chessboard.pieces import Pawn, Rook, Knight, Queen, King, Bishop, Empty
import numpy as np

class Move(Board):
    def __init__(self, boardstate, start_square, end_square, start_pos): 
        Board.__init__(self)
        self.start_pos = start_pos
        self.start = boardstate
        self.start_square = start_square
        self.end_square = end_square
        self.piece = self.start[self.start_square]

        self.moved_king = False
        self.moved_rook_l = False
        self.moved_rook_r = False

        self.vision = None
        self.legal_move_mask = None
        self.legal = None
        self.pos_new = None
        self.order()

    def order(self):
        pass

    def visions(self):
        pass

    def get_legal_move_mask(self):
        pass


    def move(self):
        pass

    
    
    

class Move_White(Move):
    def __init__(self, boardstate, start_square, end_square, start_pos): 
        Move.__init__(self, boardstate, start_square, end_square, start_pos)

    def order(self):
        self.visions(self.start)
        self.castling_white()
        self.get_legal_move_mask()
        self.move()


    def castling_white(self):
        self.king_start = self.find_piece(self.start_pos, King, 'w')[0]
        self.king = self.start_pos[self.king_start]

        self.rook_starts = self.find_piece(self.start_pos, Rook, 'w')
        self.rook_l = self.start_pos[self.rook_starts[0]]
        self.rook_r = self.start_pos[self.rook_starts[1]]
        self.king.castling(self.start, self.rook_l.moved, self.rook_r.moved, self.king.moved, self.king_start, self.rook_starts[0], self.rook_starts[1], self.vision)

        

    def get_legal_move_mask(self):
        mask = np.zeros((8, 8), dtype = 'bool')
        if self.piece.color == 'w':
            moves, moves_for_vision = self.piece.get_legal_moves(self.start, self.start_square, self.vision)
            for row, col in moves: 
                mask[(row, col)] = True 
        self.legal_move_mask = mask
        return mask
    
    def visions(self, boardstate):
        self.vision = np.zeros((8, 8), dtype = 'bool')
        for row, i in enumerate(boardstate):
            for col, j in enumerate(i):
                if boardstate[(row, col)].color == 'b' and isinstance(boardstate[(row, col)], (Knight, Rook, Queen, Bishop)):
                    moves, moves_for_vision = boardstate[(row, col)].get_legal_moves(boardstate, (row, col), None)
                    for x, y in moves: 
                        self.vision[(x, y)] = True
                    for x, y in moves_for_vision:
                        self.vision[(x, y)] = True
                if boardstate[(row, col)].color == 'b' and isinstance(boardstate[(row, col)], Pawn):
                    if 0 <= col - 1 < 8:
                        self.vision[(row + 1, col - 1)] = True
                    if 0 <= col + 1 < 8:
                        self.vision[(row + 1, col + 1)] = True
                if boardstate[(row, col)].color == 'b' and isinstance(boardstate[(row, col)], King):
                    offsets = [(1, 1), (1, 0), (1, -1), (0,-1), (-1,-1), (-1,0), (-1,1), (0, 1)]
                    for x, y in offsets:
                        new_row, new_col = row + x, col + y
                        if 0 <= new_row <8 and 0 <= new_col <8:
                            self.vision[(new_row, new_col)] = True
        return self.vision
    
    def move(self):
        self.start1 = self.start.copy()
        piece_on_end_square = self.start1[self.end_square]
        if self.legal_move_mask[self.end_square] == True:
            self.start1[self.end_square] = self.piece
            self.start1[self.start_square] = self.empty

            if isinstance(self.piece, King) and self.start_square == self.king_start and self.end_square == (7, 6):
                self.start1[self.rook_starts[1]] = self.empty
                self.start1[(7, 5)] = self.rook_r

            if isinstance(self.piece, King) and self.start_square == self.king_start and self.end_square == (7, 2):
                self.start1[self.rook_starts[0]] = self.empty
                self.start1[(7, 3)] = self.rook_l

            if isinstance(self.piece, Pawn) and isinstance(piece_on_end_square, Empty) and self.start_square[1] != self.end_square[1]:
                self.start1[(self.start_square[0], self.end_square[1])] = self.empty

            if isinstance(self.piece, Pawn) and self.start_square[0] == 6 and self.end_square[0] == 4:
                self.start1[self.end_square] = self.pawn_w 
                self.pawn_w.two_steps()



            self.pos_new = self.start1
            self.visions(self.pos_new)
            if self.vision[self.find_piece(self.pos_new, King, 'w')[0]] == False:
                print(f'Move is legal :)')
                self.legal = True
                self.display('name', self.pos_new)
            else: 
                print(f'Move is not legal! Try another one!')
                self.pos_new = self.start1
                self.legal = False
        else: 
            print(f'Move is not legal! Try another one!')
            self.pos_new = self.start1
            self.legal = False

        # Move-Tracker 
        if self.legal == True:
            self.moved_king = self.king.move_tracker(self.king_start, self.start_square)
            self.moved_rook_l = self.rook_l.move_tracker(self.rook_starts[0], self.start_square)
            self.moved_rook_r = self.rook_r.move_tracker(self.rook_starts[1], self.start_square)
            for row, i in enumerate(self.start1):
                for col, j in enumerate(i):
                    if isinstance(self.start1[row, col], Pawn) and self.start1[row, col] != self.pawn_w: 
                        self.start1[row, col].moved_two_steps = False
        return self.pos_new


    

            

    
class Move_Black(Move):
    def __init__(self, boardstate, start_square, end_square, start_pos): 
        Move.__init__(self, boardstate, start_square, end_square, start_pos)
        

    def order(self):
        self.visions(self.start)
        self.castling_black()
        self.get_legal_move_mask()
        self.move()

    def castling_black(self):
        self.king_start = self.find_piece(self.start_pos, King, 'b')[0]
        self.king = self.start_pos[self.king_start]

        self.rook_starts = self.find_piece(self.start_pos, Rook, 'b')
        self.rook_l = self.start_pos[self.rook_starts[0]]
        self.rook_r = self.start_pos[self.rook_starts[1]]
        self.king.castling(self.start, self.rook_l.moved, self.rook_r.moved, self.king.moved, self.king_start, self.rook_starts[0], self.rook_starts[1], self.vision)

    def get_legal_move_mask(self):
        mask = np.zeros((8, 8), dtype = 'bool')
        if self.piece.color == 'b':
            moves, moves_for_vision = self.piece.get_legal_moves(self.start, self.start_square, self.vision)
            for row, col in moves: 
                mask[(row, col)] = True 
        self.legal_move_mask = mask
        return mask
    
    def visions(self, boardstate):
        self.vision = np.zeros((8, 8), dtype = 'bool')
        for row, i in enumerate(boardstate):
            for col, j in enumerate(i):
                if boardstate[(row, col)].color == 'w' and isinstance(boardstate[(row, col)], (Rook, Knight, Bishop, Queen)):
                    moves, moves_for_vision = boardstate[(row, col)].get_legal_moves(boardstate, (row, col), None)
                    for x, y in moves: 
                        self.vision[(x, y)] = True
                    for x, y in moves_for_vision:
                        self.vision[(x, y)] = True
                if boardstate[(row, col)].color == 'w' and isinstance(boardstate[(row, col)], Pawn):
                    if 0 <= col - 1 < 8:
                        self.vision[(row - 1, col - 1)] = True
                    if 0 <= col + 1 < 8:
                        self.vision[(row - 1, col + 1)] = True
                if boardstate[(row, col)].color == 'w' and isinstance(boardstate[(row, col)], King):
                    offsets = [(1, 1), (1, 0), (1, -1), (0,-1), (-1,-1), (-1,0), (-1,1), (0, 1)]
                    for x, y in offsets:
                        new_row, new_col = row + x, col + y
                        if 0 <= new_row <8 and 0 <= new_col <8:
                            self.vision[(new_row, new_col)] = True
        return self.vision
    
    def move(self):
        self.start1 = self.start.copy()
        piece_on_end_square = self.start1[self.end_square]
        if self.legal_move_mask[self.end_square] == True:
            self.start1[self.end_square] = self.piece
            self.start1[self.start_square] = self.empty
            if isinstance(self.piece, King) and self.start_square == self.king_start and self.end_square == (0, 6):
                self.start1[self.rook_starts[1]] = self.empty
                self.start1[(0, 5)] = self.rook_r

            if isinstance(self.piece, King) and self.start_square == self.king_start and self.end_square == (0, 2):
                self.start1[self.rook_starts[0]] = self.empty
                self.start1[(0, 3)] = self.rook_l

            if isinstance(self.piece, Pawn) and isinstance(piece_on_end_square, Empty) and self.start_square[1] != self.end_square[1]:
                self.start1[(self.start_square[0], self.end_square[1])] = self.empty
            
            if isinstance(self.piece, Pawn) and self.start_square[0] == 1 and self.end_square[0] == 3:
                self.start1[self.end_square] = self.pawn_b
                self.pawn_b.two_steps()

            self.pos_new = self.start1
            self.visions(self.pos_new)
            if self.vision[self.find_piece(self.pos_new, King, 'b')[0]] == False:
                print(f'Move is legal :)')
                self.legal = True
                self.display('name', self.pos_new)
            else: 
                print(f'Move is not legal! Try another one!')
                self.legal = False
                self.pos_new = self.start1
        else: 
            print(f'Move is not legal! Try another one!')
            self.legal = False
            self.pos_new = self.start1

        # Move-Tracker 
        if self.legal == True:
            self.moved_king = self.king.move_tracker(self.king_start, self.start_square)
            self.moved_rook_l = self.rook_l.move_tracker(self.rook_starts[0], self.start_square)
            self.moved_rook_r = self.rook_r.move_tracker(self.rook_starts[1], self.start_square)
            for row, i in enumerate(self.start1):
                for col, j in enumerate(i):
                    if isinstance(self.start1[row, col], Pawn) and self.start1[row, col] != self.pawn_b: 
                        self.start1[row, col].moved_two_steps = False
        return self.pos_new
    

    
    
if __name__ == '__main__':
    brett = Board()
    brett.start_position()
    brett1 = Move_White(brett.start_pos, (7, 6), (5, 5))
    
    print(brett1.get_legal_move_mask())
    print(brett1.vision)






