from chessboard.game_engine import GameEngine
from chess_engine.ultimate import Ultimate
from chessboard.board import Board




class GameController:

    def __init__(self):

        self.gameEngine = GameEngine()
        self.board = Board()
        self.ultimate = Ultimate(self.board.start_position())