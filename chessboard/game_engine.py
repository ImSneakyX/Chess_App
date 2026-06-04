import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.move import Move_White, Move_Black
from chessboard.board import Board

class GameEngine:
    def __init__(self):
        self.white_to_move = True
        self.brett = Board()
        self.start_pos = self.brett.start_position()
        self.position = self.brett.start_position()

    def check_move(self, start_square, end_square):
        if self.white_to_move == True:
            x = Move_White(self.position, start_square, end_square, self.start_pos)

        else:
            x = Move_Black(self.position, start_square, end_square, self.start_pos)

        if x.legal == True:
            self.position = x.pos_new
            self.white_to_move = not self.white_to_move
            return True
        return False
    
    def check_promotion(self):

        pass

        