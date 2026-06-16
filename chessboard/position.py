from chessboard.board import Board
from chessboard.pieces import Empty


class Position: 

    def __init__(self):
        
        self.board = Board()
        self.castling_g = None
        self.castling_c = None

    def castling(self, boardstate, moved_rook_left, moved_rook_right, moved_king, start_square_king, start_square_rook_left, start_square_rook_right, vision):
        row, col = start_square_king 
        row_l, col_l = start_square_rook_left
        row_r, col_r = start_square_rook_right
        col_min_l, col_max_l = sorted([2, col])

        if moved_rook_left == False and moved_king == False and all(isinstance(square, Empty) for square in boardstate[row, col_l + 1:col]) == True and vision[row, col_min_l:col_max_l+1].any() == False:
            self.castling_c = True

        else:
            self.castling_c = False


        if moved_rook_right == False and moved_king == False and all(isinstance(square, Empty) for square in boardstate[row, col + 1:col_r]) == True and vision[row, col:col_r].any() == False:
            self.castling_g = True

        else:
            self.castling_g = False
