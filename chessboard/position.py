import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.board import Board
from chessboard.pieces import Empty
from chessboard.pieces import Rook, King, Knight, Bishop, Queen, Pawn
import numpy as np


class Position: 

    def __init__(self, boardstate, white_to_move):
        
        self.board = Board()
        self.start_boardstate = self.board.start_position()
        self.boardstate = boardstate
        self.white_to_move = white_to_move
        self.castling_g = None
        self.castling_c = None
        

        if self.white_to_move == True:
            start_king = self.find_piece(self.start_boardstate, King, 'w')[0]
            start_rook_l = self.find_piece(self.start_boardstate, Rook, 'w', 'l')[0]
            start_rook_r = self.find_piece(self.start_boardstate, Rook, 'w', 'r')[0]
            self.vision = self.visions_black(self.boardstate)
            for i in range(8):
                for j in range(8):

                    if isinstance(self.boardstate[i, j], Rook):
                        if self.boardstate[i, j].color == 'w' and self.boardstate[i, j].side == 'l':
                            rook_l = self.boardstate[i, j]
                        elif self.boardstate[i, j].color == 'w' and self.boardstate[i, j].side == 'r':
                            rook_r = self.boardstate[i, j]
                    
                    elif isinstance(self.boardstate[i, j], King):
                        if self.boardstate[i, j].color == 'w':
                            king = self.boardstate[i, j]
                        
        else: 
            start_king = self.find_piece(self.start_boardstate, King, 'b')[0]
            start_rook_l = self.find_piece(self.start_boardstate, Rook, 'b', 'l')[0]
            start_rook_r = self.find_piece(self.start_boardstate, Rook, 'b', 'r')[0]
            self.vision = self.visions_white(self.boardstate)
            for i in range(8):
                for j in range(8):

                    if isinstance(self.boardstate[i, j], Rook):
                        if self.boardstate[i, j].color == 'b' and self.boardstate[i, j].side == 'l':
                            rook_l = self.boardstate[i, j]
                        elif self.boardstate[i, j].color == 'b' and self.boardstate[i, j].side == 'r':
                            rook_r = self.boardstate[i, j]

                    elif isinstance(self.boardstate[i, j], King):
                        if self.boardstate[i, j].color == 'b':
                            king = self.boardstate[i, j]

        self.castling(self.boardstate, rook_l.moved, rook_r.moved, king.moved, start_king, start_rook_l, start_rook_r, self.vision)

    def find_piece(self, boardstate, piece, color, side = None):
        square = []
        for row, i in enumerate(boardstate):
            for col, j in enumerate(i):
                if isinstance(boardstate[(row, col)], piece): 
                    if boardstate[(row, col)].color == color:
                        if piece == Rook:
                            if boardstate[(row, col)].side == side:
                                square.append((row, col))
                        else: 
                            square.append((row, col))
        return square



    def castling(self, boardstate, moved_rook_left, moved_rook_right, moved_king, start_square_king, start_square_rook_left, start_square_rook_right, vision):
        row, col = start_square_king 
        row_l, col_l = start_square_rook_left
        row_r, col_r = start_square_rook_right
        col_min_l, col_max_l = sorted([2, col])

        if moved_rook_left == False and moved_king == False and all(isinstance(square, Empty) for square in boardstate[row, col_l + 1:col]) == True and vision[row, col_min_l:col_max_l+1].any() == False:
            self.castling_c = True

        else:
            self.castling_c = False


        if moved_rook_right == False and moved_king == False and all(isinstance(square, Empty) for square in boardstate[row, col + 1:col_r]) == True and vision[row, col:col_r].any() == False:
            self.castling_g = True

        else:
            self.castling_g = False

    def visions_black(self, boardstate):
        self.vision_black = np.zeros((8, 8), dtype = 'bool')
        for row, i in enumerate(boardstate):
            for col, j in enumerate(i):
                if boardstate[(row, col)].color == 'b' and isinstance(boardstate[(row, col)], (Knight, Rook, Queen, Bishop)):
                    moves, moves_for_vision = boardstate[(row, col)].get_legal_moves(boardstate, (row, col), None)
                    for x, y in moves: 
                        self.vision_black[(x, y)] = True
                    for x, y in moves_for_vision:
                        self.vision_black[(x, y)] = True
                if boardstate[(row, col)].color == 'b' and isinstance(boardstate[(row, col)], Pawn):
                    if 0 <= col - 1 < 8 and 0 <= row + 1 < 8:
                        self.vision_black[(row + 1, col - 1)] = True
                    if 0 <= col + 1 < 8 and 0 <= row + 1 < 8:
                        self.vision_black[(row + 1, col + 1)] = True
                if boardstate[(row, col)].color == 'b' and isinstance(boardstate[(row, col)], King):
                    offsets = [(1, 1), (1, 0), (1, -1), (0,-1), (-1,-1), (-1,0), (-1,1), (0, 1)]
                    for x, y in offsets:
                        new_row, new_col = row + x, col + y
                        if 0 <= new_row <8 and 0 <= new_col <8:
                            self.vision_black[(new_row, new_col)] = True
        return self.vision_black
    
    def visions_white(self, boardstate):
        self.vision_white = np.zeros((8, 8), dtype = 'bool')
        for row, i in enumerate(boardstate):
            for col, j in enumerate(i):
                if boardstate[(row, col)].color == 'w' and isinstance(boardstate[(row, col)], (Rook, Knight, Bishop, Queen)):
                    moves, moves_for_vision = boardstate[(row, col)].get_legal_moves(boardstate, (row, col), None)
                    for x, y in moves: 
                        self.vision_white[(x, y)] = True
                    for x, y in moves_for_vision:
                        self.vision_white[(x, y)] = True
                if boardstate[(row, col)].color == 'w' and isinstance(boardstate[(row, col)], Pawn):
                    if 0 <= col - 1 < 8 and 0 <= row - 1 < 8:
                        self.vision_white[(row - 1, col - 1)] = True
                    if 0 <= col + 1 < 8 and 0 <= row - 1 < 8:
                        self.vision_white[(row - 1, col + 1)] = True
                if boardstate[(row, col)].color == 'w' and isinstance(boardstate[(row, col)], King):
                    offsets = [(1, 1), (1, 0), (1, -1), (0,-1), (-1,-1), (-1,0), (-1,1), (0, 1)]
                    for x, y in offsets:
                        new_row, new_col = row + x, col + y
                        if 0 <= new_row <8 and 0 <= new_col <8:
                            self.vision_white[(new_row, new_col)] = True
        return self.vision_white


if __name__ == '__main__':

    board = Board()
    start_boardstate = board.start_position()
    position = Position(start_boardstate, True)
    print(position.castling_g)