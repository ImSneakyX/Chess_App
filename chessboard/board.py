import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from chessboard.pieces import Pawn, Rook, Knight, Queen, King, Bishop, Empty

class Board:
    def __init__(self):
        self.board = np.zeros((8,8), 'object')
        self.start_pos = None
        self.notation = None
        self.king_b_start = None
        self.king_w_start = None

        #weiße Figuren
        self.pawn_w = Pawn('w')
        self.knight_w = Knight('w')
        self.bishop_w = Bishop('w')
        self.rook_w_l = Rook('w', 'l')
        self.rook_w_r = Rook('w', 'r')
        self.queen_w = Queen('w')
        self.king_w = King('w')

        #Schwarze Figuren
        self.pawn_b = Pawn('b')
        self.knight_b = Knight('b')
        self.bishop_b = Bishop('b')
        self.rook_b_l = Rook('b', 'l')
        self.rook_b_r = Rook('b', 'r')
        self.queen_b = Queen('b')
        self.king_b = King('b')

        #empty 
        self.empty = Empty()
    

        
    def start_position(self):
        self.start_pos = self.board.copy()
        #Bauern
        self.start_pos[1,:] = self.pawn_b
        self.start_pos[-2,:] = self.pawn_w
        
        #Türme

        self.start_pos[0,0] = self.rook_b_r
        self.start_pos[0, -1] = self.rook_b_l

        self.start_pos[-1, 0] = self.rook_w_l
        self.start_pos[-1, -1] = self.rook_w_r

        #Springer

        row = [0,0]
        col = [1, -2]
        self.start_pos[row, col] = self.knight_b

        row = [-1, -1]
        col = [1, -2]
        self.start_pos[row, col] = self.knight_w

        #Läufer
        row = [0,0]
        col = [2, -3]
        self.start_pos[row, col] = self.bishop_b

        row = [-1, -1]
        col = [2, -3]
        self.start_pos[row, col] = self.bishop_w

        #Dame
        self.start_pos[0, 3] = self.queen_b
        self.start_pos[-1,3] = self.queen_w

        #König
        self.start_pos[0, 4] = self.king_b
        self.start_pos[-1,4] = self.king_w
        self.king_b_start = (0 ,4)
        self.king_w_start = (7, 4)

        #leere Felder
        for i in range(2, 6):
            self.start_pos[i] = self.empty


        return self.start_pos


    def display(self, attribute, boardstate):
        for rows, i in enumerate(boardstate):
            for cols, j in enumerate(i):
                if boardstate[rows, cols].value == 0:
                    print(self.empty.value, end=' ')
                else:
                    value = getattr(boardstate[rows, cols], attribute)
                    print(f"{value}", end = ' ')
            print()

    def find_piece(self, boardstate, piece, color):
        square = []
        for row, i in enumerate(boardstate):
            for col, j in enumerate(i):
                if isinstance(boardstate[(row, col)], piece):
                    if boardstate[(row, col)].color == color:
                        square.append((row, col))
        return square
    
    def chessboard_notation(self): 
        row_name = self.board.copy()
        col_name = self.board.copy()
        self.notation = self.board.copy()

        rows = ['1', '2', '3', '4', '5', '6', '7', '8']
        cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        for idx, name in enumerate(rows):
            row_name[-idx-1] = name

        for idx, name in enumerate(cols):
                col_name[:,idx] = name 
        
        for row, i in enumerate(self.notation):
            for col, j in enumerate(i):
                self.notation[row, col] = ''.join((col_name[row, col], row_name[row, col]))

        return self.notation
    
    def abs_piece_value(self):

        sum_value_white = 0
        sum_value_black = 0
        add_pawn_value = 0

        for i in range(8):
            for j in range(8):
                piece = self.start_pos[i, j]
                if piece.color == 'w':
                    sum_value_white += piece.value
                    if piece.name == 'Pawn':
                        add_pawn_value += -0.1 * i + 0,6


                elif piece.color == 'b':
                    sum_value_black += piece.value
                    if piece.name == 'Pawn':
                        add_pawn_value -= 0.1 * i - 0,1

                

        abs_value = sum_value_white - sum_value_black

        return abs_value, add_pawn_value
    




  