import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from chessboard.pieces import Pawn, Rook, Knight, Queen, King, Bishop, Empty

class Board:
    def __init__(self):
        self.brett = np.zeros((8,8), 'object')
        self.start = None
        self.notation = None
        #weiße Figuren
        self.pawn_w = Pawn('w')
        self.knight_w = Knight('w')
        self.bishop_w = Bishop('w')
        self.rook_w = Rook('w')
        self.queen_w = Queen('w')
        self.king_w = King('w')

        #Schwarze Figuren
        self.pawn_b = Pawn('b')
        self.knight_b = Knight('b')
        self.bishop_b = Bishop('b')
        self.rook_b = Rook('b')
        self.queen_b = Queen('b')
        self.king_b = King('b')

        #empty 
        self.empty = Empty()
    

        
    def start_position(self):
        self.start = self.brett.copy()
        #Bauern
        self.start[1,:] = self.pawn_b
        self.start[-2,:] = self.pawn_w
        
        #Türme

        row = [0,0]
        col = [0, -1]
        self.start[row, col] = self.rook_b

        row = [-1,-1]
        col = [0, -1]
        self.start[row, col] = self.rook_w

        #Springer

        row = [0,0]
        col = [1, -2]
        self.start[row, col] = self.knight_b

        row = [-1, -1]
        col = [1, -2]
        self.start[row, col] = self.knight_w

        #Läufer
        row = [0,0]
        col = [2, -3]
        self.start[row, col] = self.bishop_b

        row = [-1, -1]
        col = [2, -3]
        self.start[row, col] = self.bishop_w

        #Dame
        self.start[0, 3] = self.queen_b
        self.start[-1,3] = self.queen_w

        #König
        self.start[0, 4] = self.king_b
        self.start[-1,4] = self.king_w

        #leere Felder
        for i in range(2, 6):
            self.start[i] = self.empty


        return self.start


    def display(self, attribute, boardstate):
        for rows, i in enumerate(boardstate):
            for cols, j in enumerate(i):
                if boardstate[rows, cols] == self.empty:
                    print(self.empty.value, end=' ')
                else:
                    value = getattr(boardstate[rows, cols], attribute)
                    print(f"{value}", end = ' ')
            print()

    def getposition(self, position):
        return self.start[position]
    
    def chessboard_notation(self): 
        row_name = self.brett.copy()
        col_name = self.brett.copy()
        self.notation = self.brett.copy()

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


    
    

if __name__ == '__main__':
    brett = Board()
    brett.start_position()
    brett.display('name', brett.start)
  