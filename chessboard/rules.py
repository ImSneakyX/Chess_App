import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.move import Move_White, Move_Black

class Vision:
    def __init__(self):
        self.vision_w = Move_White()
        self.vision_b = Move_Black()

        

