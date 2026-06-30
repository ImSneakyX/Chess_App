import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.game_engine import GameEngine
from chess_engine.ultimate import Ultimate
from chessboard.board import Board
from chessboard.position import Position




class GameController:

    def __init__(self):


        self.board = Board()
        start_pos = self.board.start_position()
        abs_piece_value, add_pawn_value = self.board.abs_piece_value()

        self.position = Position(start_pos, self.board.king_w_start, self.board.king_b_start, True, True, True, True, True, abs_piece_value, add_pawn_value)
        self.gameEngine = GameEngine(self.position)
        self.ultimate = Ultimate()









