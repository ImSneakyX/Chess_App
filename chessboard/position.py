import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.board import Board
from chessboard.pieces import Empty
from chessboard.pieces import Rook, King, Knight, Bishop, Queen, Pawn, Empty
import numpy as np
import copy


class Position: 

    def __init__(self, boardstate, white_to_move, white_castle_c, white_castle_g, black_castle_c, black_castle_g):
        
        self.boardstate = boardstate
        self.white_to_move = white_to_move

        self.white_castle_c = white_castle_c
        self.white_castle_g = white_castle_g

        self.black_castle_c = black_castle_c
        self.black_castle_g = black_castle_g

        self.boardstate_new
        self.empty = Empty()
        self.piece = None

  
    

    def make_move(self, move):

        self.move = move
        self.piece = self.boardstate[self.move.start_square]
        self.boardstate_new = copy.deepcopy(self.boardstate)
        self.boardstate_new[self.move.end_square] = self.piece
        self.boardstate_new[self.move.start_square] = self.empty

        self.boardstate = self.boardstate_new









if __name__ == '__main__':

    board = Board()
    start_boardstate = board.start_position()
    position = Position(start_boardstate, True)
    print(position.castling_g)