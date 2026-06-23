import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.board import Board
from chessboard.pieces import Rook, King, Knight, Bishop, Queen, Pawn, Empty
from chessboard.move import Undo


class Position: 

    def __init__(self, boardstate, king_w_pos, king_b_pos, white_to_move, white_castle_c, white_castle_g, black_castle_c, black_castle_g, en_passant_square = None):
        
        self.boardstate = boardstate
        self.white_to_move = white_to_move

        self.king_w_pos = king_w_pos        
        self.king_b_pos = king_b_pos

        self.white_castle_c = white_castle_c
        self.white_castle_g = white_castle_g

        self.black_castle_c = black_castle_c
        self.black_castle_g = black_castle_g

        self.en_passant_square = en_passant_square

        self.empty = Empty()

  
    

    def make_move(self, move):

        undo = Undo()

        undo.old_castle_white_c = self.white_castle_c
        undo.old_castle_white_g = self.white_castle_g
        undo.old_castle_black_c = self.black_castle_c
        undo.old_castle_black_g = self.black_castle_g

        undo.old_en_passant = self.en_passant_square

        undo.old_turn = self.white_to_move

        undo.moved_piece = self.boardstate[move.start_square]
        undo.captured_piece = self.boardstate[move.end_square]

        piece = self.boardstate[move.start_square]
        self.boardstate[move.end_square] = piece
        self.boardstate[move.start_square] = self.empty


        if move.start_square == (7, 4):
            self.white_castle_c = False
            self.white_castle_g = False

        if move.start_square == (7, 7):
            self.white_castle_g = False

        if move.start_square == (7, 0):
            self.white_castle_c = False

        if move.start_square == (0, 4):
            self.black_castle_c = False
            self.black_castle_g = False

        if move.start_square == (0, 7):
            self.black_castle_g = False

        if move.start_square == (0, 0):
            self.black_castle_c = False 

        if move.end_square == (7, 7):
            self.white_castle_g = False   

        if move.end_square == (7, 0):
            self.white_castle_c = False

        if move.end_square == (0, 7):
            self.black_castle_g = False

        if move.end_square == (0, 0):
            self.black_castle_c = False 

        if isinstance(piece, King):
            if piece.color == 'w':
                self.king_w_pos = move.end_square
            else:
                self.king_b_pos = move.end_square

            if move.end_square == (0, 2) and move.start_square == (0, 4):

                self.boardstate[0, 3] = self.boardstate[0, 0]
                self.boardstate[0, 0] = self.empty
                undo.rook_from = (0, 0)
                undo.rook_to = (0, 3)
                undo.rook = self.boardstate[0, 3]


            elif move.end_square == (0, 6) and move.start_square == (0, 4):

                self.boardstate[0, 5] = self.boardstate[0, 7]
                self.boardstate[0, 7] = self.empty
                undo.rook_from = (0, 7)
                undo.rook_to = (0, 5)
                undo.rook = self.boardstate[0, 5]

            

            elif move.end_square == (7, 2) and move.start_square == (7, 4):

                self.boardstate[7, 3] = self.boardstate[7, 0]
                self.boardstate[7, 0] = self.empty
                undo.rook_from = (7, 0)
                undo.rook_to = (7, 3)
                undo.rook = self.boardstate[7, 3]


            elif move.end_square == (7, 6) and move.start_square == (7, 4):

                self.boardstate[7, 5] = self.boardstate[7, 7]
                self.boardstate[7, 7] = self.empty
                undo.rook_from = (7, 7)
                undo.rook_to = (7, 5)
                undo.rook = self.boardstate[7, 5]

        elif isinstance(piece, Pawn):
            if move.promotion_piece != None:
                undo.promotion = piece
                if move.promotion_piece == 'Q':
                    self.boardstate[move.end_square] = Queen(piece.color)
                
                if move.promotion_piece == 'R':
                    self.boardstate[move.end_square] = Rook(piece.color, 'l')

                if move.promotion_piece == 'K':
                    self.boardstate[move.end_square] = Knight(piece.color)

                if move.promotion_piece == 'B':
                    self.boardstate[move.end_square] = Bishop(piece.color)

            elif move.en_passant == True:
                row_end, col_end = move.end_square
                if row_end == 2:
                    undo.ep_captured_piece = self.boardstate[3, col_end]
                    self.boardstate[3, col_end] = self.empty
                    undo.ep_captured_square = (3, col_end)


                else:
                    undo.ep_captured_piece = self.boardstate[4, col_end]
                    self.boardstate[4, col_end] = self.empty
                    undo.ep_captured_square = (4, col_end)
                    

            else: 
                row_start, col_start = move.start_square
                row_end, col_end = move.end_square

                if abs(row_start - row_end) == 2:
                    row_middle = (row_start + row_end) // 2

                    self.en_passant_square = (row_middle, col_start)
                
            



        self.white_to_move = not self.white_to_move

        return undo
    
    def unmake_move(self, move, undo):

        piece = self.boardstate[move.end_square]
        self.boardstate[move.start_square] = piece
        self.boardstate[move.end_square] = undo.captured_piece

        if undo.ep_captured_square is not None:
            self.boardstate[undo.ep_captured_square] = undo.ep_captured_piece

        self.white_castle_c = undo.old_castle_white_c
        self.white_castle_g = undo.old_castle_white_g
        self.black_castle_c = undo.old_castle_black_c
        self.black_castle_g = undo.old_castle_black_g

        if isinstance(piece, King):
            if piece.color == 'b':

                self.king_b_pos = move.start_square

            else:
                self.king_w_pos = move.start_square

        self.en_passant_square = undo.old_en_passant

        self.white_to_move = undo.old_turn

        if undo.promotion is not None:
            self.boardstate[move.start_square] = undo.promotion

        if undo.rook is not None:
            self.boardstate[undo.rook_from] = undo.rook
            self.boardstate[undo.rook_to] = self.empty


        












if __name__ == '__main__':

    board = Board()
    start_boardstate = board.start_position()
    position = Position(start_boardstate, True)
    print(position.castling_g)