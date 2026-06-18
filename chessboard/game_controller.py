import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.game_engine import GameEngine
from chess_engine.ultimate import Ultimate
from chessboard.board import Board
from chessboard.position import Position




class GameController:

    def __init__(self):

        self.gameEngine = GameEngine()
        self.gameEngine.position_update.connect(self.update_position)
        self.board = Board()
        self.position = Position(self.board.start_position(), True, True, True, True, True)
        self.ultimate = Ultimate()


    def update_position(self, position):

        self.position = Position(position[0], position[1])







