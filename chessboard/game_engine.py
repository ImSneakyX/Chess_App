import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.move import Move_White, Move_Black
from chessboard.board import Board
from PyQt5.QtCore import pyqtSignal

class GameEngine:
    position_update = pyqtSignal(tuple)
    def __init__(self):
        self.white_to_move = True
        self.legal = None
        self.promotion = None
        
        self.mate = None
        self.stalemate = None

        self.brett = Board()
        self.start_pos = self.brett.start_position()
        self.position = self.brett.start_position()

    def check_move(self, start_square, end_square):
        if self.white_to_move == True:
            x = Move_White(self.position, start_square, end_square, self.start_pos) 
            if x.legal == True:
                self.legal = True
            else:
                self.legal = False

            if x.promotion == True:
                self.promotion = True
            else: 
                self.promotion = False

            self.mate = x.mate
            self.stalemate = x.stalemate

        else:
            x = Move_Black(self.position, start_square, end_square, self.start_pos)
            if x.legal == True:
                self.legal = True
            else:
                self.legal = False

            if x.promotion == True:
                self.promotion = True

            else: 
                self.promotion = False

            self.mate = x.mate
            self.stalemate = x.stalemate

        if x.legal == True:
            self.position = x.pos_new
            self.white_to_move = not self.white_to_move
            self.position_update.emit((self.position, self.white_to_move))


    def promote_pawns(self, piece, square_of_promotion):

        self.position[square_of_promotion] = piece
        

            

    

        
        

        