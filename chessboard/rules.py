import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.move import Move_White, Move_Black

class Rules:
    def __init__(self):
        self.mate = None
        self.stalemate = None
        self.repetition = None
        self.fifty_move = None

        


        

