import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.board import Board
from chessboard.new_pieces import Rook, King, Knight, Bishop, Queen, Pawn, Empty
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

        self.empty = Empty()
        self.piece = None

  
    

    def make_move(self, move):

        new_pos = copy.deepcopy(self)
        new_pos.piece = new_pos.boardstate[move.start_square]
        new_pos.boardstate[move.end_square] = new_pos.piece
        new_pos.boardstate[move.start_square] = new_pos.empty

        new_pos.white_to_move = not new_pos.white_to_move

        if move.start_square == (7, 4):
            new_pos.white_castle_c = False
            new_pos.white_castle_g = False

        if move.start_square == (7, 7):
            new_pos.white_castle_g = False

        if move.start_square == (7, 0):
            new_pos.white_castle_c = False

        if move.start_square == (0, 4):
            new_pos.black_castle_c = False
            new_pos.black_castle_g = False

        if move.start_square == (0, 7):
            new_pos.black_castle_g = False

        if move.start_square == (0, 0):
            new_pos.black_castle_c = False 

        if move.end_square == (7, 7):
            new_pos.white_castle_g = False   

        if move.end_square == (7, 0):
            new_pos.white_castle_c = False

        if move.end_square == (0, 7):
            new_pos.black_castle_g = False

        if move.end_square == (0, 0):
            new_pos.black_castle_c = False 

        if isinstance(new_pos.piece, King):

            if move.end_square == (0, 2) and move.start_square == (0, 4):

                new_pos.boardstate[0, 3] = new_pos.boardstate[0, 0]
                new_pos.boardstate[0, 0] = new_pos.empty

            elif move.end_square == (0, 6) and move.start_square == (0, 4):

                new_pos.boardstate[0, 5] = new_pos.boardstate[0, 7]
                new_pos.boardstate[0, 7] = new_pos.empty
            

            elif move.end_square == (7, 2) and move.start_square == (7, 4):

                new_pos.boardstate[7, 3] = new_pos.boardstate[7, 0]
                new_pos.boardstate[7, 0] = new_pos.empty

            elif move.end_square == (7, 6) and move.start_square == (7, 4):

                new_pos.boardstate[7, 5] = new_pos.boardstate[7, 7]
                new_pos.boardstate[7, 7] = new_pos.empty



        


        return new_pos












if __name__ == '__main__':

    board = Board()
    start_boardstate = board.start_position()
    position = Position(start_boardstate, True)
    print(position.castling_g)